Masalah Aneh di Halaman Docs Django Ninja: Dua Endpoint Berbeda Terbuka Bersamaan
==========================================================

Belum-baru ini, seorang anggota komunitas melaporkan sebuah masalah: di halaman docs, mengklik salah satu dari dua endpoint akan membuka keduanya secara bersamaan. API lain tidak berperilaku seperti ini.

![django-ninja-docs-wrong](/img/docs-wrong.png)


Akar masalahnya akhirnya ditemukan: nama fungsi atau path-nya duplikat. Dengan kata lain, saat menulis view, sebuah fungsi dicopy tetapi namanya lupa diubah.
