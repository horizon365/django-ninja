---
comments: true
---
# Dokumentasi API

## Dokumentasi OpenAPI

Setelah Anda mengonfigurasi Ninja API dan menjalankan runserver - buka <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

Anda akan melihat dokumentasi API otomatis yang interaktif (ditenagai oleh <a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a>)


## CDN dan file statis

Anda tidak perlu menambahkan django ninja ke `INSTALLED_APPS`. Dalam hal ini UI interaktifnya akan di-host dari CDN.

Untuk meng-host dokumentasi (Js/css) dari server Anda sendiri - cukup masukkan `"ninja"` ke dalam INSTALLED_APPS - dalam hal ini mekanisme hosting file statis standar django yang akan meng-host-nya.

## Beralih ke Redoc


```python
from ninja import Redoc

api = NinjaAPI(docs=Redoc())

```
Kemudian Anda akan melihat dokumentasi yang dibuat secara otomatis dengan tampilan lain (ditenagai oleh <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a>).

## Mengubah pengaturan tampilan dokumentasi
Untuk mengatur pengaturan kustom untuk Swagger atau Redocs, Anda dapat menggunakan argumen `settings` pada class docs.

```python
from ninja import Redoc, Swagger

api = NinjaAPI(docs=Swagger(settings={"persistAuthorization": True}))
...
api = NinjaAPI(docs=Redoc(settings={"disableSearch": True}))

```

Untuk pengaturan lainnya, lihat dokumentasi:

 - [Konfigurasi Swagger](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)
 - [Konfigurasi Redoc](https://redocly.com/docs/api-reference-docs/configuration/functionality/)



## Menyembunyikan docs

Jika Anda tidak perlu menampilkan dokumentasi interaktif - atur argumen `docs_url` menjadi `None`

```python
api = NinjaAPI(docs_url=None)
```

## Melindungi docs

Untuk menggunakan autentikasi (atau decorator lain untuk tujuan apa pun), gunakan argumen `docs_decorator`:

```python
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(docs_decorator=staff_member_required)
```

## Memperluas skema OpenAPI dengan atribut kustom

Anda dapat memperluas skema OpenAPI dengan atribut kustom, misalnya menambahkan `termsOfService`

```python
api = NinjaAPI(
   openapi_extra={
       "info": {
           "termsOfService": "https://example.com/terms/",
       }
   },
   title="Demo API",
   description="This is a demo API with dynamic OpenAPI info section"
)
```

## Resolve URL dokumentasi

Anda dapat me-reverse URL dari view dokumentasi API dengan merujuk nama view `openapi-view`.

Dalam kode Python, misalnya:
```python
from django.urls import reverse

reverse('api-1.0.0:openapi-view')

>>> '/api/docs'
```

Dalam template Django, misalnya:
```Html
<a href="{% url 'api-1.0.0:openapi-view' %}">API Docs</a>

<a href="/api/docs">API Docs</a>
```

## Membuat penampil docs kustom

Untuk membuat view OpenAPI Anda sendiri - buatlah class yang mewarisi dari DocsBase dan override metode `render_page`:



```python
from ninja.openapi.docs import DocsBase

class MyDocsViewer(DocsBase):
    def render_page(self, request, api):
        ... # return http response

...

api = NinjaAPI(docs=MyDocsViewer())

```

!!! success

    Lanjutkan ke bagian berikutnya **[Penanganan error](errors.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
