"""CLI & Web Runner untuk Chicken-Agent.

Contoh pemakaian:
    python main.py                  # CLI interaktif (Workflow & Asisten)
    python main.py --web            # Buka Web UI interaktif di browser
    python main.py --mode coding    # CLI mode coding

Perintah di dalam chat CLI:
    /mode <nama>   ganti mode (workflow, assistant, chat, research, coding, interviewer)
    /modes         lihat daftar mode
    /end           (pewawancara) akhiri sesi dan minta umpan balik
    /reset         hapus riwayat mode saat ini
    /quit          keluar
"""
import argparse
import os
import sys

from chicken_agent import MODES, Agent


def main():
    parser = argparse.ArgumentParser(description="Chicken-Agent - Workflow & AI Assistant")
    parser.add_argument("--mode", default="workflow", choices=list(MODES), help="Mode awal agent")
    parser.add_argument("--web", action="store_true", help="Jalankan Web UI interaktif di browser")
    parser.add_argument("--port", type=int, default=5050, help="Port untuk Web UI")
    args = parser.parse_args()

    if args.web:
        import web_ui
        web_ui.run_web(port=args.port, auto_open=True)
        return

    agent = Agent(args.mode)
    print("\n" + "="*60)
    print(f"🐔 Chicken-Agent | Mode: {agent.mode} ({agent.cfg['label']})")
    print(f"   Provider: {agent.provider.upper()}")
    if agent.provider == "local_knowledge":
        print("   💡 Info: Berjalan dalam Mode Knowledge & Workflow Router.")
        print("      (Alur pengerjaan, panduan, pencarian link & tool lokal siap digunakan)")
        print("      Untuk integrasi AI generatif bebas, isi ANTHROPIC_API_KEY atau GEMINI_API_KEY di .env")
    print("   Ketik /modes untuk daftar mode, /quit untuk keluar")
    print("   Atau jalankan: python main.py --web untuk antarmuka web di browser")
    print("="*60 + "\n")

    # Pewawancara membuka sesi lebih dulu
    if agent.mode == "interviewer" and not agent.messages:
        agent.ask("Mulai sesi wawancara.", on_text=print)
        print()

    while True:
        try:
            text = input("\nKamu: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not text:
            continue

        if text == "/quit":
            break
        if text == "/modes":
            print("\nDaftar Mode:")
            for k, v in MODES.items():
                active = " (aktif)" if k == agent.mode else ""
                print(f"  {k:12} : {v['label']}{active}")
            continue
        if text.startswith("/mode"):
            parts = text.split()
            if len(parts) != 2 or parts[1] not in MODES:
                print("Pakai: /mode <" + "|".join(MODES) + ">")
                continue
            agent.set_mode(parts[1])
            print(f"Mode berganti ke: {agent.mode} ({agent.cfg['label']})")
            if agent.mode == "interviewer" and not agent.messages:
                agent.ask("Mulai sesi wawancara.", on_text=print)
                print()
            continue
        if text == "/reset":
            agent.reset()
            print("Riwayat mode ini dihapus.")
            continue
        if text == "/end":
            text = ("Akhiri sesi sekarang dan berikan umpan balik lengkap."
                    if agent.mode == "interviewer" else "Rangkum percakapan ini.")

        print("\nChicken: ", end="")
        try:
            agent.ask(text, on_text=print)
        except Exception as e:
            print(f"\n[error] {type(e).__name__}: {e}")
        print()


if __name__ == "__main__":
    main()
