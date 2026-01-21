import { useState } from "react";
import axios from "axios";

export default function ChatBox() {
  const [msg, setMsg] = useState("");
  const [reply, setReply] = useState("");
  const [loading, setLoading] = useState(false);

  const askAI = async () => {
    if (!msg) return;
    setLoading(true);

    const form = new FormData();
    form.append("message", msg);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/chat",
        form
      );
      setReply(res.data.reply);
    } catch {
      setReply("❌ AI not responding");
    }

    setLoading(false);
  };

  return (
    <div className="mt-10 bg-black/40 backdrop-blur-xl p-4 rounded-xl max-w-xl w-full">
      <h2 className="text-lg font-semibold mb-2">💬 Ask Caloriq AI</h2>

      <input
        className="w-full p-2 rounded bg-black/60 mb-2"
        placeholder="Ask about diet, calories, health..."
        value={msg}
        onChange={(e) => setMsg(e.target.value)}
      />

      <button
        onClick={askAI}
        className="w-full bg-purple-600 py-2 rounded font-semibold"
      >
        {loading ? "Thinking..." : "Ask AI"}
      </button>

      {reply && (
        <div className="mt-3 text-sm text-purple-200">
          🤖 {reply}
        </div>
      )}
    </div>
  );
}
