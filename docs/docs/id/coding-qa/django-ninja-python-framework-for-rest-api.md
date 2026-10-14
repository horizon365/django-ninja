---
created: 2024-07-25T13:23:12 (UTC +08:00)
tags: []
source: https://medium.com/@mrclemrkz/django-ninja-python-framework-for-rest-api-83808d1037d0
author: Clement Fernando

---


Django-Ninja: Framework Python untuk REST API
===========================================================



> Baru-baru ini saya ingin membangun sebuah service CRUD yang sangat sederhana di dalam REST API. Setelah mencari-cari, saya menemukan sebuah framework sederhana yang menggabungkan fitur terbaik dari dua framework populer. Itulah Django-ninja...

* * *


TL;DR
-----


Baru-baru ini saya ingin membangun sebuah service CRUD yang sangat sederhana di dalam REST API. Setelah mencari-cari, saya menemukan sebuah framework sederhana yang menggabungkan fitur terbaik dari dua framework populer. Itulah Django-ninja; saya menganggapnya sebagai perpaduan antara Django dan FastAPI.

---
Izinkan saya menjelaskan mengapa saya merasa pendekatan ini menguntungkan.


Untuk menekankan latar belakang saya, saya adalah seorang Python Django developer dan telah mengerjakan beberapa project di Flask.


Dengan popularitas FastAPI, saya ingin mencobanya terlebih dahulu. Jadi saya menjalankan contoh-contohnya mengikuti dokumentasinya, dan kesannya, yah, ini keren. Lalu penggunaan Pydantic membuat saya semakin antusias. Yang paling penting, ia dibangun di atas async. Generasi OpenAPI yang sempurna dan tanpa usaha di Swagger UI membuatnya semakin manis.


Ini membuka mata saya. Jadi, saya mulai menggali lebih dalam.


Di sana saya menemukan bahwa karena FastAPI tidak "batteries-included" seperti Django, ia masih memerlukan konfigurasi ORM (SQLAlchemy atau SQLModel), belum lagi kebutuhan package pihak ketiga lain untuk tool migrasi database seperti Alembic.


Jadi, saya berpikir, adakah solusi yang lebih baik di luar sana, dengan konfigurasi lebih sedikit dan lebih stabil? Mungkin ada sesuatu yang belum terhighlight. Lalu saya mulai mencari.


Saya mendaftarkan beberapa dari semua pilihan yang ada (GitHub stars per September 2023):


Flask: 64K stars — rilis pertama: 1 April 2010


FastAPI: 61.8K stars — rilis pertama: 5 Desember 2018


Django Rest Framework: 26.2K stars — rilis pertama: 21 Juli 2005


Sanic: 17.3K stars — rilis pertama: 23 Oktober 2016


Django Ninja: 4.8K stars — rilis pertama: 20 Desember 2020


Jadi, jelas saya menjadi tertarik pada Django Ninja, dan inilah alasan mengapa saya menilainya bagus.

**Popularitas**
--------------


Django-Ninja dibangun di atas Django, web framework yang paling populer dan paling jelas pilihannya. Django-Ninja pertama kali dirilis pada akhir 2020, dan hanya dalam waktu sekitar 3 tahun ia telah memperoleh popularitas yang signifikan.

**Struktur Project yang Umum**
-----------


Berbeda dengan Flask dan FastAPI, Django memaksakan sebuah struktur saat Anda membuat project. Namun, Django lebih fleksibel dalam hal bagaimana Anda ingin memelihara project tersebut. Ini adalah hal yang saya sukai dari Django, karena secara signifikan memudahkan developer Django lain untuk mengikuti project tersebut.


Ya, Django Rest Framework (DRF) juga bisa melakukan ini. Tapi saya tadi bilang "pengembangan yang cepat", kan? Siapa yang tidak menyukai kode yang sederhana dan terorganisir? Itulah keindahan menggunakan Django-Ninja.

**ORM yang Powerful**
------------


Sekali lagi, berasosiasi dengan framework inti yang powerful (Django) membawa reputasi bagi Django-Ninja.


Daripada menulis SQL query sendiri dengan cara yang kurang aman, kita cenderung menggunakan ORM. ORM membantu menulis pemanggilan database yang sederhana dan aman.


Namun, tentu saja, konsep antara Django ORM dan SQLAlchemy ORM berbeda. Django ORM menggunakan pola Active Record, sedangkan SQLAlchemy menggunakan pola Data Mapper, yang akan dijelaskan secara detail di blog lain nanti.

**  
Dokumentasi API yang Mudah Digunakan
-----------------


Ya, DRF (Django Rest Framework) memiliki dokumentasi API-nya sendiri. Tapi menurut saya, OpenAPI Swagger UI jauh lebih baik. Jadi ketika saya membutuhkan Swagger UI dengan DRF, saya menggunakan package swagger generator bernama drf-yasg, yang bekerja cukup baik.


Tetapi seperti FastAPI, di Django-Ninja, Anda bisa mendapatkan OpenAPI Swagger UI yang interaktif tanpa menulis kode tambahan apa pun selain fungsi url.

**Performa**
---------------


Sama seperti FastAPI, ia memiliki dukungan built-in untuk penegakan type melalui Pydantic dan eksekusi asinkron.


Dokumentasi Django-ninja tidak lupa membanggakan hal ini dengan membandingkan data benchmark antara Flask, DRF, dan Django-ninja.

**Pengiriman Lebih Cepat**
-------------------


Sekali lagi, sama seperti FastAPI, ia dapat menjalankan sebuah service REST API dengan basis kode yang sangat sedikit. Pada saat yang sama, ia membantu Anda berkembang dengan mudah sesuai pendekatan filosofis apa pun yang Anda anggap cocok. Itulah keindahan priviledge.


Basis kode yang minimal dan ringkas menghasilkan keterbacaan yang tinggi. Ini pada gilirannya menyalakan intuisi untuk implementasi yang lebih cepat.


Bagaimana komentar, pemikiran, dan pendapat Anda tentang ini? Beri tahu saya di kolom komentar di bawah.
