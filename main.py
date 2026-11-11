"""CLI Chicken-Agent.

Contoh:
    python main.py                  # mulai di mode asisten harian
    python main.py --mode coding
Perintah di dalam chat:
    /mode <nama>   ganti mode (assistant, chat, research, coding, interviewer)
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
    parser = argparse.ArgumentParser(description="Chicken-Agent")
    parser.add_argument("--mode", default="assistant", choices=list(MODES))
    args = parser.parse_args()

    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY belum diset. Salin .env.example menjadi .env lalu isi key-nya.")

    agent = Agent(args.mode)
    print(f"Chicken-Agent | mode: {agent.mode} ({agent.cfg['label']}) | /modes untuk daftar, /quit untuk keluar")

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
            for k, v in MODES.items():
                print(f"  {k:12} {v['label']}")
            continue
        if text.startswith("/mode"):
            parts = text.split()
            if len(parts) != 2 or parts[1] not in MODES:
                print("Pakai: /mode <" + "|".join(MODES) + ">")
                continue
            agent.set_mode(parts[1])
            print(f"Mode: {agent.mode} ({agent.cfg['label']})")
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
