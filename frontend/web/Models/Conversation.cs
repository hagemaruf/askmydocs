namespace AskMyDocs.Web.Models;

public class Conversation
{
    public Guid Id { get; set; }
        = Guid.NewGuid();

    public string Title { get; set; }
        = "New Chat";

    public List<ChatMessage> Messages
    { get; set; } = new();
}