"""Knowledge Base, Alur Pengerjaan (Workflows), dan Direktori Link untuk Chicken-Agent.
Terinspirasi dari router pintar (bansos-router) untuk memberikan panduan detail langkah demi langkah
dan pencarian tautan referensi terpercaya.
"""

# Direktori tautan referensi terpercaya
LINK_DIRECTORY = [
    {
        "category": "WhatsApp & Chatbot Infrastructure",
        "title": "Baileys WhatsApp Web API (GitHub)",
        "url": "https://github.com/WhiskeySockets/Baileys",
        "description": "Library TypeScript/Node.js untuk integrasi WhatsApp Web protocol tanpa browser.",
        "tags": ["whatsapp", "baileys", "bot", "chat", "wa"]
    },
    {
        "category": "WhatsApp & Chatbot Infrastructure",
        "title": "Bansos Router Reference Repo",
        "url": "https://github.com/noura-nis/bansos-router",
        "description": "Contoh arsitektur bot WhatsApp Baileys + Telegram + Local AI Router dan FAQ matching.",
        "tags": ["bansos-router", "contoh", "router", "arsitektur", "wa"]
    },
    {
        "category": "WhatsApp & Chatbot Infrastructure",
        "title": "Telegram BotFather Official Guide",
        "url": "https://core.telegram.org/bots/tutorial",
        "description": "Panduan resmi pembuatan bot Telegram dan mendapatkan token BotFather.",
        "tags": ["telegram", "botfather", "bot", "token"]
    },
    {
        "category": "AI Models & API Consoles",
        "title": "Anthropic Claude Console",
        "url": "https://console.anthropic.com/",
        "description": "Portal API Key resmi untuk model Claude (Sonnet, Opus, Haiku).",
        "tags": ["anthropic", "claude", "api key", "ai", "token"]
    },
    {
        "category": "AI Models & API Consoles",
        "title": "Google AI Studio (Gemini API)",
        "url": "https://aistudio.google.com/",
        "description": "Dapatkan API Key Google Gemini secara gratis untuk integrasi AI cepat.",
        "tags": ["gemini", "google", "api key", "gratis", "free"]
    },
    {
        "category": "AI Models & API Consoles",
        "title": "Groq Cloud Console (Ultra Fast LLM)",
        "url": "https://console.groq.com/",
        "description": "API inference berkecepatan tinggi gratis untuk Llama 3, Mixtral, dan DeepSeek.",
        "tags": ["groq", "llama", "fast", "api", "gratis"]
    },
    {
        "category": "Deploy & Hosting",
        "title": "Railway Deployment Platform",
        "url": "https://railway.com/",
        "description": "Platform hosting cloud instan untuk menjalankan Node.js / Python bot 24/7.",
        "tags": ["deploy", "hosting", "cloud", "railway", "server"]
    },
    {
        "category": "Deploy & Hosting",
        "title": "Render Cloud Application Hosting",
        "url": "https://render.com/",
        "description": "Hosting gratis/murah untuk web service, bot, dan background workers.",
        "tags": ["deploy", "hosting", "render", "docker"]
    },
    {
        "category": "Riset & Tugas Akhir IT",
        "title": "Google Scholar (Pencarian Jurnal Ilmiah)",
        "url": "https://scholar.google.com/",
        "description": "Pencarian publikasi akademis, jurnal IT, prosiding IEEE, dan referensi skripsi.",
        "tags": ["skripsi", "jurnal", "riset", "scholar", "tugas akhir", "literatur"]
    },
    {
        "category": "Riset & Tugas Akhir IT",
        "title": "Hugging Face Models & Datasets",
        "url": "https://huggingface.co/",
        "description": "Gudang model open-source machine learning, NLP, computer vision, dan dataset penelitian.",
        "tags": ["dataset", "machine learning", "ai", "model", "nlp", "cnn", "huggingface"]
    },
    {
        "category": "Riset & Tugas Akhir IT",
        "title": "Kaggle Datasets & Notebooks",
        "url": "https://www.kaggle.com/datasets",
        "description": "Koleksi dataset publik untuk eksperimen machine learning, klasifikasi, dan prediksi.",
        "tags": ["kaggle", "dataset", "data", "ml", "python"]
    },
    {
        "category": "Peternakan & Smart Farming",
        "title": "FAO Poultry Production Guide",
        "url": "https://www.fao.org/poultry-production-products/production/en/",
        "description": "Panduan standar internasional FAO untuk manajemen pemeliharaan unggas dan ayam.",
        "tags": ["ayam", "peternakan", "poultry", "chicken", "broiler", "layer", "fao"]
    }
]

