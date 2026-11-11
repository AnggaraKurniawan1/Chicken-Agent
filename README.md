# Chicken-Agent 🐔

Agent cerdas berbasis Python dengan fitur **Panduan Alur Pengerjaan (Workflow Engine)**, **Pencarian Informasi & Link Terpercaya**, serta dukungan **Multi-Provider AI** (Claude, Gemini, OpenAI) dan **Local Knowledge Mode** (terinspirasi dari router pintar [bansos-router](https://github.com/noura-nis/bansos-router)).

---

## 🌟 Fitur Utama

- **🧭 Panduan Alur Pengerjaan Step-by-Step:**
  - Alur Pembuatan AI Agent & Bot (WhatsApp Baileys, Telegram BotFather, deployment cloud).
  - Alur Pengerjaan Skripsi / Tugas Akhir IT & Machine Learning (Bab 1 s.d. 5, dataset, modeling, Turnitin, simulasi sidang).
  - SOP Manajemen Peternakan Ayam (Broiler & Layer, FCR, pakan, biosecurity, vaksinasi).
- **🔗 Direktori Tautan & Link Finder:**
  - Pencarian repositori GitHub, dokumentasi API, portal jurnal ilmiah (Google Scholar), dan platform AI gratis.
- **🖥️ Antarmuka Ganda (Web UI & CLI):**
  - **Web Dashboard:** Antarmuka web interaktif di browser (cukup jalankan `start_web.bat` atau `python main.py --web`).
  - **Terminal CLI:** Chat konsol interaktif cepat (`start_cli.bat` atau `python main.py`).
- **🛡️ Multi-Provider & Akses Mandiri (Bisa Diakses Tanpa API Key):**
  - Jika belum memiliki API key, agen tetap **100% dapat diakses** untuk konsultasi alur kerja, SOP, pencarian link, dan manajemen tugas/catatan lokal!
  - Mendukung **Anthropic Claude**, **Google Gemini** (gratis di AI Studio), atau **OpenAI/Groq**.

---

## 📋 Daftar Mode Agent

| Mode | Label | Fungsi |
|---|---|---|
| `workflow` *(default)* | Panduan Alur & Info | Menjelaskan alur pengerjaan terperinci, cara kerja, checklist, dan link referensi |
| `assistant` | Asisten Harian | Kelola tugas (to-do list), jadwal, pengingat, dan catatan |
| `chat` | Bot Chat Santai | Ngobrol santai, ramah, dan interaktif |
| `research` | Riset Multi-Sumber | Analisis multi-topik, perbandingan sumber, dan export laporan `.md` |
| `coding` | Asisten Coding | Baca, tulis kode di `workspace/`, dan verifikasi eksekusi Python |
| `interviewer` | Simulasi Wawancara | Simulasi tanya-jawab kerja / sidang tugas akhir + umpan balik komprehensif |

---

## 🚀 Cara Menjalankan

### Cara 1: Satu Klik di Windows
- Klik dua kali file **`start_web.bat`** untuk membuka Web UI di browser.
- Atau klik dua kali **`start_cli.bat`** untuk membuka di jendela CMD/PowerShell.

### Cara 2: Lewat Terminal

```bash
# 1. (Opsional) Buat dan aktifkan virtual environment
python -m venv .venv
.venv\Scripts\activate

# 2. Install dependensi
pip install -r requirements.txt

# 3. Jalankan Web UI
python main.py --web

# Atau jalankan CLI
python main.py --mode workflow
```

---

## ⚙️ Konfigurasi API Key (Opsional)

Jika ingin mengaktifkan percakapan AI generatif di luar database bawaan:

1. Salin `.env.example` menjadi `.env` (atau edit file `.env` yang sudah disediakan).
2. Isi salah satu API key berikut:
   - **Google Gemini (Gratis):** Dapatkan di [Google AI Studio](https://aistudio.google.com/) -> Masukkan ke `GEMINI_API_KEY`.
   - **Anthropic Claude:** Dapatkan di [Anthropic Console](https://console.anthropic.com/) -> Masukkan ke `ANTHROPIC_API_KEY`.
   - **OpenAI / Groq:** Masukkan ke `OPENAI_API_KEY`.

---

## 📂 Struktur Proyek

```
main.py                  # Runner CLI & Web UI
web_ui.py                # Server Web UI (browser)
start_web.bat            # Launcher Web UI Windows 1-klik
start_cli.bat            # Launcher CLI Windows 1-klik
chicken_agent/
  agent.py               # Otak agent (Knowledge Router + Multi-LLM loop)
  knowledge.py           # Database alur pengerjaan, direktori link & matcher
  personas.py            # Prompt persona & konfigurasi mode
  tools.py               # Tools lokal (tasks, notes, files, python runner, workflow lookup)
  config.py              # Konfigurasi path, env, dan limit
data/                    # Penyimpanan data tugas, catatan, dan riwayat chat (lokal)
workspace/               # Folder kerja aman untuk eksekusi kode / riset
```
