"""
logpeek: Alat CLI untuk membaca berkas log besar.

Fitur:
- Menyaring baris berdasarkan pola regex.
- Menyorot level log (INFO, WARNING, ERROR, DEBUG) dengan warna jika terminal mendukung.
- Menampilkan N baris terakhir dengan --tail.
- Menghitung jumlah baris per level dengan --ringkas.

Semua output dalam bahasa Indonesia dan dapat diparse (format ringkas).
"""

import argparse
import re
import sys
import os
from collections import Counter

# Warna ANSI (hanya jika stdout adalah terminal)
ANSI = {
    'DEBUG': '\033[36m',    # cyan
    'INFO': '\033[32m',     # green
    'WARNING': '\033[33m',  # yellow
    'ERROR': '\033[31m',    # red
    'RESET': '\033[0m'
}

def warna_level(teks: str, level: str, aktif: bool) -> str:
    """Kembalikan teks dengan warna level jika aktif."""
    if not aktif:
        return teks
    kode = ANSI.get(level)
    if kode:
        return f"{kode}{teks}{ANSI['RESET']}"
    return teks

def deteksi_level(baris: str) -> str | None:
    """Deteksi level log dari baris (case-insensitive)."""
    baris_upper = baris.upper()
    for level in ('DEBUG', 'INFO', 'WARNING', 'ERROR'):
        if level in baris_upper:
            return level
    return None

def proses_berkas(
    path: str,
    pola: re.Pattern | None,
    tail: int | None,
    ringkas: bool,
    sorot: bool
) -> None:
    """Baca berkas log, saring, dan tampilkan/hitung."""
    # Buka berkas; tangani error di pemanggil
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        if tail is not None:
            # Baca semua baris untuk tail (bisa dioptimalkan, tapi sederhana)
            baris_list = f.readlines()
            if pola:
                baris_list = [b for b in baris_list if pola.search(b)]
            baris_list = baris_list[-tail:] if tail > 0 else baris_list
            # Tampilkan
            for b in baris_list:
                level = deteksi_level(b)
                if level:
                    b = b.replace(level, warna_level(level, level, sorot), 1)
                sys.stdout.write(b)
            return

        # Mode streaming (tanpa tail)
        hitung = Counter() if ringkas else None
        for baris in f:
            if pola and not pola.search(baris):
                continue
            level = deteksi_level(baris)
            if ringkas:
                if level:
                    hitung[level] += 1
                else:
                    hitung['LAINNYA'] += 1
            else:
                # Tampilkan baris dengan sorot level
                if level:
                    baris = baris.replace(level, warna_level(level, level, sorot), 1)
                sys.stdout.write(baris)

        if ringkas:
            # Cetak ringkasan yang dapat diparse
            for level in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'LAINNYA'):
                jumlah = hitung.get(level, 0)
                print(f"{level}: {jumlah}")

def main() -> int:
    parser = argparse.ArgumentParser(
        description='logpeek: Saring dan ringkas berkas log besar.',
        epilog='Contoh: logpeek app.log --pola ERROR --tail 10 --ringkas',
        add_help=True
    )
    parser.add_argument('berkas', help='Path ke berkas log yang akan dibaca')
    parser.add_argument('--pola', '-p', help='Pola regex untuk menyaring baris')
    parser.add_argument('--tail', '-t', type=int, metavar='N', help='Tampilkan N baris terakhir setelah penyaringan')
    parser.add_argument('--ringkas', '-r', action='store_true', help='Hitung jumlah baris per level log')
    parser.add_argument('--sorot', '-s', action='store_true', help='Sorot level log dengan warna (jika terminal mendukung)')

    args = parser.parse_args()

    # Validasi argumen
    if args.tail is not None and args.tail < 0:
        print('Kesalahan: --tail tidak boleh negatif.', file=sys.stderr)
        return 1

    pola = None
    if args.pola:
        try:
            pola = re.compile(args.pola)
        except re.error as e:
            print(f'Kesalahan: pola regex tidak valid: {e}', file=sys.stderr)
            return 1

    # Cek keberadaan dan keterbacaan berkas
    if not os.path.exists(args.berkas):
        print(f'Kesalahan: Berkas tidak ditemukan: {args.berkas}', file=sys.stderr)
        return 2
    if not os.access(args.berkas, os.R_OK):
        print(f'Kesalahan: Berkas tidak dapat dibaca: {args.berkas}', file=sys.stderr)
        return 2

    # Tentukan apakah sorot aktif (jika terminal dan --sorot)
    sorot_aktif = args.sorot and sys.stdout.isatty()

    try:
        proses_berkas(args.berkas, pola, args.tail, args.ringkas, sorot_aktif)
    except OSError as e:
        print(f'Kesalahan: Gagal membaca berkas: {e}', file=sys.stderr)
        return 2
    except Exception as e:
        print(f'Kesalahan tak terduga: {e}', file=sys.stderr)
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
