using Microsoft.Extensions.AI;
using Microsoft.Extensions.DependencyInjection;
using OpenAI;
using OpenAI.Chat;

var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddUserSecrets<Program>();

builder.Services.AddSingleton<ChatClient>(sp =>
{
    var configuration = sp.GetRequiredService<IConfiguration>();
    var apiKey = configuration["OpenAI:ApiKey"];
    var model = configuration["OpenAI:Model"];

    if (string.IsNullOrEmpty(apiKey))
    {
        throw new Exception("No se encontró la clave de OpenAI en los User Secrets.");
    }

    if (string.IsNullOrEmpty(model))
    {
        model = "gpt-3.5-turbo"; // Modelo por defecto
    }

    return new ChatClient(model, apiKey); // Instancia explícita de ChatClient
});




builder.Services.AddSingleton(builder.Configuration);



// Configurar los controladores y Swagger
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configurar el pipeline HTTP
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseAuthorization();

app.MapControllers();

app.Run();
