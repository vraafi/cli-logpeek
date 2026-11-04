"""
logpeek - Alat CLI untuk membaca dan menganalisis berkas log besar.

Fitur:
- Menyaring baris berdasarkan pola regex.
- Menyorot level log (INFO, WARN, ERROR, DEBUG, dll.) dengan warna.
- Menampilkan N baris terakhir dengan opsi --tail.
- Menghitung jumlah baris per level dengan opsi --ringkas.

Hanya menggunakan pustaka standar Python 3.11.
Keluaran dalam bahasa Indonesia, ringkas, dan dapat diparse.
"""

import argparse
import re
import sys
from pathlib import Path

# Pemetaan level log ke kode warna ANSI
WARNA_LEVEL = {
    "DEBUG": "\033[36m",    # Cyan
    "INFO": "\033[32m",     # Hijau
    "WARN": "\033[33m",     # Kuning
    "WARNING": "\033[33m",  # Kuning
    "ERROR": "\033[31m",    # Merah
    "CRITICAL": "\033[41m", # Latar merah
    "FATAL": "\033[41m",    # Latar merah
}
RESET = "\033[0m"

POLA_LEVEL = re.compile(r"\b(DEBUG|INFO|WARN(?:ING)?|ERROR|CRITICAL|FATAL)\b", re.IGNORECASE)


def baca_baris(berkas, pola_regex=None):
    """Baca berkas dan hasilkan baris yang cocok dengan pola regex (jika ada)."""
    try:
        with open(berkas, "r", encoding="utf-8", errors="replace") as f:
            for baris in f:
                baris = baris.rstrip("\n")
                if pola_regex is None or pola_regex.search(baris):
                    yield baris
    except FileNotFoundError:
        print(f"Kesalahan: Berkas '{berkas}' tidak ditemukan.", file=sys.stderr)
        sys.exit(2)
    except PermissionError:
        print(f"Kesalahan: Tidak memiliki izin untuk membaca berkas '{berkas}'.", file=sys.stderr)
        sys.exit(2)
    except OSError as e:
        print(f"Kesalahan: Gagal membaca berkas '{berkas}': {e}", file=sys.stderr)
        sys.exit(2)


def sorot_level(baris):
    """Sorot level log dalam baris dengan warna ANSI."""
    def ganti(match):
        level = match.group(0).upper()
        warna = WARNA_LEVEL.get(level, "")
        return f"{warna}{match.group(0)}{RESET}" if warna else match.group(0)
    return POLA_LEVEL.sub(ganti, baris)


def hitung_level(baris_list):
    """Hitung kemunculan setiap level log dari daftar baris."""
    hitungan = {}
    for baris in baris_list:
        for match in POLA_LEVEL.finditer(baris):
            level = match.group(0).upper()
            # Normalisasi WARNING menjadi WARN
            if level == "WARNING":
                level = "WARN"
            hitungan[level] = hitungan.get(level, 0) + 1
    return hitungan


def main():
    parser = argparse.ArgumentParser(
        prog="logpeek",
        description="Membaca dan menganalisis berkas log besar: saring pola, sorot level, tail, dan ringkas per level.",
        epilog="Contoh: logpeek app.log --pola 'ERROR' --tail 10 --sorot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("berkas", type=str, help="Path ke berkas log yang akan dibaca")
    parser.add_argument("-p", "--pola", type=str, default=None, help="Pola regex untuk menyaring baris (contoh: 'ERROR|WARN')")
    parser.add_argument("-t", "--tail", type=int, default=None, metavar="N", help="Tampilkan hanya N baris terakhir setelah penyaringan")
    parser.add_argument("-s", "--sorot", action="store_true", help="Sorot level log dengan warna ANSI")
    parser.add_argument("-r", "--ringkas", action="store_true", help="Hitung dan tampilkan jumlah baris per level log")
    args = parser.parse_args()

    # Validasi argumen
    if args.tail is not None and args.tail <= 0:
        parser.error("--tail harus berupa bilangan bulat positif")

    # Kompilasi pola regex jika diberikan
    pola_regex = None
    if args.pola:
        try:
            pola_regex = re.compile(args.pola)
        except re.error as e:
            print(f"Kesalahan: Pola regex tidak valid: {e}", file=sys.stderr)
            sys.exit(2)

    # Baca baris (dengan penyaringan)
    baris_iter = baca_baris(args.berkas, pola_regex)

    # Jika mode ringkas, kumpulkan semua baris yang cocok lalu hitung level
    if args.ringkas:
        baris_list = list(baris_iter)
        hitungan = hitung_level(baris_list)
        if not hitungan:
            print("Tidak ada level log yang ditemukan.")
        else:
            print("Ringkasan per level:")
            for level in sorted(hitungan):
                print(f"  {level}: {hitungan[level]}")
        return

    # Mode tampilan baris
    if args.tail is not None:
        # Gunakan deque untuk efisiensi memori
        from collections import deque
        baris_list = deque(baris_iter, maxlen=args.tail)
    else:
        baris_list = baris_iter

    for baris in baris_list:
        keluaran = sorot_level(baris) if args.sorot else baris
        print(keluaran)


if __name__ == "__main__":
    main()
