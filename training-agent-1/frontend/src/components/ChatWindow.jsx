import ChatMessage from "./ChatMessage";

function ChatWindow({ messages }) {
  return (
    <div style={{ border: "1px solid gray", padding: "10px", height: "300px", overflowY: "auto" }}>
      {messages.map((msg, index) => (
        <ChatMessage key={index} role={msg.role} content={msg.content} />
      ))}
    </div>
  );
}

export default ChatWindow;