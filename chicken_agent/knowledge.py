"""Knowledge Base, Alur Pengerjaan (Workflows), dan Direktori Link untuk Chicken-Agent.
Terinspirasi dari router pintar (bansos-router) untuk memberikan panduan detail langkah demi langkah
dan pencarian tautan referensi terpercaya.
"""

# Direktori tautan referensi terpercaya
LINK_DIRECTORY = [
    # Laravel & Vue.js Fullstack Ecosystem
    {
        "category": "Web Development & Frameworks",
        "title": "Laravel Official Documentation (v11/v12)",
        "url": "https://laravel.com/docs",
        "description": "Dokumentasi resmi framework PHP Laravel: Routing, Middleware, Authentication, Eloquent ORM, dan Events.",
        "tags": ["laravel", "php", "backend", "framework", "api", "dashboard", "admin"]
    },
    {
        "category": "Web Development & Frameworks",
        "title": "Vue.js 3 Official Guide & Documentation",
        "url": "https://vuejs.org/guide/introduction.html",
        "description": "Panduan resmi Vue 3 Composition API, Reactive State, dan SFC (Single File Components).",
        "tags": ["vue", "vuejs", "vue3", "frontend", "javascript", "spa", "dashboard"]
    },
    {
        "category": "Web Development & Frameworks",
        "title": "Inertia.js - The Modern Monolith",
        "url": "https://inertiajs.com/",
        "description": "Jembatan penghubung tanpa API rumit antara backend Laravel dan frontend Vue.js.",
        "tags": ["inertia", "inertiajs", "laravel", "vue", "fullstack", "monolith"]
    },
    {
        "category": "Web Development & Frameworks",
        "title": "Spatie Laravel Permission (Role & Permissions)",
        "url": "https://spatie.be/docs/laravel-permission/v6/introduction",
        "description": "Paket standar industri untuk manajemen Multi-Role (Super Admin, Admin, User) dan hak akses di Laravel.",
        "tags": ["spatie", "permission", "role", "roles", "super admin", "admin", "rbac", "laravel"]
    },
    {
        "category": "Web Development & Frameworks",
        "title": "Laravel Reverb (Realtime WebSocket Server)",
        "url": "https://laravel.com/docs/reverb",
        "description": "Server WebSocket bawaan Laravel berkecepatan tinggi untuk notifikasi realtime antar user dan admin.",
        "tags": ["reverb", "websocket", "realtime", "notifikasi", "broadcast", "laravel", "terhubung"]
    },
    {
        "category": "Web Development & Frameworks",
        "title": "Tailwind CSS Documentation",
        "url": "https://tailwindcss.com/docs",
        "description": "Framework CSS utility-first untuk membangun antarmuka dashboard admin yang modern dan responsif.",
        "tags": ["tailwind", "css", "ui", "dashboard", "styling"]
    },

    # WhatsApp & Chatbot
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

    # AI Models & API
    {
        "category": "AI Frameworks & Harness",
        "title": "DeepSeek Harness (GitHub)",
        "url": "https://github.com/deepseek-ai/deepseek-harness",
        "description": "Framework harness agent open-source resmi DeepSeek dengan arsitektur 'Everything is a Plugin' dan Web UI.",
        "tags": ["deepseek", "harness", "dsh", "deepseek-harness", "agent", "cordis", "plugin"]
    },
    {
        "category": "AI Models & API Consoles",
        "title": "DeepSeek Open Platform (API Key)",
        "url": "https://platform.deepseek.com/",
        "description": "Portal API resmi DeepSeek untuk mengakses model DeepSeek-V3 dan DeepSeek-R1 (OpenAI-compatible).",
        "tags": ["deepseek", "deepseek-v3", "deepseek-r1", "api key", "ai", "llm"]
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
        "title": "Anthropic Claude Console",
        "url": "https://console.anthropic.com/",
        "description": "Portal API Key resmi untuk model Claude (Sonnet, Opus, Haiku).",
        "tags": ["anthropic", "claude", "api key", "ai", "token"]
    },
    {
        "category": "AI Models & API Consoles",
        "title": "Groq Cloud Console (Ultra Fast LLM)",
        "url": "https://console.groq.com/",
        "description": "API inference berkecepatan tinggi gratis untuk Llama 3, Mixtral, dan DeepSeek.",
        "tags": ["groq", "llama", "fast", "api", "gratis"]
    },

    # Deploy & Hosting
    {
        "category": "Deploy & Hosting",
        "title": "Railway Deployment Platform",
        "url": "https://railway.com/",
        "description": "Platform hosting cloud instan untuk menjalankan Node.js / Python / Laravel bot 24/7.",
        "tags": ["deploy", "hosting", "cloud", "railway", "server"]
    },
    {
        "category": "Deploy & Hosting",
        "title": "Render Cloud Application Hosting",
        "url": "https://render.com/",
        "description": "Hosting gratis/murah untuk web service, bot, dan background workers.",
        "tags": ["deploy", "hosting", "render", "docker"]
    },

    # Riset & Tugas Akhir IT
    {
        "category": "Riset & Tugas Akhir IT",
        "title": "Google Scholar (Pencarian Jurnal Ilmiah)",
        "url": "https://scholar.google.com/",
        "description": "Pencarian publikasi akademis, jurnal IT, prosiding IEEE, dan referensi skripsi.",
        "tags": ["skripsi", "jurnal", "riset", "scholar", "tugas akhir", "literatur"]
    },
    {
        "category": "Riset & Tugas Akhir IT",
        "title": "Kaggle Datasets & Notebooks",
        "url": "https://www.kaggle.com/datasets",
        "description": "Koleksi dataset publik untuk eksperimen machine learning, klasifikasi, dan prediksi.",
        "tags": ["kaggle", "dataset", "data", "ml", "python"]
    },
    {
        "category": "Riset & Tugas Akhir IT",
        "title": "Hugging Face Models & Datasets",
        "url": "https://huggingface.co/",
        "description": "Gudang model open-source machine learning, NLP, computer vision, dan dataset penelitian.",
        "tags": ["dataset", "machine learning", "ai", "model", "nlp", "cnn", "huggingface"]
    },

    # Peternakan
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
    "laravel-vue-dashboard": {
        "id": "laravel-vue-dashboard",
        "title": "Alur Pengerjaan Website Dashboard Multi-Role (Super Admin, Admin, User) Laravel + Vue.js",
        "summary": "Panduan arsitektur dan langkah teknis membangun dashboard terintegrasi dengan Role-Based Access Control (RBAC), Inertia.js, dan komunikasi data antar-role.",
        "steps": [
            {
                "step": 1,
                "title": "Pemilihan Arsitektur & Stack (Inertia.js vs REST API)",
                "details": (
                    "- **Pilihan Utama (Direkomendasikan): Laravel 11 + Vue 3 + Inertia.js**.\n"
                    "  Menggunakan starter kit `Laravel Breeze` dengan opsi `--vue`. Inertia menghilangkan kebutuhan membuat API REST terpisah, routing langsung diarahkan dari Laravel controller ke komponen Vue.\n"
                    "- **Pilihan Alternatif: Laravel REST API + Vue 3 SPA (Vite + Pinia)**.\n"
                    "  Menggunakan Laravel Sanctum untuk autentikasi token Bearer dan Vue Router untuk navigasi frontend."
                ),
                "tips": "Untuk dashboard admin internal, gunakan stack Laravel + Inertia.js + Vue 3 karena proses development 3x lebih cepat tanpa pusing mengelola token di localStorage."
            },
            {
                "step": 2,
                "title": "Desain Database & Hak Akses (RBAC) dengan Spatie Permission",
                "details": (
                    "- Install paket manajemen role standar industri:\n"
                    "  `composer require spatie/laravel-permission`\n"
                    "- Buat 3 Role Utama di Seeder (`RoleSeeder.php`):\n"
                    "  1. `super_admin`: Hak akses mutlak (kelola Admin, kelola role, konfigurasi sistem, audit trail).\n"
                    "  2. `admin`: Hak akses operasional (verifikasi data user, input master data, kelola transaksi).\n"
                    "  3. `user`: Hak akses mandiri (input data pribadi, ajukan permohonan, lihat status dashboard sendiri).\n"
                    "- Terapkan relasi `HasRoles` trait pada model `App\\Models\\User`."
                ),
                "tips": "Gunakan seeder dengan `Role::firstOrCreate(['name' => 'super_admin'])` agar data awal otomatis terisi saat `php artisan migrate --seed`."
            },
            {
                "step": 3,
                "title": "Pembuatan Middleware & Proteksi Route di Laravel",
                "details": (
                    "- Buat route grouping di `routes/web.php` berdasarkan role:\n"
                    "  ```php\n"
                    "  Route::middleware(['auth', 'role:super_admin'])->prefix('super-admin')->group(function () {\n"
                    "      Route::get('/dashboard', [SuperAdminController::class, 'index'])->name('superadmin.dashboard');\n"
                    "      Route::resource('/manage-admins', AdminManagementController::class);\n"
                    "  });\n"
                    "  Route::middleware(['auth', 'role:admin|super_admin'])->prefix('admin')->group(function () {\n"
                    "      Route::get('/dashboard', [AdminController::class, 'index'])->name('admin.dashboard');\n"
                    "      Route::get('/users-list', [AdminController::class, 'users']);\n"
                    "  });\n"
                    "  Route::middleware(['auth', 'role:user'])->prefix('user')->group(function () {\n"
                    "      Route::get('/dashboard', [UserController::class, 'index'])->name('user.dashboard');\n"
                    "  });\n"
                    "  ```"
                ),
                "tips": "Pastikan middleware `'role' => \\Spatie\\Permission\\Middleware\\RoleMiddleware::class` didaftarkan di `bootstrap/app.php` (Laravel 11)."
            },
            {
                "step": 4,
                "title": "Perancangan Antarmuka Vue 3 & Sidebar Dinamis per Role",
                "details": (
                    "- Di middleware `HandleInertiaRequests.php`, bagikan data user beserta rolenya ke semua komponen Vue:\n"
                    "  ```php\n"
                    "  'auth' => [\n"
                    "      'user' => $request->user() ? array_merge($request->user()->toArray(), [\n"
                    "          'roles' => $request->user()->getRoleNames(),\n"
                    "          'permissions' => $request->user()->getAllPermissions()->pluck('name')\n"
                    "      ]) : null\n"
                    "  ]\n"
                    "  ```\n"
                    "- Di komponen Vue (`Sidebar.vue`), render menu secara kondisional:\n"
                    "  - Jika role memuat `super_admin`: tampilkan menu Master Admin, Log Aktivitas, Pengaturan Server.\n"
                    "  - Jika role memuat `admin`: tampilkan menu Validasi User, Laporan Rekap, Monitoring Harian.\n"
                    "  - Jika role memuat `user`: tampilkan menu Profil Saya, Pengajuan Permohonan, Riwayat Transaksi."
                ),
                "tips": "Buat helper function di Vue: `const hasRole = (role) => $page.props.auth.user.roles.includes(role)`."
            },
            {
                "step": 5,
                "title": "Mekanisme Saling Terhubung Antar-Role (Interkoneksi & Realtime)",
                "details": (
                    "Agar Super Admin, Admin, dan User **saling terhubung secara real-time**:\n"
                    "1. **Alur Notifikasi & Approval:**\n"
                    "   - User submit pengajuan/data -> Laravel Trigger Event `NewUserSubmission`.\n"
                    "   - Admin menerima notifikasi realtime dan tombol aksi 'Approve' / 'Reject'.\n"
                    "   - Hasil approval Admin otomatis memicu notifikasi balik ke Dashboard User.\n"
                    "   - Super Admin dapat memantau seluruh riwayat aksi (siapa yang menyetujui, jam berapa) di Audit Log.\n"
                    "2. **Teknologi Realtime:** Gunakan **Laravel Reverb** (bawaan Laravel 11) atau **Pusher** + **Laravel Echo** di Vue 3."
                ),
                "tips": "Kombinasikan Event Broadcasting dengan database notification table (`php artisan make:notification`) agar notifikasi tetap tersimpan saat pengguna offline."
            },
            {
                "step": 6,
                "title": "Pengujian Hak Akses, Keamanan & Deployment",
                "details": (
                    "- Uji coba skenario bypass URL: pastikan User biasa tidak bisa membuka `/admin/dashboard` (harus return 403 Forbidden).\n"
                    "- Pasang policy authorization pada controller (`$this->authorize(...)`) selain middleware route.\n"
                    "- Build asset frontend sebelum deploy: `npm run build`.\n"
                    "- Siapkan environment production: `php artisan config:cache`, `php artisan route:cache`, `php artisan view:cache`."
                ),
                "tips": "Gunakan database transaction `DB::transaction()` saat Super Admin membuat atau memutasi akun Admin dan User."
            }
        ],
        "links": [
            {"title": "Laravel 11 Documentation", "url": "https://laravel.com/docs"},
            {"title": "Vue.js 3 Composition API", "url": "https://vuejs.org/guide/introduction.html"},
            {"title": "Inertia.js Documentation", "url": "https://inertiajs.com/"},
            {"title": "Spatie Laravel Permission", "url": "https://spatie.be/docs/laravel-permission/v6/introduction"},
            {"title": "Laravel Reverb (WebSockets)", "url": "https://laravel.com/docs/reverb"}
        ]
    },
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

    # Cek kecocokan tema spesifik dengan bobot tinggi
    matched_workflows = []

    # 1. Laravel, Vue, Dashboard, PHP, Web Admin Multi-Role
    is_laravel_vue = any(k in q for k in ["laravel", "vue", "dashboard", "admin", "super admin", "rbac", "multi role", "php"])
    if is_laravel_vue:
        matched_workflows.append((20, WORKFLOWS["laravel-vue-dashboard"]))

    # 2. Bot WA / Telegram / Agent
    if any(k in q for k in ["bot", "agent", "wa", "telegram", "baileys", "whatsapp"]):
        matched_workflows.append((18, WORKFLOWS["buat-agent-bot"]))

    # 3. Skripsi IT / AI / Machine Learning
    if any(k in q for k in ["skripsi", "tugas akhir", "sidang", "jurnal", "riset", "koding", "dataset"]):
        matched_workflows.append((18, WORKFLOWS["skripsi-it-ai"]))

    # 4. Peternakan Ayam
    if any(k in q for k in ["ayam", "ternak", "broiler", "layer", "kandang", "doc", "fcr"]):
        matched_workflows.append((18, WORKFLOWS["manajemen-peternakan-ayam"]))

    # 5. Generic scoring terhadap text corpus
    for wf_id, wf in WORKFLOWS.items():
        if any(w[1]["id"] == wf_id for w in matched_workflows):
            continue
        score = 0
        text_corpus = (wf["title"] + " " + wf["summary"] + " " + wf_id).lower()
        for w in words:
            if w in text_corpus:
                score += 2
        if score > 0:
            matched_workflows.append((score, wf))

    matched_workflows.sort(key=lambda x: x[0], reverse=True)

    # 6. Pencocokan tautan (links) secara tepat
    matched_links = []
    for item in LINK_DIRECTORY:
        score = 0
        tag_str = " ".join(item["tags"]).lower()
        title_str = item["title"].lower()
        desc_str = item["description"].lower()

        # Prioritaskan jika kata spesifik cocok
        for w in words:
            # Hindari kata umum seperti 'dan', 'ini', 'web', 'dengan' yang memicu false positive
            if w in ["web", "dan", "yang", "untuk", "bisa", "dengan", "ingin", "buat", "saya", "pada", "saat"]:
                continue
            if w in tag_str:
                score += 3
            if w in title_str:
                score += 4
            if w in desc_str:
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
