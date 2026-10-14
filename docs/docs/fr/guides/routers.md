---
comments: true
---
# Fractionner votre API avec des routers

Dans le monde réel, il est presque impossible de conserver toute la logique dans un seul fichier.

**Django Ninja** fournit un moyen simple de fractionner votre API en plusieurs modules à l'aide de routers.

Supposons que vous avez un projet Django avec la structure suivante :


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

Pour ajouter une API à chaque application Django, créez un module `api.py` dans chaque application :

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

Ajoutons maintenant quelques opérations à `events/api.py`. L'astuce consiste à utiliser la classe **Router** au lieu de la classe `NinjaAPI` :

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

Faites ensuite de même pour le `news/api.py` de l'application `news` :

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
Et également pour `blogs/api.py`.


Enfin, rassemblons le tout.
Dans votre dossier de projet de premier niveau (à côté de `urls.py`), créez un autre fichier `api.py` avec une instance `NinjaAPI` :

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

Il devrait ressembler à ceci :

```python
from ninja import NinjaAPI

api = NinjaAPI()

```

Nous importons maintenant tous les routers des applications individuelles et les incluons dans l'instance principale de l'API :

```python hl_lines="2 6 7 8"
from ninja import NinjaAPI
from events.api import router as events_router

api = NinjaAPI()

api.add_router("/events/", events_router)    # You can add a router as an object
api.add_router("/news/", "news.api.router")  #   or by Python path
api.add_router("/blogs/", "blogs.api.router")
```

Ajoutez maintenant `api` à vos URLs comme d'habitude et ouvrez votre navigateur sur `/api/docs`, vous devriez voir tous vos routers combinés en une seule API :


![Swagger UI Simple Routers](../img/simple-routers-swagger.png)


## Authentification du router

Utilisez l'argument `auth` pour appliquer un authentificateur à toutes les opérations déclarées dans un router :

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

Ou en utilisant le constructeur du router
```python
router = Router(auth=BasicAuth())
```

## Tags du router

Vous pouvez utiliser l'argument `tags` pour appliquer des tags à toutes les opérations déclarées dans un router :

```python
api.add_router("/events/", events_router, tags=["events"])
```

Ou en utilisant le constructeur du router
```python
router = Router(tags=["events"])
```


## Routers imbriqués

Parfois, vous devez également fractionner davantage la logique.
**Django Ninja** vous permet d'inclure un router à l'intérieur d'un autre router autant de fois que nécessaire, et enfin d'inclure le router de premier niveau dans l'instance principale de l'`api`.


Concrètement, cela signifie que vous disposez de `add_router` à la fois sur l'instance de l'`api` et sur l'instance de `router` :



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

Vous disposez maintenant des endpoints suivants

```
/api/add
/api/l1/add
/api/l1/l2/add
/api/l1/l2/l3/add
```

Génial ! Allez maintenant consulter la documentation générée automatiquement :

![Swagger UI nested routers](../img/nested-routers-swagger.png)

!!! success

    Poursuivez avec la section suivante **[Authentification](authentication.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
