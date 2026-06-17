using AskMyDocs.Web.Models;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using static System.Net.WebRequestMethods;

namespace AskMyDocs.Web.Services;

public class ApiService
{
    private readonly HttpClient _httpClient;
    private const string _baseUrl = "http://localhost:8000";

    public ApiService(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task StreamQuestion(
    string question,
    List<ChatMessage> history,
    Action<string> onChunk)
    {
        var payload = new
        {
            question = question,
            history = history
        };

        var json = JsonSerializer.Serialize(
            payload,
            new JsonSerializerOptions
            {
                PropertyNamingPolicy =
                    JsonNamingPolicy.CamelCase
            });

        var content = new StringContent(
            json,
            Encoding.UTF8,
            "application/json");

        var request = new HttpRequestMessage(
            HttpMethod.Post,
            $"{_baseUrl}/chat");

        request.Content = content;

        var response = await _httpClient.SendAsync(
            request,
            HttpCompletionOption.ResponseHeadersRead);

        using var stream =
            await response.Content.ReadAsStreamAsync();

        byte[] buffer = new byte[128];

        while (true)
        {
            var bytesRead = await stream.ReadAsync(
                buffer,
                0,
                buffer.Length);

            if (bytesRead == 0)
                break;

            var chunk = Encoding.UTF8.GetString(
                buffer,
                0,
                bytesRead);

            onChunk(chunk);
        }
    }


    public async Task<string> AskQuestion(string question)
    {
        var response = await _httpClient.PostAsJsonAsync(
            $"{_baseUrl}/chat",
            new
            {
                question = question
            });

        var json = await response.Content.ReadAsStringAsync();
        using var document = JsonDocument.Parse(json);

        var answer = document
            .RootElement
            .GetProperty("answer")
            .GetString();

        return answer ?? "";
    }

    public async Task<string> GenerateTitle(string question)
    {
        var response =
            await _httpClient.PostAsJsonAsync(
                $"{_baseUrl}/generate-title",
                new
                {
                    question = question
                });

        var result =
            await response.Content
                .ReadFromJsonAsync
                <TitleResponse>();

        return result?.Title
            ?? "New Chat";
    }

    public async Task<List<DocumentInfo>> GetDocuments()
    {
        return await _httpClient.GetFromJsonAsync<List<DocumentInfo>>(
            $"{_baseUrl}/documents"
        ) ?? new();
    }

    public async Task DeleteDocument(string documentId)
    {
        await _httpClient.DeleteAsync(
            $"{_baseUrl}/documents/{documentId}"
        );
    }

    public async Task<List<ChunkInfo>> GetChunks(
    string documentId)
    {
        return await _httpClient.GetFromJsonAsync<List<ChunkInfo>>(
            $"{_baseUrl}/documents/{documentId}/chunks"
        ) ?? new();
    }
}