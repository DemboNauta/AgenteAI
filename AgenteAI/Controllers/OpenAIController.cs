using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using OpenAI;
using OpenAI.Assistants;
using OpenAI.Chat;
using System.Text.Json;

[ApiController]
[Route("api/[controller]")]
public class OpenAIController : ControllerBase
{
    private readonly ChatClient _client;
    private readonly string _connectionString;

    private readonly List<string> ejemplosDePeticiones = new List<string>()
{
        "¿Qué agente tiene más solicitudes? Quiero saber quién es y cómo contactarlo.",
        "Enséñame los pisos disponibles con al menos 3 habitaciones que cuesten menos de 200,000 euros.",
        "¿Qué solicitudes ha gestionado María Gómez?",
        "¿Hay algún agente que no tenga solicitudes? Quiero saber quién es.",
        "Muéstrame las casas que tiene Juan Pérez, con los precios y características.",
        "¿Cuáles son los inmuebles más caros que gestiona cada agente?",
        "¿Cuántas solicitudes de compra se han hecho esta semana?",
        "Quiero ver todas las casas disponibles y qué agente las gestiona.",
        "¿Qué pisos grandes están disponibles? Necesito uno con al menos 4 habitaciones.",
        "¿Qué agente tiene casas con vistas al mar?",
        "¿Quién gestiona el piso de la Calle Mayor 123, Madrid? Quiero su contacto.",
        "Estoy buscando casas para alquilar con al menos 2 habitaciones. ¿Qué tienes?",
        "Quiero un piso grande, más de 150 metros cuadrados, gestionado por Ana Martín. ¿Hay algo?",
        "¿Qué agente tiene más pisos asignados?",
        "¿Qué solicitudes están relacionadas con casas en la playa?",
        "Muéstrame los pisos que tiene Carlos López ordenados por precio, del más caro al más barato.",
        "Me gusta mucho la playa, que pisos hay que puedan tener playa cerca?"
    };

    public OpenAIController(ChatClient chatClient, IConfiguration config)
    {
        _client = chatClient;
        _connectionString = config.GetConnectionString("DefaultConnection") ?? throw new Exception("No hay connectionString");
    }

    [HttpPost("query")]
    public async Task<IActionResult> QueryDatabase([FromBody] string userQuery)
    {
        if (string.IsNullOrEmpty(userQuery))
        {
            return BadRequest("La consulta no puede estar vacía.");
        }

        try
        {
            var sqlQuery = await GenerateSqlQueryAsync(userQuery);

            var queryResults = await ExecuteSqlQueryAsync(sqlQuery);

            var response = await GenerateNaturalResponseAsync(userQuery, queryResults);

            return Ok(new { respuesta = response });
        }
        catch (SqlException ex)
        {
            return Ok(new { mensaje = "Uy, parece que tuvimos un problema al realizar la consulta. Por favor, inténtalo de nuevo o verifica tu solicitud." });
        }
        catch (Exception ex)
        {
            return Ok(new { mensaje = "Uy, ocurrió un problema inesperado. Intenta nuevamente más tarde." });
        }
    }

    private async Task<string> GenerateSqlQueryAsync(string userQuery)
    {
        var databaseContext = GetDatabaseContext();
        var messages = new List<ChatMessage>
            {
                new SystemChatMessage($"Eres un asistente experto en SQLserver ten en cuenta que estamos usando sqlserver para no hacer consultas incompatibles. Aquí está la estructura de la base de datos:\n{databaseContext}\nGenera una consulta SQL válida basandote en la estructura, es extremadmente importante que respondas solo con el texto de la consulta, ni una palabra más. Además ciñete a la estructura de las tablas, no puedes inventarte columnas, campos o tablas, además si te piden cosas concretas como descripciones o similares trata de usar like para abordar mejor"),
                new UserChatMessage(userQuery)
            };

        ChatCompletion completion = await this._client.CompleteChatAsync(messages);

        if (completion.Content == null || !completion.Content.Any())
        {
            throw new Exception("No se pudo generar una consulta SQL válida.");
        }

        return completion.Content[0].Text.Trim();
    }

    private async Task<List<Dictionary<string, object>>> ExecuteSqlQueryAsync(string sqlQuery)
    {
        var results = new List<Dictionary<string, object>>();

        try
        {
            using (var connection = new SqlConnection(_connectionString))
            {
                await connection.OpenAsync();
                using (var command = new SqlCommand(sqlQuery, connection))
                {
                    using (var reader = await command.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            var row = new Dictionary<string, object>();
                            for (int i = 0; i < reader.FieldCount; i++)
                            {
                                row[reader.GetName(i)] = reader.GetValue(i);
                            }
                            results.Add(row);
                        }
                    }
                }
            }
        }
        catch (Exception)
        {
            throw new Exception("Error al ejecutar la consulta");
        }

        return results;
    }

    private string GetDatabaseContext()
    {
        return @"
        1. Tabla: Agentes
           - Columnas:
             - IdAgente (int): Identificador único del agente.
             - Nombre (nvarchar): Nombre del agente.
             - Correo (nvarchar): Correo electrónico del agente.
             - Telefono (nvarchar): Número de teléfono (opcional).

        2. Tabla: Solicitudes
           - Columnas:
             - IdSolicitud (int): Identificador único de la solicitud.
             - IdAgente (int): Relación con la tabla Agentes.
             - FechaSolicitud (datetime): Fecha de la solicitud.
             - Descripcion (nvarchar): Descripción de la solicitud.

           Relaciones:
           - Solicitudes.IdAgente está relacionado con Agentes.IdAgente.

        3. Tabla: Propiedades
           - Columnas:
             - IdPropiedad (int): Identificador único de la propiedad.
             - Direccion (nvarchar): Dirección de la propiedad.
             - Precio (decimal): Precio de la propiedad.
             - Habitaciones (int): Número de habitaciones.
             - Banos (int): Número de baños.
             - Tamano (int): Tamaño de la propiedad en metros cuadrados.
             - Disponible (bit): Indica si la propiedad está disponible (1) o no (0).
             - IdAgente (int): Relación con la tabla Agentes.

           Relaciones:
           - Propiedades.IdAgente está relacionado con Agentes.IdAgente.
        ";
    }

    private async Task<string> GenerateNaturalResponseAsync(string userQuery, List<Dictionary<string, object>> queryResults)
    {
        const int maxResults = 5; // Limitar la cantidad de resultados
        var limitedResults = queryResults.Take(maxResults);

        var resultSummary = string.Join("\n", limitedResults.Select(r =>
            string.Join(", ", r.Select(kv => $"{kv.Key}: {kv.Value}"))
        ));

        var chatMessages = new List<ChatMessage>
        {
            new SystemChatMessage($"Eres un asistente que convierte datos SQL en respuestas en lenguaje natural de el CRM inmobiliario Mobilia. Es importante que no hables sobre sql como tal, ya que vas a responder a los usuarios, te vamos a pasar los datos, tu solo tienes que pasarlo a lenguaje natrual, esta es la repsuesta que hemos obtenido de la base de datos: Resultados de la consulta:\\n{resultSummary}\""),
            new UserChatMessage(userQuery),
        };

        ChatCompletion response = await _client.CompleteChatAsync(chatMessages);

        if (response.Content == null || !response.Content.Any())
        {
            throw new Exception("No se pudo generar una respuesta en lenguaje natural.");
        }

        return response.Content[0].Text.Trim();
    }
}
