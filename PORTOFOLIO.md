## Masalah
Berkas log besar sulit dibaca dengan alat standar. Baris ribuan membuat pencarian pola lambat dan level log tenggelam di antara noise. Tim butuh alat CLI ringan yang langsung menyaring, menyorot, dan meringkas.

## Yang Dibangun
logpeek: CLI untuk membaca berkas log besar. Fitur utama: saring pola, sorot level, `--tail N` untuk mengambil N baris terakhir, dan `--ringkas` untuk menghitung jumlah per level. Berkas hasil: `logpeek.py` (5021 B) dan `README.md` (1705 B).

## Keputusan Teknis
Saya memilih Python satu berkas agar mudah dipasang tanpa dependensi. Mode `--ringkas` menghitung per level langsung saat streaming, bukan menyimpan seluruh log di memori. `--tail` memakai pembacaan dari ujung berkas agar hemat I/O pada berkas besar.

## Bukti
QC hanya mengaktifkan lapis kode. Lapis kode lulus. Waktu QC 1,01 detik. Temuan: 0. Rincian berkas: 1 Python, 0 JavaScript, 0 JSON, 0 Lua, 1 lainnya.

## Batasan
QC belum mencakup lapis non-kode, jadi dokumentasi dan perilaku CLI belum diverifikasi otomatis. Repo memuat 0 berkas uji JS, JSON, dan Lua. Bukti masih terbatas pada lintas kode Python.