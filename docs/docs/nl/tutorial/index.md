---
comments: true
---
# Tutorial - Eerste stappen

Deze tutorial laat je zien hoe je de meeste functies van **Django Ninja** gebruikt.

In deze tutorial gaan we ervan uit dat je op zijn minst de basis van het <a href="https://www.djangoproject.com/" target="_blank">Django framework</a> kent, zoals het aanmaken van een project en het uitvoeren ervan.

## Installatie

```console
pip install django-ninja
```

!!! note

    Dit is niet vereist, maar je kunt `ninja` ook toevoegen aan `INSTALLED_APPS`.
    In dat geval wordt de OpenAPI/Swagger UI (of Redoc) geladen vanuit het meegeleverde JavaScript-pakket (wat sneller is) (anders komt het JavaScript-bundel van een CDN)

## Maak een Django-project aan

Start een nieuw Django-project (of, als je al een bestaand Django-project hebt, ga dan naar de volgende stap).

```
django-admin startproject myproject
```

## Maak een API aan

Laten we een module maken voor onze API. Maak een bestand `api.py` aan op dezelfde locatie als de root-`urls.py` van je Django-project:

```python
from ninja import NinjaAPI

api = NinjaAPI()
```

Ga nu naar `urls.py` en voeg het volgende toe:

```python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## Onze eerste operatie

**Django Ninja** wordt geleverd met een decorator voor elke HTTP-methode (`GET`, `POST`,
`PUT`, enz.). Laten we in ons bestand `api.py` een eenvoudige "hello world"-operatie toevoegen.

```python hl_lines="5-7"
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"
```

Ga nu naar de browser en open <a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a>, wat een eenvoudige JSON-response teruggeeft:
```json
"Hello world"
```

!!! success

    Ga verder naar het volgende hoofdstuk **[Omgaan met inputparameters](step2.md)**.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
