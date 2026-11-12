import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv

    # override=True: nilai di .env mengalahkan variabel lingkungan sistem yang usang
    load_dotenv(BASE_DIR / ".env", override=True)
except ImportError:
    pass

# Token bearer dari sistem (mis. sisa setelan Claude Code) membuat error
# "Invalid bearer token". Agent ini memakai ANTHROPIC_API_KEY saja jika pakai Anthropic.
os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)

DATA_DIR = BASE_DIR / "data"           # tugas, catatan, riwayat chat
WORKSPACE_DIR = BASE_DIR / "workspace"  # folder kerja aman untuk mode coding/riset

DATA_DIR.mkdir(exist_ok=True)
WORKSPACE_DIR.mkdir(exist_ok=True)

# Default model
MODEL = os.getenv("CHICKEN_MODEL", "deepseek-chat")
MAX_TOKENS = int(os.getenv("CHICKEN_MAX_TOKENS", "4096"))
MAX_TOOL_ROUNDS = 12     # batas putaran tool per satu pesan user
MAX_HISTORY_TURNS = 40   # jumlah pesan teks yang disimpan antar sesi

# Cloud Integrations (Render & Supabase)
RENDER_API_KEY = os.getenv("RENDER_API_KEY", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_ACCESS_TOKEN = os.getenv("SUPABASE_ACCESS_TOKEN", "")
