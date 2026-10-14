![Test](https://github.com/eadwinCode/django-ninja-extra/workflows/Test/badge.svg)
[![PyPI version](https://badge.fury.io/py/django-ninja-extra.svg)](https://badge.fury.io/py/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/v/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/pyversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/djversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![Codecov](https://img.shields.io/codecov/c/gh/eadwinCode/django-ninja-extra)](https://codecov.io/gh/eadwinCode/django-ninja-extra)
[![Downloads](https://pepy.tech/badge/django-ninja-extra)](https://pepy.tech/project/django-ninja-extra)

# Dokumentasi Django Ninja Extra

**Django Ninja Extra** menyediakan pendekatan **class-based** beserta fitur-fitur tambahan yang akan mempercepat pengembangan RESTful API Anda menggunakan [**Django Ninja**](https://django-ninja.cn).

**Fitur utama:**

Semua fitur **Django-Ninja**:

- **Sederhana**: Dirancang agar mudah digunakan dan intuitif.
- **Eksekusi cepat**: Berkat **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** dan **<a href="/async-support/">async support</a>, ia memberikan performa yang sangat tinggi.**
- **Coding cepat**: Type hints dan dokumentasi otomatis membiarkan Anda fokus pada business logic.
- **Berbasis standar**: Berbasis pada standar: **OpenAPI** (dahulu Swagger) dan **JSON Schema**.
- **Ramah Django**: (Jelas saja) terintegrasi dengan baik dengan core dan ORM Django.

Ditambah **Extra**:

- **Class-based**: Rancang API Anda dengan cara class-based.
- **Permission**: Amankan endpoint akses dengan mudah melalui permission dan autentikasi yang didefinisikan di level route atau level controller.
- **Dependency injection**: Class controller mendukung penggunaan Python [**Injector** ](https://injector.readthedocs.io/en/latest/) atau [**django_injector**](https://github.com/blubber/django_injector). Ini memungkinkan Anda meng-inject service dependensi API ke dalam class APIController dan menggunakannya di tempat yang dibutuhkan.

---

### Persyaratan Versi
- Python >= 3.6
- django >= 2.1 
- pydantic >= 1.6 
- Django-Ninja >= 0.16.1


Untuk dokumentasi lengkapnya, [kunjungi link ini](https://django-ninja.cn/django-ninja-extra/).

## Instalasi

```
pip install django-ninja-extra
```
Setelah instalasi, tambahkan `ninja_extra` ke `INSTALLED_APPS` Anda

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```

## Penggunaan

Di project Django Anda, buat file `api.py` baru di samping `urls.py`:

```Python
from ninja_extra import NinjaExtraAPI, api_controller, http_get

api = NinjaExtraAPI()

# Function-based definition
@api.get("/add", tags=['Math'])
def add(request, a: int, b: int):
    return {"result": a + b}

# Class-based definition
@api_controller('/', tags=['Math'], permissions=[])
class MathAPI:

    @http_get('/subtract',)
    def subtract(self, a: int, b: int):
        """Subtracts a from b"""
        return {"result": a - b}

    @http_get('/divide',)
    def divide(self, a: int, b: int):
        """Divides a by b"""
        return {"result": a / b}
    
    @http_get('/multiple',)
    def multiple(self, a: int, b: int):
        """Multiples a with b"""
        return {"result": a * b}
    
api.register_controllers(
    MathAPI
)
```

Sekarang buka `urls.py` dan tambahkan yang berikut:

```Python
...
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # <---------- !
]
```

### Dokumentasi API interaktif

Sekarang buka <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

Anda akan melihat dokumentasi API interaktif otomatis (ditenagai oleh <a href="https://github.com/swagger-api/swagger-ui" target="_blank">Swagger UI</a>):

![Swagger UI](images/ui_swagger_preview_readme.gif)

## Tutorial
- [django-ninja - Menggunakan permission, controller, dan throttling django-ninja-extra!](https://www.youtube.com/watch?v=yQqig-c2dd4) - Pelajari cara menggunakan permission, controller, dan throttling django-ninja-extra
- [BookStore API](https://github.com/eadwinCode/bookstoreapi) - Sebuah contoh project yang mendemonstrasikan cara menggunakan django-ninja-extra dengan ninja schema dan ninja-jwt

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
