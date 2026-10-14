---
comments: true
---
# Memecah API Anda dengan routers

Di dunia nyata, hampir tidak mungkin menempatkan seluruh logika dalam satu file. 

**Django Ninja** menyediakan cara sederhana untuk memecah API Anda menjadi beberapa modul menggunakan routers.

Misalkan Anda memiliki proyek Django dengan struktur berikut:


```
├── myproject
│   └── settings.py
├── events/
│   ├── __init__.py
│   └── models.py
├── news/
│   ├── __init__.py
│   └── models.py
├── blogs/
│   ├── __init__.py
│   └── models.py
└── manage.py
```

Untuk menambahkan API ke setiap aplikasi Django, buatlah sebuah modul `api.py` di setiap aplikasi:

``` hl_lines="5 9 13"
├── myproject
│   └── settings.py
├── events/
│   ├── __init__.py
│   ├── api.py
│   └── models.py
├── news/
│   ├── __init__.py
│   ├── api.py
│   └── models.py
├── blogs/
│   ├── __init__.py
│   ├── api.py
│   └── models.py
└── manage.py
```

Sekarang mari kita tambahkan beberapa operation ke `events/api.py`. Triknya adalah alih-alih menggunakan class `NinjaAPI`, Anda menggunakan class **Router**:

```python  hl_lines="1 4 6 13"
from ninja import Router
from .models import Event

router = Router()

@router.get('/')
def list_events(request):
    return [
        {"id": e.id, "title": e.title}
        for e in Event.objects.all()
    ]

@router.get('/{event_id}')
def event_details(request, event_id: int):
    event = Event.objects.get(id=event_id)
    return {"title": event.title, "details": event.details}
```

Kemudian lakukan hal yang sama untuk `news/api.py` milik aplikasi `news`:

```python  hl_lines="1 4"
from ninja import Router
from .models import News

router = Router()

@router.get('/')
def list_news(request):
    ...

@router.get('/{news_id}')
def news_details(request, news_id: int):
    ...
```
Dan juga `blogs/api.py`.


Terakhir, mari kita satukan semuanya.
Di folder proyek tingkat atas Anda (bersebelahan dengan `urls.py`), buatlah file `api.py` lain dengan sebuah instance `NinjaAPI`:

``` hl_lines="2"
├── myproject
│   ├── api.py
│   └── settings.py
├── events/
│   ...
├── news/
│   ...
├── blogs/
│   ...

```

Isinya akan terlihat seperti ini:

```python
from ninja import NinjaAPI

api = NinjaAPI()

```

Sekarang kita mengimpor semua routers dari masing-masing aplikasi dan memasukkannya ke instance API utama:

```python hl_lines="2 6 7 8"
from ninja import NinjaAPI
from events.api import router as events_router

api = NinjaAPI()

api.add_router("/events/", events_router)    # You can add a router as an object
api.add_router("/news/", "news.api.router")  #   or by Python path
api.add_router("/blogs/", "blogs.api.router")
```

Sekarang, tambahkan `api` ke URL Anda seperti biasa dan buka browser di `/api/docs`, Anda akan melihat semua router Anda tergabung menjadi satu API:


![Swagger UI Simple Routers](../img/simple-routers-swagger.png)


## Autentikasi pada router

Gunakan argumen `auth` untuk menerapkan authenticator ke semua operation yang dideklarasikan di dalam sebuah router:

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

Atau melalui konstruktor router
```python
router = Router(auth=BasicAuth())
```

## Tags pada router

Anda dapat menggunakan argumen `tags` untuk menerapkan tags ke semua operation yang dideklarasikan di dalam sebuah router:

```python
api.add_router("/events/", events_router, tags=["events"])
```

Atau melalui konstruktor router
```python
router = Router(tags=["events"])
```


## Nested routers

Terkadang Anda juga perlu memecah logika lebih jauh lagi.
**Django Ninja** memungkinkan Anda memasukkan sebuah router ke dalam router lain sebanyak yang Anda mau, dan terakhir memasukkan router tingkat atas ke instance `api` utama.


Pada dasarnya, ini berarti Anda memiliki `add_router` baik pada instance `api` maupun pada instance `router`:



```python hl_lines="7 8 9 32 33 34"
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, Router

api = NinjaAPI()

first_router = Router()
second_router = Router()
third_router = Router()


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


@first_router.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


@second_router.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


@third_router.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


second_router.add_router("l3", third_router)
first_router.add_router("l2", second_router)
api.add_router("l1", first_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

Sekarang Anda memiliki endpoints berikut

```
/api/add
/api/l1/add
/api/l1/l2/add
/api/l1/l2/l3/add
```

Bagus! Sekarang silakan periksa dokumentasi yang dihasilkan secara otomatis:

![Swagger UI nested routers](../img/nested-routers-swagger.png)

!!! success

    Lanjutkan ke bagian berikutnya **[Autentikasi](authentication.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
