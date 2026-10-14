---
comments: true
---
# Membuat Situs mkdocs Terindeks oleh Google/Baidu

Di [artikel sebelumnya](add-google-adsense-with-mkdocs.md), kita telah membahas cara menambahkan Google Ads ke mkdocs melalui custom template.

Kemudian, saya menemukan bahwa banyak orang menyarankan untuk secara aktif mengirimkan situs agar terindeks oleh Google dan Baidu.

## Pengindeksan Google

### Tambahkan Situs Web

Buka situs web Google Search Console: [Google Search Console](https://search.google.com/search-console/welcome?hl=zh-CN)

Anda akan diminta untuk memverifikasi kepemilikan situs web. Di sini, kita menggunakan metode HTML tag.

Dengan cara ini, sama seperti menambahkan iklan di artikel sebelumnya, Anda hanya perlu menambahkan satu baris sebelum `</head>` lalu mempublikasikannya.

### Sitemap

Setelah verifikasi berhasil, masukkan `sitemap.xml`, dan setelah beberapa menit, refresh untuk melihat status "Fetch successful", yang berarti Anda sudah selesai.

Kode berikut mem-parsing file sitemap.xml situs ini dan mengambil semua link dokumen.

## Pengindeksan Baidu

### Tambahkan Situs Web

Buka situs web pengindeksan Baidu: [Baidu Search Resource Platform](https://ziyuan.baidu.com/dailysubmit/index)

Mirip dengan verifikasi Google di atas, gunakan verifikasi HTML tag.

### Sitemap
Kemungkinan karena saya tidak mengisi nomor registrasi ICP, bagian sitemap berwarna abu-abu untuk saya. Jadi saya memilih pengiriman manual. Perhatikan bahwa maksimalnya adalah 20 entri per hari.

Semua link situs dapat diperoleh melalui skrip berikut.

```python
import urllib.request
import xml.etree.ElementTree as ET


def parse_and_save_loc(url, output_file):
    # Fetch the XML data from the online address
    response = urllib.request.urlopen(url)
    data = response.read()

    # Parse the XML
    root = ET.fromstring(data)

    # Extract all loc attributes and save them to a TXT file
    with open(output_file, 'w') as f:
        for element in root.iter():
            if 'loc' in element.tag:
                print(element.text)
                f.write(element.text + '\n')


# Specify the online XML file address and the output TXT file path
url = 'https://django-ninja.cn/sitemap.xml'
output_file = 'urls.txt'

parse_and_save_loc(url, output_file)
```

> Artikel referensi:
    1. [Building a Personal Blog Website from Scratch Series](https://www.techxiaofei.com/post/hugo/hugo_search/#%E8%B0%B7%E6%AD%8C%E6%94%B6%E5%BD%95)
  
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
