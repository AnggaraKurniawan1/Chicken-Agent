"""Tool lokal untuk agent. Setiap tool = skema (untuk Claude) + fungsi Python."""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from .config import DATA_DIR, WORKSPACE_DIR
from .knowledge import format_links_response, format_workflow_response, search_knowledge
from . import supabase_db

TASKS_FILE = DATA_DIR / "tasks.json"
NOTES_FILE = DATA_DIR / "notes.json"


# ---------- util ----------
def _load(path: Path):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
    return []


def _save(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _safe_path(rel: str) -> Path:
    """Pastikan path tetap di dalam workspace/."""
    p = (WORKSPACE_DIR / rel).resolve()
    if WORKSPACE_DIR.resolve() not in p.parents and p != WORKSPACE_DIR.resolve():
        raise ValueError("Path di luar workspace tidak diizinkan.")
    return p


# ---------- implementasi tool ----------
def get_current_time() -> str:
    return datetime.now().astimezone().strftime("%A, %d %B %Y, %H:%M %Z (UTC%z)")


def add_task(title: str, due: str = "") -> str:
    if supabase_db.is_enabled():
        res = supabase_db.add_task(title, due)
        if res:
            return f"Tugas #{res['id']} ditambahkan ke Supabase Cloud: {title}"

    tasks = _load(TASKS_FILE)
    new_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({"id": new_id, "title": title, "due": due, "done": False})
    _save(TASKS_FILE, tasks)
    return f"Tugas #{new_id} ditambahkan: {title} (tenggat: {due or 'tidak ada'})"


def list_tasks(only_open: bool = True) -> str:
    if supabase_db.is_enabled():
        tasks = supabase_db.list_tasks(only_open=only_open)
        if tasks is not None:
            if not tasks:
                return "Tidak ada tugas di Supabase Cloud."
            return "\n".join(
                f"#{t['id']} [{'x' if t.get('done') else ' '}] {t['title']} (Cloud)"
                for t in tasks
            )

    tasks = _load(TASKS_FILE)
    if only_open:
        tasks = [t for t in tasks if not t["done"]]
    if not tasks:
        return "Tidak ada tugas."
    return "\n".join(
        f"#{t['id']} [{'x' if t['done'] else ' '}] {t['title']}"
        + (f" (tenggat {t['due']})" if t.get("due") else "")
        for t in tasks
    )


def complete_task(task_id: int) -> str:
    if supabase_db.is_enabled():
        ok = supabase_db.complete_task(task_id)
        if ok:
            return f"Tugas #{task_id} ditandai selesai di Supabase Cloud."

    tasks = _load(TASKS_FILE)
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            _save(TASKS_FILE, tasks)
            return f"Tugas #{task_id} ditandai selesai."
    return f"Tugas #{task_id} tidak ditemukan."


def save_note(text: str, tag: str = "") -> str:
    if supabase_db.is_enabled():
        ok = supabase_db.save_note(text, tag)
        if ok:
            return "Catatan berhasil disimpan ke Supabase Cloud."

    notes = _load(NOTES_FILE)
    notes.append({"time": datetime.now().isoformat(timespec="seconds"), "tag": tag, "text": text})
    _save(NOTES_FILE, notes)
    return "Catatan disimpan."


def search_notes(query: str) -> str:
    if supabase_db.is_enabled():
        hits = supabase_db.search_notes(query)
        if hits is not None:
            if not hits:
                return "Tidak ada catatan di Supabase Cloud yang cocok."
            return "\n".join(f"[{h.get('created_at', '')[:19]}] ({h.get('tag', '')}) {h['text']}" for h in hits)

    q = query.lower()
    hits = [n for n in _load(NOTES_FILE) if q in n["text"].lower() or q in n["tag"].lower()]
    if not hits:
        return "Tidak ada catatan yang cocok."
    return "\n".join(f"[{n['time']}] ({n['tag']}) {n['text']}" for n in hits[-10:])


def list_files(subdir: str = ".") -> str:
    base = _safe_path(subdir)
    if not base.exists():
        return "Folder tidak ada."
    items = sorted(p.relative_to(WORKSPACE_DIR).as_posix() + ("/" if p.is_dir() else "")
                   for p in base.rglob("*"))
    return "\n".join(items[:200]) or "(kosong)"


def read_file(path: str) -> str:
    p = _safe_path(path)
    if not p.is_file():
        return "File tidak ditemukan."
    text = p.read_text(encoding="utf-8", errors="replace")
    return text[:20000] + ("\n...[dipotong]" if len(text) > 20000 else "")


def write_file(path: str, content: str) -> str:
    p = _safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"Ditulis: {path} ({len(content)} karakter)"


def run_python(path: str, timeout: int = 30) -> str:
    p = _safe_path(path)
    if not p.is_file():
        return "File tidak ditemukan."
    try:
        r = subprocess.run(
            [sys.executable, "-I", str(p)],
            cwd=WORKSPACE_DIR, capture_output=True, text=True, timeout=min(timeout, 60),
        )
    except subprocess.TimeoutExpired:
        return "Dihentikan: melebihi batas waktu."
    out = (r.stdout + ("\n[stderr]\n" + r.stderr if r.stderr else "")).strip()
    return f"exit code {r.returncode}\n{out[:8000]}"


def get_workflow(topic: str) -> str:
    """Ambil alur pengerjaan dan panduan detail berdasarkan topik (misal: bot, skripsi, ternak)."""
    res = search_knowledge(topic)
    if res["workflow"]:
        return format_workflow_response(res["workflow"])
    return f"Alur pengerjaan untuk '{topic}' belum terdaftar secara spesifik. Cobalah kata kunci: 'bot', 'skripsi', atau 'ternak ayam'."


def search_links(query: str) -> str:
    """Cari tautan, repositori referensi, dan dokumentasi terkait topik."""
    res = search_knowledge(query)
    if res["links"]:
        return format_links_response(res["links"])
    return f"Tidak ditemukan tautan spesifik untuk kata kunci '{query}'."


def check_render_status() -> str:
    """Cek status akun dan layanan Render menggunakan RENDER_API_KEY."""
    from .config import RENDER_API_KEY
    if not RENDER_API_KEY:
        return "RENDER_API_KEY belum dikonfigurasi di file .env."
    try:
        import requests
        headers = {"Authorization": f"Bearer {RENDER_API_KEY}", "Accept": "application/json"}
        r = requests.get("https://api.render.com/v1/services?limit=10", headers=headers, timeout=10)
        if r.status_code == 200:
            services = r.json()
            if not services:
                return "Koneksi ke Render API sukses! Akun aktif (Belum ada service yang berjalan)."
            out = f"Koneksi ke Render API sukses! Ditemukan {len(services)} service:\n"
            for s in services:
                svc = s.get("service", {})
                out += f"- {svc.get('name')} ({svc.get('type')}) - Status: {svc.get('suspended')}\n"
            return out
        return f"Render API Error ({r.status_code}): {r.text}"
    except Exception as e:
        return f"Gagal menghubungi Render API: {e}"


def check_supabase_status() -> str:
    """Cek status akun dan project Supabase menggunakan SUPABASE_ACCESS_TOKEN."""
    from .config import SUPABASE_ACCESS_TOKEN
    if not SUPABASE_ACCESS_TOKEN:
        return "SUPABASE_ACCESS_TOKEN belum dikonfigurasi di file .env."
    try:
        import requests
        headers = {"Authorization": f"Bearer {SUPABASE_ACCESS_TOKEN}", "Accept": "application/json"}
        r = requests.get("https://api.supabase.com/v1/projects", headers=headers, timeout=10)
        if r.status_code == 200:
            projects = r.json()
            if not projects:
                return "Koneksi ke Supabase API sukses! Token valid (Belum ada project aktif)."
            out = f"Koneksi ke Supabase API sukses! Ditemukan {len(projects)} project:\n"
            for p in projects:
                out += f"- {p.get('name')} (ID: {p.get('id')}) - Region: {p.get('region')} - Status: {p.get('status')}\n"
            return out
        return f"Supabase API Error ({r.status_code}): {r.text}"
    except Exception as e:
        return f"Gagal menghubungi Supabase API: {e}"


# ---------- registry ----------
def _schema(name, desc, props=None, required=None):
    return {
        "name": name,
        "description": desc,
        "input_schema": {"type": "object", "properties": props or {}, "required": required or []},
    }


S = {"type": "string"}

TOOLS = {
    "get_current_time": (_schema("get_current_time", "Waktu dan tanggal saat ini."), get_current_time),
    "add_task": (_schema("add_task", "Tambah tugas baru ke daftar to-do.",
                         {"title": S, "due": {"type": "string", "description": "Tenggat, mis. 2026-11-12"}},
                         ["title"]), add_task),
    "list_tasks": (_schema("list_tasks", "Tampilkan daftar tugas.",
                           {"only_open": {"type": "boolean"}}), list_tasks),
    "complete_task": (_schema("complete_task", "Tandai tugas selesai berdasarkan id.",
                              {"task_id": {"type": "integer"}}, ["task_id"]), complete_task),
    "save_note": (_schema("save_note", "Simpan catatan.", {"text": S, "tag": S}, ["text"]), save_note),
    "search_notes": (_schema("search_notes", "Cari di catatan tersimpan.", {"query": S}, ["query"]), search_notes),
    "list_files": (_schema("list_files", "Daftar file di workspace.", {"subdir": S}), list_files),
    "read_file": (_schema("read_file", "Baca file di workspace.", {"path": S}, ["path"]), read_file),
    "write_file": (_schema("write_file", "Tulis/timpa file di workspace.",
                           {"path": S, "content": S}, ["path", "content"]), write_file),
    "run_python": (_schema("run_python", "Jalankan file Python di workspace (butuh konfirmasi user).",
                           {"path": S, "timeout": {"type": "integer"}}, ["path"]), run_python),
    "get_workflow": (_schema("get_workflow", "Ambil panduan alur pengerjaan terperinci langkah demi langkah untuk topik tertentu.",
                             {"topic": S}, ["topic"]), get_workflow),
    "search_links": (_schema("search_links", "Cari direktori tautan dan link dokumentasi/repositori penting.",
                             {"query": S}, ["query"]), search_links),
    "check_render_status": (_schema("check_render_status", "Cek koneksi dan status akun hosting Render."), check_render_status),
    "check_supabase_status": (_schema("check_supabase_status", "Cek koneksi dan project database Supabase."), check_supabase_status),
}

# Tool yang dieksekusi server Anthropic (tidak perlu kode lokal)
SERVER_TOOLS = {
    "web_search": {"type": "web_search_20250305", "name": "web_search", "max_uses": 5},
}

# Tool yang wajib minta konfirmasi sebelum dijalankan
NEEDS_CONFIRM = {"run_python"}


def tool_specs(names):
    specs = []
    for n in names:
        if n in SERVER_TOOLS:
            specs.append(SERVER_TOOLS[n])
        elif n in TOOLS:
            specs.append(TOOLS[n][0])
    return specs


def execute(name: str, args: dict) -> str:
    if name not in TOOLS:
        return f"Tool tidak dikenal: {name}"
    try:
        return str(TOOLS[name][1](**args))
    except Exception as e:  # kembalikan error ke Claude agar bisa memperbaiki
        return f"Error: {type(e).__name__}: {e}"