# Database Alur Pengerjaan Lengkap
WORKFLOWS = {
    "buat-agent-bot": {
        "id": "buat-agent-bot",
        "title": "Alur Pengerjaan Pembuatan AI Agent & Bot (WhatsApp / Telegram / Web)",
        "summary": "Panduan langkah demi langkah membangun bot cerdas seperti bansos-router dari nol hingga online.",
        "steps": [
            {
                "step": 1,
                "title": "Perencanaan & Penentuan Arsitektur",
                "details": (
                    "- Tentukan peran agen (misal: Customer Service, Konsultan Skripsi, Asisten Peternakan).\n"
                    "- Pilih kanal antarmuka: Web UI (akses lokal/browser), Telegram (mudah via BotFather), atau WhatsApp (Baileys/Meta Cloud API).\n"
                    "- Tentukan LLM engine: Anthropic Claude, Google Gemini, Groq, atau Router hybrid lokal."
                ),
                "tips": "Gunakan pendekatan Hybrid Router (seperti bansos-router): cek rule/FAQ lokal dulu sebelum lempar ke LLM untuk hemat kuota API."
            },
            {
                "step": 2,
                "title": "Persiapan Environment & Kunci API",
                "details": (
                    "- Buat file konfigurasi `.env` dari `.env.example`.\n"
                    "- Dapatkan API key dari provider pilihan (misal: https://aistudio.google.com/ untuk Gemini gratis, atau https://console.anthropic.com/ untuk Claude).\n"
                    "- Install dependensi yang dibutuhkan (Python: `pip install -r requirements.txt`, Node.js: `npm install`)."
                ),
                "tips": "Jangan pernah commit file `.env` ke GitHub publik."
            },
            {
                "step": 3,
                "title": "Implementasi Rule Engine & Prompt Persona",
                "details": (
                    "- Definisikan system prompt yang tegas: batasan peran, gaya bahasa (ramah, to-the-point), dan basis data wajib.\n"
                    "- Buat rule-based matcher untuk pertanyaan umum (alamat, harga, alur, kontak) sehingga bot langsung menjawab cepat tanpa delay LLM.\n"
                    "- Siapkan tool-calling: kalkulator, pencari file, pengingat tugas, atau pencarian web."
                ),
                "tips": "Format jawaban dengan poin-poin tebal dan sertakan link tujuan agar pengguna mudah bertindak."
            },
            {
                "step": 4,
                "title": "Koneksi ke Kanal (WhatsApp / Telegram / Web)",
                "details": (
                    "- **Web UI**: Jalankan server web lokal (`python main.py --web`) untuk interaksi langsung di browser.\n"
                    "- **Telegram**: Gunakan `@BotFather` di Telegram untuk membuat bot, dapatkan Token HTTP API, lalu jalankan polling worker.\n"
                    "- **WhatsApp**: Gunakan Baileys untuk pairing code nomor WA atau Meta Cloud API untuk nomor resmi bisnis."
                ),
                "tips": "Untuk WhatsApp Baileys, pastikan folder sesi (`.wa_auth`) tersimpan di penyimpanan persisten."
            },
            {
                "step": 5,
                "title": "Pengujian, Rate Limiting & Deployment",
                "details": (
                    "- Uji coba penanganan kesalahan (fallback) jika API down atau kuota habis.\n"
                    "- Terapkan cooldown per user (misal: jeda 10-15 detik antar pesan) untuk mencegah spam.\n"
                    "- Deploy ke server cloud (Railway, Render, VPS, atau SnapDeploy) agar bot aktif 24 jam."
                ),
                "tips": "Cek log server secara berkala untuk memantau waktu respons dan error token."
            }
        ],
        "links": [
            {"title": "Bansos Router Reference", "url": "https://github.com/noura-nis/bansos-router"},
            {"title": "Baileys WhatsApp Library", "url": "https://github.com/WhiskeySockets/Baileys"},
            {"title": "Telegram Bot API Docs", "url": "https://core.telegram.org/bots/api"},
            {"title": "Google AI Studio", "url": "https://aistudio.google.com/"}
        ]
    },
    "skripsi-it-ai": {
        "id": "skripsi-it-ai",
        "title": "Alur Pengerjaan Skripsi / Tugas Akhir IT & Machine Learning",
        "summary": "Metodologi terstruktur pengerjaan penelitian Informatika / Sistem Informasi dari Bab 1 hingga Sidang.",
        "steps": [
            {
                "step": 1,
                "title": "Penetapan Topik, Rumusan Masalah & Studi Literatur (Bab 1 & 2)",
                "details": (
                    "- Cari gap penelitian dari minimal 10-15 jurnal bereputasi 3 tahun terakhir di Google Scholar / IEEE.\n"
                    "- Formulasikan rumusan masalah yang terukur (misal: 'Bagaimana akurasi model YOLOv8 dalam deteksi penyakit ayam?').\n"
                    "- Susun latar belakang dengan piramida terbalik: kondisi ideal -> fakta lapangan -> solusi yang diajukan."
                ),
                "tips": "Pastikan dataset tersedia sebelum memfinalisasi judul proposal."
            },
            {
                "step": 2,
                "title": "Pengumpulan & Preprocessing Dataset (Bab 3)",
                "details": (
                    "- Ambil dataset dari sumber terpercaya (Kaggle, HuggingFace, atau pengambilan data primer di lapangan).\n"
                    "- Lakukan pembersihan data: handling missing values, normalisasi, augmentasi gambar (untuk citra), atau tokenisasi (untuk teks NLP).\n"
                    "- Bagi data menjadi Train, Validation, dan Test set (misal: 70:15:15 atau 80:20)."
                ),
                "tips": "Dokumentasikan setiap tahap preprocessing ke dalam diagram alur metodologi penelitian."
            },
            {
                "step": 3,
                "title": "Perancangan Sistem & Coding Model / Aplikasi (Bab 3 & 4)",
                "details": (
                    "- Rancang arsitektur sistem: UML (Use Case, Activity Diagram), ERD, atau diagram arsitektur neural network.\n"
                    "- Implementasikan model menggunakan Python (PyTorch, TensorFlow, Scikit-Learn) atau backend web (FastAPI/Laravel).\n"
                    "- Lakukan hyperparameter tuning (learning rate, batch size, epoch, optimizer) untuk mencari performa optimal."
                ),
                "tips": "Gunakan Git untuk version control dan simpan checkpoint model terbaik (.pt, .h5, .onnx)."
            },
            {
                "step": 4,
                "title": "Evaluasi & Analisis Hasil (Bab 4)",
                "details": (
                    "- Hitung metrik evaluasi standar: Confusion Matrix, Accuracy, Precision, Recall, F1-Score, atau mAP.\n"
                    "- Buat grafik visualisasi performa model (Loss curve, ROC-AUC, perbandingan antar algoritma).\n"
                    "- Berikan interpretasi ilmiah terhadap hasil: mengapa model berhasil atau mengalami salah klasifikasi."
                ),
                "tips": "Bahas error analysis (kasus di mana model salah memprediksi) untuk memperkuat nilai analisis skripsi."
            },
            {
                "step": 5,
                "title": "Kesimpulan, Turnitin & Persiapan Simulasi Sidang (Bab 5)",
                "details": (
                    "- Tarik kesimpulan yang menjawab rumusan masalah di Bab 1 secara langsung.\n"
                    "- Lakukan uji Turnitin (target kesamaan di bawah 20-25% sesuai panduan kampus).\n"
                    "- Buat slide presentasi yang visual (hindari teks berparagraf panjang) dan latihan simulasi tanya-jawab sidang."
                ),
                "tips": "Gunakan mode 'interviewer' pada Chicken-Agent untuk latihan simulasi pertanyaan penguji sidang!"
            }
        ],
        "links": [
            {"title": "Google Scholar", "url": "https://scholar.google.com/"},
            {"title": "Kaggle Datasets", "url": "https://www.kaggle.com/datasets"},
            {"title": "Hugging Face Datasets", "url": "https://huggingface.co/datasets"}
        ]
    },
    "manajemen-peternakan-ayam": {
        "id": "manajemen-peternakan-ayam",
        "title": "Alur Manajemen & SOP Pemeliharaan Ayam (Broiler & Layer)",
        "summary": "Alur operasional budidaya ayam modern dari persiapan kandang (chick-in) hingga panen.",
        "steps": [
            {
                "step": 1,
                "title": "Persiapan Kandang & Biosecurity Pra Chick-In",
                "details": (
                    "- Cuci dan semprot kandang dengan desinfektan minimal 14 hari masa istirahat kandang.\n"
                    "- Taburkan sekam padi (litter) setebal 8-10 cm dan pasang pemanas (brooder) 3-4 jam sebelum DOC tiba.\n"
                    "- Siapkan air minum bercampur gula merah/elektrolit untuk pemulihan energi anak ayam (DOC)."
                ),
                "tips": "Suhu ideal masa brooding (hari 1-3) adalah 33°C - 35°C dengan kelembapan 60-70%."
            },
            {
                "step": 2,
                "title": "Fase Starter (Hari 1 s.d. 14)",
                "details": (
                    "- Berikan pakan starter berprotein tinggi (minimal 21-23% protein kasar).\n"
                    "- Berikan vaksinasi wajib: ND-IB (tetes mata/air minum hari ke-4) dan Gumboro (hari ke-10-12).\n"
                    "- Pelebaran sekat brooding secara bertahap setiap 2-3 hari mengikuti pertumbuhan bobot DOC."
                ),
                "tips": "Pantau tembolok DOC 24 jam pertama: minimal 95% DOC harus sudah terisi pakan dan air."
            },
            {
                "step": 3,
                "title": "Fase Finisher & Manajemen Pakan (Hari 15 s.d. Panen)",
                "details": (
                    "- Transisi ke pakan finisher secara bertahap (campuran 3:1, 1:1, 1:3 selama 3 hari).\n"
                    "- Hitung FCR (Feed Conversion Ratio) mingguan = Total Pakan Dihabiskan (kg) / Total Bobot Ayam (kg).\n"
                    "- Atur sirkulasi ventilasi (blower / curtain) untuk membuang gas amonia kandang."
                ),
                "tips": "Target FCR broiler modern adalah di kisaran 1.4 - 1.6 pada umur panen 30-35 hari."
            },
            {
                "step": 4,
                "title": "Deteksi Dini Penyakit & Pengendalian",
                "details": (
                    "- Perhatikan konsistensi feses: feses berdarah (gejala Koksidiosis), feses hijau/putih kapur (ND/Pullorum).\n"
                    "- Amati suara pernapasan pada malam hari (waspadai CRD/ngorok).\n"
                    "- Pisahkan (karantina) ayam yang lemas atau kerdil ke petak khusus perawatan."
                ),
                "tips": "Cegah stress panas (heat stress) dengan pemberian vitamin C dan es batu di toren air saat siang terik."
            },
            {
                "step": 5,
                "title": "Pemanenan & Evaluasi Indeks Performa (IP)",
                "details": (
                    "- Puasakan makan 6-8 jam sebelum panen (tetap beri air minum) untuk menghindari kotoran berlebih saat pemotongan.\n"
                    "- Timbang sampel acak dan catat persentase deplesi (mortalitas).\n"
                    "- Hitung Indeks Performa (IP) = (Persentase Hidup x Bobot Rata-rata (kg)) / (Umur Panen x FCR) x 100."
                ),
                "tips": "Nilai IP di atas 350 dikategorikan performa peternakan sangat baik."
            }
        ],
        "links": [
            {"title": "Panduan Pemeliharaan Unggas FAO", "url": "https://www.fao.org/poultry-production-products/production/en/"}
        ]
    }
}


