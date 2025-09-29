import { useState } from "react";
import FileUpload from "./components/FileUpload";
import ChatWindow from "./components/ChatWindow";

export default function App() {
  const [sessionId, setSessionId] = useState(null);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-6">
      <h1 className="text-2xl font-bold mb-4">📊 Excel Q&A Assistant</h1>
      {!sessionId ? (
        <FileUpload setSession={setSessionId} />
      ) : (
        <div className="w-full max-w-2xl h-[600px]">
          <ChatWindow sessionId={sessionId} />
        </div>
      )}
    </div>
  );
}
