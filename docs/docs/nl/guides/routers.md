---
comments: true
---
# Je API splitsen met routers

In de echte wereld is het vrijwel onmogelijk om alle logica in één bestand te houden. 

**Django Ninja** biedt een eenvoudige manier om je API op te splitsen in meerdere modules met behulp van routers.

Stel dat je een Django project hebt met de volgende structuur:


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

Om een API aan elke Django applicatie toe te voegen, maak je in elke applicatie een module `api.py` aan:

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

Laten we nu enkele operaties toevoegen aan `events/api.py`. De truc is dat je in plaats van de class `NinjaAPI` de class **Router** gebruikt:

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

Doe daarna hetzelfde voor de `api.py` van de `news` app:

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
En ook voor `blogs/api.py`.


Laten we ten slotte alles samenvoegen.
Maak in je bovenste projectmap (naast `urls.py`) nog een bestand `api.py` aan met een `NinjaAPI` instantie:

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

Het ziet er dan zo uit:

```python
from ninja import NinjaAPI

api = NinjaAPI()

```

Nu importeren we alle routers uit de individuele applicaties en voegen we ze toe aan de hoofd-API instantie:

```python hl_lines="2 6 7 8"
from ninja import NinjaAPI
from events.api import router as events_router

api = NinjaAPI()

api.add_router("/events/", events_router)    # You can add a router as an object
api.add_router("/news/", "news.api.router")  #   or by Python path
api.add_router("/blogs/", "blogs.api.router")
```

Voeg nu `api` op de gebruikelijke manier toe aan je URLs en open je browser op `/api/docs`, je zou al je routers samengevoegd in één API moeten zien:


![Swagger UI Simple Routers](../img/simple-routers-swagger.png)


## Router authenticatie

Gebruik het argument `auth` om een authenticator toe te passen op alle operaties die in een router worden gedeclareerd:

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

Of via de constructor van de router:
```python
router = Router(auth=BasicAuth())
```

## Router tags

Je kunt het argument `tags` gebruiken om tags toe te passen op alle operaties die in een router worden gedeclareerd:

```python
api.add_router("/events/", events_router, tags=["events"])
```

Of via de constructor van de router:
```python
router = Router(tags=["events"])
```


## Geneste routers

Soms moet je de logica ook verder opsplitsen.
**Django Ninja** laat je een router een willekeurig aantal keren in een andere router opnemen, en ten slotte de router op het hoogste niveau opnemen in de hoofd-`api` instantie.


In feite betekent dit dat je `add_router` hebt op zowel de `api` instantie als de `router` instantie:



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

Nu heb je de volgende endpoints:

```
/api/add
/api/l1/add
/api/l1/l2/add
/api/l1/l2/l3/add
```

Geweldig! Ga nu de automatisch gegenereerde documentatie bekijken:

![Swagger UI nested routers](../img/nested-routers-swagger.png)

!!! success

    Ga verder naar de volgende sectie **[Authenticatie](authentication.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
