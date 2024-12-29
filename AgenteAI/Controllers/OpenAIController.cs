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
        catch (Exception ex)
        {
            return StatusCode(500, $"Error: {ex.Message}");
        }
    }

    private async Task<string> GenerateSqlQueryAsync(string userQuery){
        var databaseContext = GetDatabaseContext();
        var messages = new List<ChatMessage>
            {
                new SystemChatMessage($"Eres un asistente experto en SQLserver ten en cuenta que estamos usando sqlserver para no hacer consultas incompatibles. Aquí está la estructura de la base de datos:\n{databaseContext}\nGenera una consulta SQL válida basandota en la estructura, es extremadmente importante que respondas solo con el texto de la consulta, ni una palabra más."),
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
        new SystemChatMessage("Eres un asistente que convierte datos SQL en respuestas en lenguaje natural de el CRM inmobiliario Mobilia. Es importante que no hables sobre sql como tal, ya que vas a responder a los usuarios, te vamos a pasar los datos, tu solo tienes que pasarlo a lenguaje natrual"),
        new UserChatMessage(userQuery),
        new AssistantChatMessage($"Aquí tienes los primeros {maxResults} resultados:\n{resultSummary}")
    };

        ChatCompletion response = await _client.CompleteChatAsync(chatMessages);

        if (response.Content == null || !response.Content.Any())
        {
            throw new Exception("No se pudo generar una respuesta en lenguaje natural.");
        }

        return response.Content[0].Text.Trim();
    }

}
