# logpeek

Alat CLI Python 3.11 untuk membaca berkas log besar dengan fitur penyaringan pola, sorot level, tail, dan ringkasan per level. Hanya menggunakan pustaka standar.

## Instalasi

Tidak perlu instalasi dependensi. Cukup jalankan dengan Python 3.11+:

```bash
python logpeek.py --help
```

## Penggunaan

```
logpeek [--pola POLA] [--tail N] [--sorot] [--ringkas] berkas
```

### Argumen

- `berkas`: Path ke berkas log yang akan dibaca (wajib).
- `-p, --pola POLA`: Pola regex untuk menyaring baris. Contoh: `'ERROR|WARN'`.
- `-t, --tail N`: Tampilkan hanya N baris terakhir setelah penyaringan.
- `-s, --sorot`: Sorot level log (DEBUG, INFO, WARN, ERROR, dll.) dengan warna ANSI.
- `-r, --ringkas`: Hitung dan tampilkan jumlah baris per level log. Tidak menampilkan baris.

### Contoh

1. Tampilkan 10 baris terakhir dari log dengan sorot level:
   ```bash
   python logpeek.py app.log --tail 10 --sorot
   ```

2. Saring baris yang mengandung "ERROR" atau "WARN" lalu tampilkan 5 terakhir:
   ```bash
   python logpeek.py app.log --pola 'ERROR|WARN' --tail 5
   ```

3. Ringkas jumlah level log dari seluruh berkas:
   ```bash
   python logpeek.py app.log --ringkas
   ```

4. Saring dengan pola dan ringkas:
   ```bash
   python logpeek.py app.log --pola 'CRITICAL' --ringkas
   ```

## Penanganan Kesalahan

- Jika berkas tidak ditemukan atau tidak dapat dibaca, program mencetak pesan kesalahan ke stderr dan keluar dengan kode 2.
- Jika pola regex tidak valid, program mencetak pesan kesalahan dan keluar dengan kode 2.

## Catatan

- Warna ANSI hanya ditampilkan jika opsi `--sorot` digunakan; pastikan terminal mendukung warna.
- Untuk berkas sangat besar, disarankan menggunakan `--tail` atau `--ringkas` untuk mengurangi memori.
