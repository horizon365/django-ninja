---
title: Django Ninja - REST framework Django yang cepat
template: home.html
comments: true
---

Django Ninja adalah framework web untuk membangun API dengan Django dan type hints Python 3.6+.

Fitur utama:

 - **Mudah dipahami**: Dirancang agar mudah digunakan dan intuitif.
 - **Eksekusi cepat**: Berkat **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** dan **<a href="guides/async-support/">async support</a>**, kinerjanya sangat tinggi.
 - **Cepat untuk coding**: Django Ninja adalah framework web untuk membangun API dengan Django dan type hints Python 3.6+.
 - **Berbasis standar**: Berdasarkan standar: **OpenAPI** (dahulu Swagger) dan **JSON Schema**.
 - **Ramah Django**: (tentu saja) terintegrasi dengan baik dengan core Django dan ORM.
 - **Siap untuk production**: Digunakan oleh banyak perusahaan dalam proyek nyata (jika Anda menggunakan Django Ninja dan ingin membagikan masukan Anda, silakan kirim email ke ppr.vitaly@gmail.com).

<a href="https://github.com/vitalik/django-ninja-benchmarks" target="_blank">Benchmarks</a>:

![Django Ninja REST Framework](img/benchmark.png)

## Instalasi

```
pip install django-ninja
```

## Contoh singkat

Mulai proyek Django baru (atau gunakan proyek yang sudah ada)
```
django-admin startproject apidemo
```

Di `urls.py`

```python hl_lines="3 5 8 9 10 15"
{!./src/index001.py!}
```

Sekarang, jalankan seperti biasa:
```
./manage.py runserver
```

Catatan: Anda tidak perlu menambahkan Django Ninja ke installed apps Anda agar dapat berfungsi.

## Periksa hasilnya

Buka browser Anda di <a href="http://127.0.0.1:8000/api/add?a=1&b=2" target="_blank">http://127.0.0.1:8000/api/add?a=1&b=2</a>

Anda akan melihat response JSON seperti:
```JSON
{"result": 3}
```
Sekarang Anda baru saja membuat API yang:

 - Menerima HTTP GET request di `/api/add`
 - Menerima, memvalidasi, dan melakukan konversi tipe parameter GET `a` dan `b`
 - Meng-decode hasilnya sebagai JSON
 - Menghasilkan schema OpenAPI untuk operasi yang didefinisikan

## Dokumentasi API interaktif

Sekarang buka <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

Anda akan melihat dokumentasi API interaktif otomatis (disediakan oleh <a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a> atau <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a>) :

![Swagger UI](img/index-swagger-ui.png)


## Ringkasan

Singkatnya, Anda hanya perlu mendeklarasikan tipe parameter, request body, dll. **satu kali**, sebagai argumen fungsi.

Anda melakukannya dengan tipe Python modern yang standar.

Anda tidak perlu mempelajari sintaks baru, method atau class dari library tertentu, dll.

Cukup **Python 3.6+** standar.

Sebagai contoh, untuk `int`:

```python
a: int
```

Atau, untuk model `Item` yang lebih kompleks:

```python
class Item(Schema):
    foo: str
    bar: float

def operation(a: Item):
    ...
```

...hanya dengan satu deklarasi ini, Anda mendapatkan:

* Dukungan editor, termasuk:
    * Autocompletion
    * Type checking
* Validasi data:
    * Error yang otomatis dan jelas saat data tidak valid
    * Validasi bahkan untuk objek JSON yang bersarang secara mendalam
* <abbr title="Juga dikenal sebagai: serialization, parsing, marshalling">Serialization</abbr> data input jaringan dan konversi menjadi data keluaran Python, serta pembacaan dari:
    * JSON
    * Path parameters
    * Query parameters
    * Cookies
    * Headers
    * Forms
    * Files
* Dokumentasi API interaktif otomatis

Proyek ini sangat terinspirasi oleh <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a>.

!!! note

    Lihat **[Tutorial](tutorial/index.md)** untuk memulai dengan cepat.

    Ekosistem di sekitar Django Ninja:

    1. [django-ninja](index.md): Framework berbasis Django yang mengambil yang terbaik dari Django dan memasangkannya dengan kekuatan Pydantic — pilihan optimal di persimpangan antara keamanan dan kenyamanan.

    2. [django-ninja-crud](django-ninja-crud/index.md): Framework yang dibangun di atas django-ninja untuk menyederhanakan pengembangan antarmuka CRUD, menyediakan model viewset deklaratif dan metode pengujian berbasis skenario.

    3. [django-ninja-extra](django-ninja-extra/index.md): Alat yang memungkinkan developer melewati dokumentasi Django yang bertele-tele dan membangun aplikasi web yang powerful serta antarmuka API modern dengan kode minimal.

    4. [django-ninja-jwt](django-ninja-jwt/index.md): Plugin JSON Web Token untuk django-ninja yang mengimplementasikan authentication dan fitur terkait, di-fork dari plugin Django Rest Framework yang populer.
