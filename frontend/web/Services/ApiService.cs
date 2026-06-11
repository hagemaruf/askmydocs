using System.Net.Http.Json;
using System.Text.Json;

namespace AskMyDocs.Web.Services;

public class ApiService
{
    private readonly HttpClient _httpClient;

    public ApiService(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<string> AskQuestion(string question)
    {
        var response = await _httpClient.PostAsJsonAsync(
            "http://127.0.0.1:8000/chat",
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
}