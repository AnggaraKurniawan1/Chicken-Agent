"""Integrasi Database Cloud Supabase untuk Chicken-Agent.
Menyimpan riwayat chat, tugas (tasks), dan catatan (notes) langsung di cloud Supabase
sehingga data tidak perlu disimpan di disk/laptop lokal.
"""
import json
import os
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env", override=True)
except ImportError:
    pass


def _get_url() -> str:
    return os.getenv("SUPABASE_URL", "").rstrip("/")


def _get_key() -> str:
    return os.getenv("SUPABASE_KEY", "") or os.getenv("SUPABASE_ACCESS_TOKEN", "")


def is_enabled() -> bool:
    """Cek apakah konfigurasi Supabase aktif."""
    url = _get_url()
    key = _get_key()
    return bool(url and key and (key.startswith("eyJ") or key.startswith("sbp_") or key.startswith("sb_")))


def _request(path: str, method: str = "GET", data: dict | list = None, params: str = ""):
    """Kirim request ke Supabase PostgREST API."""
    if not is_enabled():
        return None

    url = f"{_get_url()}/rest/v1/{path}"
    if params:
        url += f"?{params}"

    key = _get_key()
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content) if content else []
    except Exception as e:
        # Fallback graceful jika jaringan bermasalah
        return None


# ==================== TASKS ====================
def add_task(title: str, due: str = "") -> dict | None:
    res = _request("chicken_tasks", method="POST", data={"title": title, "done": False})
    if res and isinstance(res, list):
        return res[0]
    return None


def list_tasks(only_open: bool = True) -> list[dict] | None:
    params = "order=id.asc"
    if only_open:
        params += "&done=eq.false"
    res = _request("chicken_tasks", method="GET", params=params)
    return res if isinstance(res, list) else None


def complete_task(task_id: int) -> bool:
    res = _request("chicken_tasks", method="PATCH", data={"done": True}, params=f"id=eq.{task_id}")
    return bool(res)


# ==================== NOTES ====================
def save_note(text: str, tag: str = "") -> bool:
    res = _request("chicken_notes", method="POST", data={"text": text, "tag": tag})
    return bool(res)


def search_notes(query: str) -> list[dict] | None:
    # Filter text / tag via ilike
    params = f"or=(text.ilike.*{query}*,tag.ilike.*{query}*)&order=created_at.desc&limit=20"
    res = _request("chicken_notes", method="GET", params=params)
    return res if isinstance(res, list) else None


# ==================== CHAT HISTORY ====================
def load_history(mode: str) -> list[dict] | None:
    params = f"mode=eq.{mode}&order=created_at.asc&limit=40"
    res = _request("chicken_chat_history", method="GET", params=params)
    if isinstance(res, list):
        return [{"role": r["role"], "content": r["content"]} for r in res]
    return None


def save_history(mode: str, messages: list[dict]) -> bool:
    """Hapus chat lama mode ini lalu simpan turn terbaru di Supabase."""
    if not is_enabled():
        return False

    # Ambil 40 pesan teks terakhir
    plain = []
    for m in messages[-40:]:
        role = m.get("role", "")
        content = m.get("content", "")
        if isinstance(content, str) and content.strip():
            plain.append({"mode": mode, "role": role, "content": content})

    if not plain:
        return True

    try:
        # Bersihkan pesan lama mode ini lalu insert batch
        _request("chicken_chat_history", method="DELETE", params=f"mode=eq.{mode}")
        res = _request("chicken_chat_history", method="POST", data=plain)
        return bool(res)
    except Exception:
        return False


def reset_history(mode: str) -> bool:
    res = _request("chicken_chat_history", method="DELETE", params=f"mode=eq.{mode}")
    return res is not None
