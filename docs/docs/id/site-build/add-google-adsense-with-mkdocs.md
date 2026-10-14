---
comments: true
---
# Menambahkan Google Adsense ke Dokumentasi mkdocs
Temukan `base.html` asli di versi mkdocs-material Anda:

```
✗ python3               
>>> import material
>>> material.__path__
['/opt/homebrew/lib/python3.10/site-packages/material']
```
Di `mkdocs.yml`, aktifkan fitur `overrides`, dan buat folder baru bernama `overrides` di bawah direktori situs.
```
theme:
  name: material
  custom_dir: overrides
```

Struktur file:
```
.
├─ overrides/
│  └─ base.html
└─ mkdocs.yml
```

Edit file `template/base.html` di bawah direktori `material.__path__` di atas, dan tambahkan kode adsense Anda sebelum bagian `</head>`,
```
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4071429194671997"
     crossorigin="anonymous"></script>
  </head>
```
Lalu simpan ke `overides/base.html`.

Terakhir, setelah menjalankan perintah `mkdocs build`, periksa apakah source halaman yang dihasilkan berisi bagian yang berkaitan dengan `adsbygoogle`.

Jika semuanya berjalan lancar, situs mkdocs Anda sekarang sudah terintegrasi dengan Google Adsense.

Selamat!
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
