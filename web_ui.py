"""Web UI Server untuk Chicken-Agent.
Menyediakan antarmuka web modern berbasis browser tanpa dependensi eksternal berat.
"""
import json
import os
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from chicken_agent import MODES, Agent

# Shared Agent instance
agent = Agent(mode="workflow")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chicken-Agent 🐔 | Workflow & AI Assistant</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {
      --bg: #0f172a;
      --card-bg: rgba(30, 41, 59, 0.7);
      --card-border: rgba(255, 255, 255, 0.08);
      --primary: #f59e0b;
      --primary-hover: #d97706;
      --accent: #38bdf8;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --bot-bubble: #1e293b;
      --user-bubble: #d97706;
      --code-bg: #0b1120;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: radial-gradient(circle at 10% 10%, #1e1b4b 0%, #0f172a 100%);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    header {
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--card-border);
      padding: 14px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 50;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-icon {
      font-size: 28px;
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.3);
      width: 44px;
      height: 44px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 12px;
    }

    .brand h1 {
      font-size: 18px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .brand p {
      font-size: 12px;
      color: var(--text-muted);
    }

    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: var(--accent);
      font-weight: 500;
    }

    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
    }

    main {
      flex: 1;
      max-width: 960px;
      width: 100%;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      padding: 16px 20px 24px;
      gap: 16px;
    }

    .toolbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
      padding: 10px 14px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
    }

    .mode-pills {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .mode-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: inherit;
    }

    .mode-btn:hover {
      background: rgba(255, 255, 255, 0.1);
      color: var(--text);
    }

    .mode-btn.active {
      background: var(--primary);
      color: #0f172a;
      border-color: var(--primary);
      font-weight: 600;
    }

    .reset-btn {
      background: transparent;
      border: 1px solid rgba(239, 68, 68, 0.3);
      color: #f87171;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 12px;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.2s;
    }

    .reset-btn:hover {
      background: rgba(239, 68, 68, 0.1);
    }

    .quick-chips {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 4px;
    }

    .chip {
      background: rgba(56, 189, 248, 0.08);
      border: 1px solid rgba(56, 189, 248, 0.2);
      color: #bae6fd;
      font-size: 12px;
      padding: 6px 12px;
      border-radius: 20px;
      white-space: nowrap;
      cursor: pointer;
      transition: all 0.2s;
    }

    .chip:hover {
      background: rgba(56, 189, 248, 0.2);
      border-color: var(--accent);
    }

    .chat-container {
      flex: 1;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 20px;
      overflow-y: auto;
      min-height: 440px;
      max-height: 60vh;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .message {
      display: flex;
      gap: 12px;
      max-width: 88%;
      animation: fadeIn 0.25s ease-out;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .message.user {
      align-self: flex-end;
      flex-direction: row-reverse;
    }

    .message.bot {
      align-self: flex-start;
    }

    .avatar {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      flex-shrink: 0;
    }

    .message.user .avatar {
      background: linear-gradient(135deg, #f59e0b, #d97706);
    }

    .message.bot .avatar {
      background: linear-gradient(135deg, #0284c7, #0369a1);
      border: 1px solid rgba(56, 189, 248, 0.4);
    }

    .bubble {
      padding: 12px 16px;
      border-radius: 14px;
      font-size: 14px;
      line-height: 1.6;
    }

    .message.user .bubble {
      background: var(--user-bubble);
      color: #fff;
      border-bottom-right-radius: 4px;
    }

    .message.bot .bubble {
      background: var(--bot-bubble);
      color: var(--text);
      border: 1px solid var(--card-border);
      border-bottom-left-radius: 4px;
    }

    .bubble p { margin-bottom: 8px; }
    .bubble p:last-child { margin-bottom: 0; }
    .bubble h3, .bubble h4 { margin: 12px 0 6px; color: #fbbf24; }
    .bubble ul, .bubble ol { margin: 8px 0 8px 20px; }
    .bubble li { margin-bottom: 4px; }
    .bubble code {
      font-family: 'JetBrains Mono', monospace;
      background: var(--code-bg);
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 12px;
      color: #38bdf8;
    }
    .bubble pre {
      background: var(--code-bg);
      border: 1px solid rgba(255, 255, 255, 0.1);
      padding: 12px;
      border-radius: 8px;
      overflow-x: auto;
      margin: 8px 0;
    }
    .bubble pre code { background: none; padding: 0; }
    .bubble blockquote {
      border-left: 3px solid var(--primary);
      padding-left: 10px;
      margin: 8px 0;
      color: #cbd5e1;
      font-style: italic;
    }
    .bubble a {
      color: var(--accent);
      text-decoration: underline;
    }

    .input-bar {
      display: flex;
      gap: 10px;
      position: relative;
    }

    .input-bar textarea {
      flex: 1;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 14px 18px;
      color: var(--text);
      font-family: inherit;
      font-size: 14px;
      resize: none;
      outline: none;
      height: 52px;
      line-height: 22px;
      transition: all 0.2s;
    }

    .input-bar textarea:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.2);
    }

    .send-btn {
      background: var(--primary);
      color: #0f172a;
      border: none;
      border-radius: 14px;
      padding: 0 24px;
      font-size: 15px;
      font-weight: 600;
      cursor: pointer;
      font-family: inherit;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .send-btn:hover {
      background: var(--primary-hover);
      transform: translateY(-1px);
    }

    .send-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }

    .typing-indicator {
      display: none;
      align-items: center;
      gap: 4px;
      padding: 8px 12px;
      background: var(--bot-bubble);
      border-radius: 12px;
      width: fit-content;
      border: 1px solid var(--card-border);
    }

    .typing-dot {
      width: 6px;
      height: 6px;
      background: var(--accent);
      border-radius: 50%;
      animation: bounce 1.4s infinite ease-in-out;
    }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes bounce {
      0%, 80%, 100% { transform: scale(0); }
      40% { transform: scale(1); }
    }
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <div class="brand-icon">🐔</div>
      <div>
        <h1>Chicken-Agent</h1>
        <p>Detail Workflows, Step-by-Step Guidance & Link Search</p>
      </div>
    </div>
    <div class="status-badge" id="providerBadge">
      <span class="status-dot"></span>
      <span id="providerText">Knowledge Engine Active</span>
    </div>
  </header>

  <main>
    <div class="toolbar">
      <div class="mode-pills" id="modePills">
        <!-- Injected via JS -->
      </div>
      <button class="reset-btn" onclick="resetChat()">Hapus Riwayat</button>
    </div>

    <div class="quick-chips">
      <div class="chip" onclick="sendPrompt('Bagaimana alur pembuatan website dashboard multi-role Admin, User, dan Super Admin dengan Laravel dan Vue.js?')">💻 Dashboard Laravel + Vue.js</div>
      <div class="chip" onclick="sendPrompt('Bagaimana alur pengerjaan pembuatan AI agent dan bot WhatsApp/Telegram?')">🤖 Alur Buat Bot</div>
      <div class="chip" onclick="sendPrompt('Jelaskan alur pengerjaan skripsi IT dari Bab 1 sampai sidang')">🎓 Alur Skripsi IT</div>
      <div class="chip" onclick="sendPrompt('Bagaimana alur manajemen peternakan ayam broiler dan hitung FCR?')">🐔 SOP Ternak Ayam</div>
      <div class="chip" onclick="sendPrompt('Cari link referensi AI, Baileys WhatsApp, dan jurnal ilmiah')">🔗 Cari Link & Referensi</div>
      <div class="chip" onclick="sendPrompt('Lihat daftar tugas saya')">📋 Cek Tugas</div>
    </div>

    <div class="chat-container" id="chatContainer">
      <div class="message bot">
        <div class="avatar">🐔</div>
        <div class="bubble">
          <p>Halo! Saya <strong>Chicken-Agent</strong>. 👋</p>
          <p>Saya dirancang untuk <strong>menjelaskan secara detail alur pengerjaan (step-by-step)</strong>, memberikan panduan praktis, dan membantu <strong>pencarian informasi serta tautan penting</strong> (seperti pada bansos-router).</p>
          <p>Pilih topik cepat di atas atau ketik pertanyaan apa saja di bawah!</p>
        </div>
      </div>
    </div>

    <div class="typing-indicator" id="typingIndicator">
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    </div>

    <div class="input-bar">
      <textarea id="userInput" placeholder="Tanyakan alur pengerjaan, cara kerja, atau cari link referensi... (Tekan Enter untuk mengirim)" rows="1" onkeydown="handleKeyDown(event)"></textarea>
      <button class="send-btn" id="sendBtn" onclick="sendMessage()">Kirim 🚀</button>
    </div>
  </main>

  <script>
    let currentMode = "workflow";
    const modesList = {
      "workflow": "Panduan Alur & Info",
      "assistant": "Asisten Harian",
      "chat": "Chat Santai",
      "research": "Riset",
      "coding": "Coding",
      "interviewer": "Pewawancara / Sidang"
    };

    function renderModes() {
      const container = document.getElementById("modePills");
      container.innerHTML = "";
      for (const [key, label] of Object.entries(modesList)) {
        const btn = document.createElement("button");
        btn.className = "mode-btn" + (key === currentMode ? " active" : "");
        btn.innerText = label;
        btn.onclick = () => switchMode(key);
        container.appendChild(btn);
      }
    }

    async function fetchInfo() {
      try {
        const res = await fetch("/api/info");
        const data = await res.json();
        currentMode = data.mode || "workflow";
        if (data.provider === "deepseek") {
          document.getElementById("providerText").innerText = "DeepSeek AI Connected 🐳";
        } else if (data.provider === "anthropic") {
          document.getElementById("providerText").innerText = "Claude AI Connected";
        } else if (data.provider === "gemini") {
          document.getElementById("providerText").innerText = "Gemini AI Connected";
        } else if (data.provider === "openai") {
          document.getElementById("providerText").innerText = "OpenAI Connected";
        } else {
          document.getElementById("providerText").innerText = "Knowledge Router Active (Offline/Fast)";
        }
        renderModes();
      } catch (e) {
        console.error("Info error:", e);
      }
    }

    async function switchMode(newMode) {
      currentMode = newMode;
      renderModes();
      try {
        await fetch("/api/mode", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ mode: newMode })
        });
        appendBotMessage(`*Beralih ke mode:* **${modesList[newMode]}**`);
      } catch (e) {
        console.error("Switch mode error:", e);
      }
    }

    async function resetChat() {
      if (!confirm("Hapus riwayat percakapan untuk mode ini?")) return;
      try {
        await fetch("/api/reset", { method: "POST" });
        document.getElementById("chatContainer").innerHTML = "";
        appendBotMessage("Riwayat percakapan telah dibersihkan.");
      } catch (e) {
        console.error("Reset error:", e);
      }
    }

    function appendUserMessage(text) {
      const container = document.getElementById("chatContainer");
      const msg = document.createElement("div");
      msg.className = "message user";
      msg.innerHTML = `
        <div class="avatar">👤</div>
        <div class="bubble">${escapeHtml(text)}</div>
      `;
      container.appendChild(msg);
      container.scrollTop = container.scrollHeight;
    }

    function appendBotMessage(markdown) {
      const container = document.getElementById("chatContainer");
      const msg = document.createElement("div");
      msg.className = "message bot";
      const htmlContent = marked.parse(markdown);
      msg.innerHTML = `
        <div class="avatar">🐔</div>
        <div class="bubble">${htmlContent}</div>
      `;
      container.appendChild(msg);
      container.scrollTop = container.scrollHeight;
    }

    function escapeHtml(string) {
      return String(string).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    function sendPrompt(text) {
      document.getElementById("userInput").value = text;
      sendMessage();
    }

    function handleKeyDown(e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    }

    async function sendMessage() {
      const input = document.getElementById("userInput");
      const text = input.value.trim();
      if (!text) return;

      appendUserMessage(text);
      input.value = "";
      input.style.height = "52px";

      const sendBtn = document.getElementById("sendBtn");
      const indicator = document.getElementById("typingIndicator");
      sendBtn.disabled = true;
      indicator.style.display = "flex";

      try {
        const res = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text, mode: currentMode })
        });
        const data = await res.json();
        appendBotMessage(data.reply || "Maaf, tidak ada jawaban.");
      } catch (e) {
        appendBotMessage(`[Error]: Tidak dapat terhubung ke server agent. (${e.message})`);
      } finally {
        sendBtn.disabled = false;
        indicator.style.display = "none";
      }
    }

    fetchInfo();
  </script>
