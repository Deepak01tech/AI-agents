import { useState } from "react";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";
import { submitTraining } from "../api/trainingApi";

function Home() {
  const [messages, setMessages] = useState([]);

  const handleSend = async (text) => {
    const userMessage = { role: "user", content: text };

    setMessages((prev) => [...prev, userMessage]);

    const response = await submitTraining({
      level: "beginner",
      submission: text,
    });

    const botMessage = {
      role: "bot",
      content: response.reply || JSON.stringify(response),
    };

    setMessages((prev) => [...prev, botMessage]);
  };

  return (
    <div>
      <h2>Training Agent Chat</h2>

      <ChatWindow messages={messages} />

      <ChatInput onSend={handleSend} />
    </div>
  );
}

export default Home;