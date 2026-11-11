"""Inti agent: loop pesan -> tool -> hasil, dengan dukungan Knowledge Router,
Multi-Provider LLM (Anthropic Claude, Gemini/OpenAI-compatible), dan Local Fallback.
"""
import json
import os
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from . import tools
from .config import DATA_DIR, MAX_HISTORY_TURNS, MAX_TOKENS, MAX_TOOL_ROUNDS, MODEL
from .knowledge import format_links_response, format_workflow_response, search_knowledge
from .personas import MODES


class Agent:
    def __init__(self, mode: str = "workflow", confirm=None):
        self.confirm = confirm or (lambda prompt: input(f"{prompt} [y/N] ").strip().lower() == "y")
        self.messages: list[dict] = []
        self.mode = ""
        self.client = None
        self.provider = "none"

        # Cek provider LLM yang tersedia
        self._init_llm_client()
        self.set_mode(mode)

    def _init_llm_client(self):
        """Inisialisasi client LLM sesuai API key yang tersedia."""
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        openai_key = os.getenv("OPENAI_API_KEY", "").strip()
        openai_base = os.getenv("OPENAI_BASE_URL", "").strip()

        if anthropic_key and anthropic_key != "isi_api_key_kamu_di_sini":
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=anthropic_key)
                self.provider = "anthropic"
                return
            except Exception as e:
                print(f"[warning] Gagal inisialisasi Anthropic client: {e}")

        if gemini_key and gemini_key != "isi_gemini_api_key_di_sini":
            self.provider = "gemini"
            return

        if openai_key or openai_base:
            self.provider = "openai"
            return

        self.provider = "local_knowledge"

    # ----- mode & riwayat -----
    def set_mode(self, mode: str):
        if mode not in MODES:
            raise ValueError(f"Mode tidak dikenal: {mode}. Pilihan: {', '.join(MODES)}")
        self.mode = mode
        self.cfg = MODES[mode]
        self.messages = self._load_history()

    @property
    def _history_file(self):
        return DATA_DIR / f"history_{self.mode}.json"

    def _load_history(self):
        if self._history_file.exists():
            try:
                return json.loads(self._history_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        return []

    def _save_history(self):
        plain = []
        for m in self.messages:
            if isinstance(m.get("content"), str):
                plain.append(m)
            elif m.get("role") == "assistant" and isinstance(m.get("content"), list):
                text = "".join(getattr(b, "text", "") for b in m["content"] if getattr(b, "type", "") == "text")
                if text:
                    plain.append({"role": "assistant", "content": text})
        self._history_file.write_text(
            json.dumps(plain[-MAX_HISTORY_TURNS:], ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def reset(self):
        self.messages = []
        self._history_file.unlink(missing_ok=True)

    # ----- eksekusi tool -----
    def _run_tool_calls(self, blocks):
        """Jalankan tool_use secara paralel; yang butuh konfirmasi dijalankan satu-satu."""
        results = {}
        parallel = [b for b in blocks if b.name not in tools.NEEDS_CONFIRM]
        serial = [b for b in blocks if b.name in tools.NEEDS_CONFIRM]

        if parallel:
            with ThreadPoolExecutor(max_workers=min(8, len(parallel))) as pool:
                for b, out in zip(parallel, pool.map(lambda b: tools.execute(b.name, b.input), parallel)):
                    results[b.id] = out
        for b in serial:
            print(f"\n[tool] {b.name}({json.dumps(b.input, ensure_ascii=False)})")
            if self.confirm(f"Izinkan menjalankan {b.name}?"):
                results[b.id] = tools.execute(b.name, b.input)
            else:
                results[b.id] = "Ditolak oleh user."

        return [
            {"type": "tool_result", "tool_use_id": b.id, "content": results[b.id]}
            for b in blocks
        ]

    # ----- respons mandiri / local fallback (bansos-router style) -----
    def _handle_local_query(self, user_text: str) -> str:
        """Menangani pertanyaan alur pengerjaan, link, atau tool lokal tanpa butuh external LLM API."""
        t = user_text.lower().strip()

        # 1. Cek query alur pengerjaan atau pembuatan sistem
        k_res = search_knowledge(user_text)
        is_asking_workflow = any(w in t for w in [
            "alur", "cara", "langkah", "tahap", "step", "gimana", "proses", "sop",
            "ingin membuat", "membuat", "bikin", "membangun", "arsitektur", "dashboard",
            "laravel", "vue", "super admin", "admin", "role", "sistem"
        ])
        is_asking_links = any(w in t for w in ["link", "tautan", "url", "daftar link", "minta link", "cari link"]) and not is_asking_workflow

        if (is_asking_workflow or k_res["workflow"]) and k_res["workflow"]:
            return format_workflow_response(k_res["workflow"])

        if is_asking_links and k_res["links"]:
            return format_links_response(k_res["links"])

        # 2. Cek perintah to-do / tasks
        if "tugas" in t or "todo" in t or "to-do" in t:
            if "tambah" in t or "buat" in t:
                title = user_text.replace("tambah tugas", "").replace("buat tugas", "").strip()
                return tools.add_task(title or "Tugas Baru")
            return tools.list_tasks(only_open=False)

        # 3. Cek catatan
        if "catat" in t or "simpan catatan" in t:
            note = user_text.replace("catat", "").replace("simpan catatan", "").strip()
            return tools.save_note(note or "Catatan Baru")
        if "cari catatan" in t:
            q = user_text.replace("cari catatan", "").strip()
            return tools.search_notes(q)

        # 4. Waktu
        if "jam" in t or "waktu" in t or "tanggal" in t:
            return f"🕒 Waktu saat ini: {tools.get_current_time()}"

        # 5. Fallback panduan
        return (
            "Halo! Saya **Chicken-Agent** (Mode Knowledge & Workflow Router). 🐔\n\n"
            "Saya dapat membantu menjelaskan secara detail:\n"
            "1. 🤖 **Alur Pembuatan AI Agent / Bot** (WhatsApp, Telegram, Web UI seperti bansos-router)\n"
            "2. 🎓 **Alur Skripsi & Riset IT** (Metodologi, Dataset, Modeling AI, Bab 1-5, Simulasi Sidang)\n"
            "3. 🐔 **Alur Manajemen Peternakan Ayam** (SOP Broiler/Layer, FCR, Pakan & Vaksinasi)\n"
            "4. 🔗 **Pencarian Informasi & Link Referensi** (Kaggle, GitHub Baileys, Google AI Studio, dll.)\n\n"
            "*Tips:* Tanyakan misalnya: *'Bagaimana alur pengerjaan pembuatan bot WhatsApp?'* atau *'Cari link referensi AI'*.\n\n"
            "> [!NOTE]\n"
            "> Untuk mengaktifkan percakapan AI generatif tak terbatas, Anda dapat menambahkan `ANTHROPIC_API_KEY` atau `GEMINI_API_KEY` pada file `.env`."
        )

    # ----- call Gemini / OpenAI-compatible via urllib (stdlib) -----
    def _call_openai_compatible(self, user_text: str, on_text=print) -> str:
        """Panggil endpoint OpenAI-compatible (Gemini, Groq, atau local server)."""
        gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        openai_key = os.getenv("OPENAI_API_KEY", "").strip()
        base_url = os.getenv("OPENAI_BASE_URL", "").strip()

        if self.provider == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
            api_key = gemini_key
            model_name = os.getenv("CHICKEN_MODEL", "gemini-2.5-flash")
        else:
            url = f"{base_url.rstrip('/')}/chat/completions" if base_url else "https://api.openai.com/v1/chat/completions"
            api_key = openai_key
            model_name = os.getenv("CHICKEN_MODEL", "gpt-4o-mini")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Format percakapan
        chat_msgs = [{"role": "system", "content": self.cfg["system"]}]
        for m in self.messages[-10:]:
            if isinstance(m.get("content"), str):
                chat_msgs.append({"role": m["role"], "content": m["content"]})
        chat_msgs.append({"role": "user", "content": user_text})

        payload = {
            "model": model_name,
            "messages": chat_msgs,
            "max_tokens": MAX_TOKENS,
            "temperature": 0.7
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                reply = data["choices"][0]["message"]["content"]
                on_text(reply)
                self.messages.append({"role": "user", "content": user_text})
                self.messages.append({"role": "assistant", "content": reply})
                self._save_history()
                return reply
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            err_msg = f"[API Error {e.code}]: {err_body}"
            print(err_msg)
            return self._handle_local_query(user_text)
        except Exception as e:
            print(f"[Error]: {e}")
            return self._handle_local_query(user_text)

    # ----- satu giliran percakapan -----
    def ask(self, user_text: str, on_text=print) -> str:
        """Kirim pesan user, jalankan loop tool / knowledge matcher, kembalikan teks jawaban."""
        # 1. Prioritaskan Knowledge Router untuk query alur pengerjaan dan solusi pembuatan sistem
        t_low = user_text.lower()
        k_res = search_knowledge(user_text)
        is_workflow_trigger = any(w in t_low for w in [
            "alur", "tahap", "sop", "cara", "langkah", "ingin membuat", "membuat",
            "bikin", "rancang", "membangun", "dashboard", "laravel", "vue",
            "super admin", "admin", "skripsi", "bot", "ayam", "role"
        ])
        if k_res["workflow"] and is_workflow_trigger:
            reply = format_workflow_response(k_res["workflow"])
            on_text(reply)
            self.messages.append({"role": "user", "content": user_text})
            self.messages.append({"role": "assistant", "content": reply})
            self._save_history()
            return reply

        # 2. Jika provider adalah Anthropic Claude
        if self.provider == "anthropic" and self.client:
            self.messages.append({"role": "user", "content": user_text})
            final_text = ""

            for _ in range(MAX_TOOL_ROUNDS):
                with self.client.messages.stream(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    system=self.cfg["system"],
                    tools=tools.tool_specs(self.cfg["tools"]),
                    messages=self.messages,
                ) as stream:
                    for chunk in stream.text_stream:
                        on_text(chunk, end="", flush=True)
                    resp = stream.get_final_message()

                self.messages.append({"role": "assistant", "content": resp.content})
                final_text = "".join(b.text for b in resp.content if b.type == "text")

                if resp.stop_reason == "pause_turn":
                    continue
                if resp.stop_reason != "tool_use":
                    break

                calls = [b for b in resp.content if b.type == "tool_use"]
                if not calls:
                    break
                print()
                for c in calls:
                    print(f"[tool] {c.name}")
                self.messages.append({"role": "user", "content": self._run_tool_calls(calls)})
            else:
                on_text("\n[batas putaran tool tercapai]", end="", flush=True)

            self._save_history()
            return final_text

        # 3. Jika provider adalah Gemini atau OpenAI-compatible
        if self.provider in ("gemini", "openai"):
            return self._call_openai_compatible(user_text, on_text=on_text)

        # 4. Fallback ke Local Knowledge Engine (selalu bisa diakses tanpa API key)
        reply = self._handle_local_query(user_text)
        on_text(reply)
        self.messages.append({"role": "user", "content": user_text})
        self.messages.append({"role": "assistant", "content": reply})
        self._save_history()
        return reply
