import { useState } from "react";
import { askQuestion } from "../api";
import Message from "./Message";

export default function ChatWindow({ sessionId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input) return;
    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await askQuestion(sessionId, input);
      const answer = res.answer || "No answer generated.";
      newMessages.push({ role: "assistant", content: answer });
      if (res.chart) {
        newMessages.push({
          role: "assistant",
          content: "📊 Chart generated below:",
        });
        newMessages.push({
          role: "assistant",
          content: (
            <img
              src={`data:image/png;base64,${res.chart}`}
              alt="chart"
              className="max-w-sm rounded-md"
            />
          ),
        });
      }
      setMessages([...newMessages]);
    } catch (err) {
      newMessages.push({
        role: "assistant",
        content: "⚠️ Error: " + err.message,
      });
      setMessages([...newMessages]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 border rounded-xl shadow-md bg-white flex flex-col h-full">
      <div className="flex-1 overflow-y-auto mb-4">
        {messages.map((msg, i) => (
          <Message key={i} role={msg.role} content={msg.content} />
        ))}
        {loading && <p className="text-gray-400">Thinking...</p>}
      </div>
      <div className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 border rounded-md px-3 py-2"
          placeholder="Ask a question..."
        />
        <button
          onClick={handleSend}
          className="px-4 py-2 bg-green-600 text-white rounded-md"
        >
          Send
        </button>
      </div>
    </div>
  );
}
