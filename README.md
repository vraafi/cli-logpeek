# logpeek

Alat CLI untuk membaca berkas log besar dengan penyaringan, sorot level, tail, dan ringkasan per level. Hanya menggunakan pustaka standar Python 3.11.

## Instalasi

Tidak perlu instalasi. Cukup jalankan dengan Python 3.11+:

```bash
python logpeek.py --help
```

## Penggunaan

```
logpeek.py BERKAS [--pola POLA] [--tail N] [--ringkas] [--sorot]
```

### Opsi

- `BERKAS`: Path ke berkas log yang akan dibaca (wajib).
- `--pola`, `-p`: Pola regex untuk menyaring baris (opsional).
- `--tail`, `-t`: Tampilkan N baris terakhir setelah penyaringan (opsional).
- `--ringkas`, `-r`: Hitung jumlah baris per level log (DEBUG, INFO, WARNING, ERROR, LAINNYA).
- `--sorot`, `-s`: Sorot level log dengan warna (hanya jika terminal mendukung).

### Contoh

1. Tampilkan semua baris dari `app.log`:
   ```bash
   python logpeek.py app.log
   ```

2. Saring baris yang mengandung "ERROR" dan tampilkan 5 baris terakhir:
   ```bash
   python logpeek.py app.log --pola ERROR --tail 5
   ```

3. Ringkas jumlah per level dari `app.log`:
   ```bash
   python logpeek.py app.log --ringkas
   ```

4. Saring dengan regex dan sorot level:
   ```bash
   python logpeek.py app.log --pola "user=\d+" --sorot
   ```

## Exit Code

- `0`: Berhasil.
- `1`: Kesalahan argumen (mis. regex tidak valid, tail negatif).
- `2`: Berkas tidak ditemukan atau tidak dapat dibaca.

## Catatan

- Sorot warna hanya aktif jika `--sorot` diberikan dan output adalah terminal (TTY).
- Output ringkasan dalam format `LEVEL: jumlah` yang mudah diparse.
- Penanganan berkas besar: mode streaming untuk penyaringan tanpa tail; mode baca semua untuk tail (karena keterbatasan).