def search_knowledge(query: str) -> dict:
    """Mencari alur pengerjaan dan tautan berdasarkan kata kunci (keyword router)."""
    q = query.lower().strip()
    words = [w for w in q.split() if len(w) > 2]

    # 1. Cek pencocokan workflow
    matched_workflows = []
    for wf_id, wf in WORKFLOWS.items():
        score = 0
        text_corpus = (wf["title"] + " " + wf["summary"] + " " + wf_id).lower()
        for w in words:
            if w in text_corpus:
                score += 1
        if score > 0 or any(kw in q for kw in ["alur", "langkah", "cara", "tahap", "step", "proses", "sop"]):
            # Cek kecocokan tema spesifik
            if ("bot" in q or "agent" in q or "wa" in q or "telegram" in q) and wf_id == "buat-agent-bot":
                matched_workflows.append((10, wf))
            elif ("skripsi" in q or "tugas akhir" in q or "sidang" in q or "koding" in q or "riset" in q) and wf_id == "skripsi-it-ai":
                matched_workflows.append((10, wf))
            elif ("ayam" in q or "ternak" in q or "broiler" in q or "kandang" in q or "doc" in q or "fcr" in q) and wf_id == "manajemen-peternakan-ayam":
                matched_workflows.append((10, wf))
            elif score > 0:
                matched_workflows.append((score, wf))

    matched_workflows.sort(key=lambda x: x[0], reverse=True)

    # 2. Cek pencocokan tautan (links)
    matched_links = []
    for item in LINK_DIRECTORY:
        score = 0
        tag_str = " ".join(item["tags"])
        for w in words:
            if w in tag_str or w in item["title"].lower() or w in item["description"].lower():
                score += 1
        if score > 0:
            matched_links.append((score, item))

    matched_links.sort(key=lambda x: x[0], reverse=True)

    top_wf = matched_workflows[0][1] if matched_workflows else None
    top_links = [item for _, item in matched_links[:6]]

    return {
        "workflow": top_wf,
        "links": top_links
    }


