# Chicken-Agent

Agent pribadi berbasis Claude dengan 5 mode:

| Mode | Fungsi |
|---|---|
| `assistant` | Asisten harian: tugas, catatan, tanggal, cari web |
| `chat` | Bot chat santai |
| `research` | Riset multi-sumber, bisa simpan laporan `.md` |
| `coding` | Tulis, baca, dan jalankan kode Python di `workspace/` |
| `interviewer` | Simulasi wawancara + umpan balik (`/end`) |

Tool yang independen dijalankan **paralel** (misalnya beberapa pencarian atau beberapa pembacaan file sekaligus).

## Cara pakai

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # lalu isi ANTHROPIC_API_KEY
python main.py --mode assistant
```

API key didapat dari https://console.anthropic.com. Jangan commit file `.env`.

## Perintah di dalam chat

- `/modes` daftar mode, `/mode coding` ganti mode
- `/end` mengakhiri sesi wawancara dan meminta umpan balik
- `/reset` hapus riwayat mode saat ini, `/quit` keluar

## Struktur

```
main.py                  CLI
chicken_agent/
  config.py              model, folder data & workspace
  personas.py            prompt dan daftar tool tiap mode
  tools.py               tool lokal (tugas, catatan, file, run_python)
  agent.py               loop agent + eksekusi tool paralel
data/                    tugas, catatan, riwayat (tidak di-commit)
workspace/               folder kerja aman untuk mode coding/riset
```

## Keamanan

- Operasi file dibatasi di `workspace/`.
- `run_python` selalu minta konfirmasi `y/N` sebelum jalan.
- Pencarian web memakai tool `web_search` dari Anthropic (pastikan aktif di akun API kamu).

## Menambah tool

1. Tulis fungsinya di `tools.py` dan daftarkan di dict `TOOLS`.
2. Tambahkan namanya ke `tools` pada mode yang diinginkan di `personas.py`.
