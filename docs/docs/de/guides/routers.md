---
comments: true
---
# Ihre API mit Routern aufteilen

In der realen Welt ist es fast unmöglich, die gesamte Logik in einer einzigen Datei zu halten. 

**Django Ninja** bietet eine einfache Möglichkeit, Ihre API mithilfe von Routern in mehrere Module aufzuteilen.

Angenommen, Sie haben ein Django-Projekt mit der folgenden Struktur:


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

Um jeder Django-Anwendung eine API hinzuzufügen, erstellen Sie in jeder Anwendung ein Modul `api.py`:

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

Fügen wir nun einige Operationen zu `events/api.py` hinzu. Der Trick besteht darin, dass Sie anstelle der Klasse `NinjaAPI` die Klasse **Router** verwenden:

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

Machen Sie dasselbe dann für `news/api.py` der `news`-App:

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
Und ebenso für `blogs/api.py`.


Zum Schluss bringen wir alles zusammen.
Erstellen Sie in Ihrem übergeordneten Projektordner (neben `urls.py`) eine weitere Datei `api.py` mit einer `NinjaAPI`-Instanz:

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

Sie sollte so aussehen:

```python
from ninja import NinjaAPI

api = NinjaAPI()

```

Nun importieren wir alle Router aus den einzelnen Anwendungen und binden sie in die Haupt-API-Instanz ein:

```python hl_lines="2 6 7 8"
from ninja import NinjaAPI
from events.api import router as events_router

api = NinjaAPI()

api.add_router("/events/", events_router)    # You can add a router as an object
api.add_router("/news/", "news.api.router")  #   or by Python path
api.add_router("/blogs/", "blogs.api.router")
```

Fügen Sie nun `api` wie gewohnt zu Ihren URLs hinzu und öffnen Sie im Browser `/api/docs` – Sie sollten alle Ihre Router zu einer einzigen API zusammengefasst sehen:


![Swagger UI Simple Routers](../img/simple-routers-swagger.png)


## Router-Authentifizierung

Verwenden Sie das Argument `auth`, um einen Authentifikator auf alle in einem Router deklarierten Operationen anzuwenden:

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

Oder über den Konstruktor des Routers:
```python
router = Router(auth=BasicAuth())
```

## Router-Tags

Sie können das Argument `tags` verwenden, um allen in einem Router deklarierten Operationen Tags zuzuweisen:

```python
api.add_router("/events/", events_router, tags=["events"])
```

Oder über den Konstruktor des Routers:
```python
router = Router(tags=["events"])
```


## Verschachtelte Router

Manchmal müssen Sie die Logik auch weiter aufteilen.
**Django Ninja** erlaubt es Ihnen, einen Router beliebig oft in einen anderen Router einzubinden und schließlich den Router der obersten Ebene in die Haupt-`api`-Instanz einzubinden.


Im Grunde bedeutet das, dass Sie `add_router` sowohl auf der `api`-Instanz als auch auf der `router`-Instanz haben:



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

Jetzt haben Sie die folgenden Endpunkte

```
/api/add
/api/l1/add
/api/l1/l2/add
/api/l1/l2/l3/add
```

Super! Sehen Sie sich nun die automatisch generierte Dokumentation an:

![Swagger UI nested routers](../img/nested-routers-swagger.png)

!!! success

    Fahren Sie mit dem nächsten Abschnitt fort: **[Authentifizierung](authentication.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
