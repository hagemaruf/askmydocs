using Microsoft.AspNetCore.Components.Forms;
using System.Net.Http.Headers;

namespace AskMyDocs.Web.Services;

public class UploadService
{
    private readonly HttpClient _http;

    public UploadService(HttpClient http)
    {
        _http = http;
    }

    public async Task<bool> UploadPdf(
        IBrowserFile file)
    {
        using var content =
            new MultipartFormDataContent();

        using var stream =
            file.OpenReadStream(
                maxAllowedSize:
                20 * 1024 * 1024);

        using var fileContent =
            new StreamContent(stream);

        fileContent.Headers.ContentType =
            new MediaTypeHeaderValue(
                "application/pdf");

        content.Add(
            fileContent,
            "file",
            file.Name);

        var response =
            await _http.PostAsync(
                "http://127.0.0.1:8000/upload",
                content);

        return response.IsSuccessStatusCode;
    }
}