import { useState } from "react";
import axios from "axios";

export default function Dashboard() {
  const [file, setFile] = useState(null);
  const [portion, setPortion] = useState("medium");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [preview, setPreview] = useState(null);

  // 💬 CHAT STATE
  const [chatOpen] = useState(true);
  const [messages, setMessages] = useState([
    { role: "bot", text: "Hi 👋 I’m Caloriq AI. Ask me anything about food & calories!" }
  ]);
  const [input, setInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);

  // ==========================
  // IMAGE → CALORIE PREDICTION
  // ==========================
  const handlePredict = async () => {
    if (!file) {
      alert("Please upload an image first");
      return;
    }

    setLoading(true);
    setResults([]);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("portion", portion);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/predict",
        formData
      );
      setResults(res.data.top_predictions || []);
    } catch (err) {
      console.error(err);
      alert("Prediction failed. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  // ==========================
  // 💬 REAL GEMINI CHAT
  // ==========================
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setChatLoading(true);

    const formData = new FormData();
    formData.append("message", userMsg.text);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/chat",
        formData
      );

      setMessages(prev => [
        ...prev,
        { role: "bot", text: res.data.reply }
      ]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [
        ...prev,
        { role: "bot", text: "❌ AI not responding right now." }
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-slate-900 to-indigo-950 text-white p-8 flex flex-col items-center gap-10">

      {/* TITLE */}
      <h1 className="text-4xl font-bold tracking-wide">
        🍽️ <span className="text-indigo-400">Caloriq</span>
      </h1>

      {/* IMAGE CARD */}
      <div className="bg-white/10 backdrop-blur-xl p-6 rounded-2xl w-full max-w-xl shadow-xl animate-glow">
        <input
          type="file"
          accept="image/*"
          onChange={(e) => {
            setFile(e.target.files[0]);
            setPreview(URL.createObjectURL(e.target.files[0]));
          }}
          className="mb-4"
        />

        {preview && (
          <img
            src={preview}
            className="rounded-xl mb-4 max-h-60 mx-auto"
            alt="preview"
          />
        )}

        <select
          className="w-full p-2 rounded-lg bg-black/40 mb-4"
          value={portion}
          onChange={(e) => setPortion(e.target.value)}
        >
          <option value="small">Small</option>
          <option value="medium">Medium</option>
          <option value="large">Large</option>
        </select>

        <button
          onClick={handlePredict}
          className="w-full py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg font-semibold"
        >
          {loading ? "Analyzing..." : "Predict Calories"}
        </button>
      </div>

      {/* RESULTS */}
      {results.length > 0 && (
        <div className="max-w-xl w-full space-y-4">
          {results.map((r, i) => (
            <div key={i} className="bg-slate-900/80 p-4 rounded-xl shadow-lg">
              <div className="flex justify-between">
                <h3 className="capitalize font-bold">🍽️ {r.food}</h3>
                <span className="text-purple-400 font-bold">
                  {r.calories} kcal
                </span>
              </div>
              <div className="mt-2 text-sm text-gray-400">
                Confidence: {Math.round(r.confidence * 100)}%
              </div>
            </div>
          ))}
        </div>
      )}

      {/* 💬 CHAT UI */}
      {chatOpen && (
        <div className="fixed bottom-6 right-6 w-80 bg-slate-900 border border-purple-500/30 rounded-xl shadow-xl flex flex-col">

          <div className="p-3 border-b border-purple-500/20 font-semibold text-purple-300">
            🤖 Caloriq AI
          </div>

          <div className="flex-1 p-3 space-y-2 overflow-y-auto max-h-64">
            {messages.map((m, i) => (
              <div
                key={i}
                className={`p-2 rounded-lg text-sm max-w-[80%]
                  ${m.role === "user"
                    ? "bg-indigo-600 ml-auto"
                    : "bg-slate-700"
                  }`}
              >
                {m.text}
              </div>
            ))}

            {chatLoading && (
              <div className="bg-slate-700 p-2 rounded-lg text-sm w-fit">
                🤖 Thinking...
              </div>
            )}
          </div>

          <div className="p-2 flex gap-2 border-t border-purple-500/20">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about calories..."
              className="flex-1 px-2 py-1 rounded bg-black/40 text-sm outline-none"
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            />
            <button
              onClick={sendMessage}
              className="px-3 bg-purple-600 rounded text-sm"
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
