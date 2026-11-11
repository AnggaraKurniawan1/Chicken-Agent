"""Inti agent: loop pesan -> tool -> hasil, dengan eksekusi tool paralel."""
import json
from concurrent.futures import ThreadPoolExecutor

import anthropic

from . import tools
from .config import DATA_DIR, MAX_HISTORY_TURNS, MAX_TOKENS, MAX_TOOL_ROUNDS, MODEL
from .personas import MODES


class Agent:
    def __init__(self, mode: str = "assistant", confirm=None):
        self.client = anthropic.Anthropic()  # baca ANTHROPIC_API_KEY dari env
        self.confirm = confirm or (lambda prompt: input(f"{prompt} [y/N] ").strip().lower() == "y")
        self.messages: list[dict] = []
        self.mode = ""
        self.set_mode(mode)

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
        # Simpan hanya giliran teks biasa agar file kecil dan aman dibaca ulang
        plain = []
        for m in self.messages:
            if isinstance(m["content"], str):
                plain.append(m)
            elif m["role"] == "assistant":
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

    # ----- satu giliran percakapan -----
    def ask(self, user_text: str, on_text=print) -> str:
        """Kirim pesan user, jalankan loop tool, kembalikan teks jawaban akhir."""
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

            if resp.stop_reason == "pause_turn":  # web_search di sisi server masih lanjut
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