def format_workflow_response(wf: dict) -> str:
    """Memformat data alur pengerjaan menjadi teks Markdown yang mudah dibaca dan detail."""
    lines = [
        f"### 📋 {wf['title']}",
        f"*{wf['summary']}*\n",
        "---",
        "#### 🧭 Tahapan Alur Pengerjaan:"
    ]
    for step in wf["steps"]:
        lines.append(f"\n**Langkah {step['step']}: {step['title']}**")
        lines.append(step["details"])
        lines.append(f"> 💡 **Tips Praktis:** {step['tips']}")

    if wf.get("links"):
        lines.append("\n---")
        lines.append("#### 🔗 Tautan & Referensi Terkait:")
        for l in wf["links"]:
            lines.append(f"- [{l['title']}]({l['url']})")

    return "\n".join(lines)


def format_links_response(links: list) -> str:
    """Memformat daftar tautan ke teks Markdown."""
    if not links:
        return "Tidak ditemukan tautan spesifik yang cocok. Silakan coba kata kunci lain."
    lines = ["#### 🔗 Tautan & Direktori Referensi yang Ditemukan:"]
    for l in links:
        lines.append(f"- **[{l['title']}]({l['url']})** (`{l['category']}`)\n  _{l['description']}_")
    return "\n".join(lines)
