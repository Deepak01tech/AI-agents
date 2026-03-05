function ChatMessage({ role, content }) {
  return (
    <div style={{ margin: "10px 0" }}>
      <strong>{role === "user" ? "You" : "Bot"}:</strong>
      <p>{content}</p>
    </div>
  );
}

export default ChatMessage;