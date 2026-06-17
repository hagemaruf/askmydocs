namespace AskMyDocs.Web.Models;

public class ChunkInfo
{
    public int Page { get; set; }

    public int Chunk { get; set; }

    public string Content { get; set; } = "";
}