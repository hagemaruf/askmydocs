namespace AskMyDocs.Web.Models;

public class DocumentInfo
{
    public string Document_Id { get; set; } = "";

    public string Filename { get; set; } = "";

    public string Uploaded_At { get; set; } = "";

    public int Chunks { get; set; }
}