</body>
</html>
"""


class AgentHttpHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/" or url.path == "/index.html":
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
        elif url.path == "/api/info":
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = {
                "mode": agent.mode,
                "provider": agent.provider,
                "modes": {k: v["label"] for k, v in MODES.items()}
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))
        elif url.path in ("/v1/models", "/api/models"):
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = {
                "object": "list",
                "data": [
                    {"id": "chicken-agent", "object": "model", "owned_by": "user"},
                    {"id": "workflow", "object": "model", "owned_by": "chicken-agent"},
                    {"id": "assistant", "object": "model", "owned_by": "chicken-agent"}
                ]
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))
        else:
            self.send_response(404)
            self._send_cors_headers()
            self.end_headers()

    def do_POST(self):
        url = urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {}

        if url.path == "/api/chat":
            msg = payload.get("message", "")
            mode = payload.get("mode")
            if mode and mode != agent.mode:
                try:
                    agent.set_mode(mode)
                except Exception:
                    pass

            reply = agent.ask(msg, on_text=lambda *a, **kw: None)

            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"reply": reply, "mode": agent.mode}).encode("utf-8"))

        elif url.path in ("/v1/chat/completions", "/api/v1/chat/completions"):
            # Standar OpenAI-compatible endpoint
            messages = payload.get("messages", [])
            user_msg = ""
            for m in reversed(messages):
                if isinstance(m, dict) and m.get("role") == "user":
                    user_msg = m.get("content", "")
                    break
            if not user_msg and messages and isinstance(messages[-1], dict):
                user_msg = messages[-1].get("content", "")

            req_model = payload.get("model", "")
            if req_model in MODES:
                try:
                    agent.set_mode(req_model)
                except Exception:
                    pass

            reply = agent.ask(user_msg, on_text=lambda *a, **kw: None)
            now = int(time.time())
            res = {
                "id": f"chatcmpl-chicken-{now}",
                "object": "chat.completion",
                "created": now,
                "model": agent.mode,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": reply
                        },
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": len(user_msg.split()),
                    "completion_tokens": len(reply.split()),
                    "total_tokens": len(user_msg.split()) + len(reply.split())
                }
            }
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

        elif url.path == "/api/mode":
            mode = payload.get("mode", "workflow")
            try:
                agent.set_mode(mode)
                res = {"status": "ok", "mode": agent.mode}
            except Exception as e:
                res = {"status": "error", "message": str(e)}

            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

        elif url.path == "/api/reset":
            agent.reset()
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))

        else:
            self.send_response(404)
            self._send_cors_headers()
            self.end_headers()

    def log_message(self, format, *args):
        # Hindari log berisik di terminal
        pass


def run_web(port: int = 5173, auto_open: bool = True):
    ThreadingHTTPServer.allow_reuse_address = True
    try:
        server = ThreadingHTTPServer(("127.0.0.1", port), AgentHttpHandler)
    except OSError as e:
        if getattr(e, "winerror", None) == 10048 or "10048" in str(e):
            print(f"\n=======================================================")
            print(f"🚀 Chicken-Agent sudah aktif di port {port}!")
            print(f"   EnvKit URL : http://chicken-agent.test")
            print(f"   Local URL  : http://127.0.0.1:{port}")
            print(f"   Menjaga dev-server EnvKit tetap berjalan...")
            print(f"=======================================================\n")
            try:
                while True:
                    time.sleep(5)
            except KeyboardInterrupt:
                return
        raise

    url = f"http://127.0.0.1:{port}"
    print(f"\n=======================================================")
    print(f"🚀 Chicken-Agent Web UI aktif!")
    print(f"   EnvKit URL : http://chicken-agent.test")
    print(f"   Local URL  : {url}")
    print(f"   Mode: {agent.mode} | Provider: {agent.provider}")
    print(f"   Tekan Ctrl+C di terminal ini untuk berhenti.")
    print(f"=======================================================\n")

    if auto_open:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nMenutup server web Chicken-Agent...")
        server.server_close()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5173"))
    auto_open = "--no-browser" not in sys.argv
    for arg in sys.argv[1:]:
        if arg.isdigit():
            port = int(arg)
    run_web(port=port, auto_open=auto_open)
