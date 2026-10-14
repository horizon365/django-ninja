---
comments: true
---
# Tutorial - Langkah pertama

Tutorial ini menunjukkan cara menggunakan sebagian besar fitur **Django Ninja**.

Tutorial ini mengasumsikan bahwa Anda mengetahui setidaknya dasar-dasar <a href="https://www.djangoproject.com/" target="_blank">framework Django</a>, seperti cara membuat proyek dan menjalankannya.

## Instalasi

```console
pip install django-ninja
```

!!! note

    Ini tidak diwajibkan, tetapi Anda juga dapat menambahkan `ninja` ke `INSTALLED_APPS`.
    Dalam hal itu, OpenAPI/Swagger UI (atau Redoc) akan dimuat dari paket JavaScript yang disertakan (yang lebih cepat) (sebaliknya, paket JavaScript berasal dari CDN)

## Membuat proyek Django

Mulai proyek Django baru (atau, jika Anda sudah memiliki proyek Django yang ada, langsung ke langkah berikutnya).

```
django-admin startproject myproject
```

## Membuat API

Mari kita buat sebuah module untuk API kita. Buat file `api.py` di lokasi yang sama dengan root `urls.py` proyek Django Anda:

```python
from ninja import NinjaAPI

api = NinjaAPI()
```

Sekarang buka `urls.py` dan tambahkan yang berikut:

```python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## Operasi pertama kita

**Django Ninja** dilengkapi dengan decorator untuk setiap method HTTP (`GET`, `POST`,
`PUT`, dll.). Di file `api.py` kita, mari tambahkan operasi "hello world" sederhana.

```python hl_lines="5-7"
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"
```

Sekarang buka browser dan buka <a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a> yang akan mengembalikan response JSON sederhana:
```json
"Hello world"
```

!!! success

    Lanjutkan ke bab berikutnya **[Menangani parameter input](step2.md)**.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
