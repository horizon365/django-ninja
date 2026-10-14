---
comments: true
---
# Разделение вашего API с помощью роутеров

В реальном мире практически невозможно держать всю логику в одном файле. 

**Django Ninja** предоставляет простой способ разделить ваш API на несколько модулей с помощью роутеров.

Предположим, у вас есть проект Django со следующей структурой:


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

Чтобы добавить API в каждое Django-приложение, создайте модуль `api.py` в каждом приложении:

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

Теперь добавим несколько операций в `events/api.py`. Хитрость в том, что вместо класса `NinjaAPI` вы используете класс **Router**:

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

Затем сделайте то же самое для `news/api.py` приложения `news`:

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
А также для `blogs/api.py`.


Наконец, соберём всё вместе.
В папке проекта верхнего уровня (рядом с `urls.py`) создайте ещё один файл `api.py` с экземпляром `NinjaAPI`:

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

Он должен выглядеть так:

```python
from ninja import NinjaAPI

api = NinjaAPI()

```

Теперь импортируем все роутеры из отдельных приложений и подключим их к основному экземпляру API:

```python hl_lines="2 6 7 8"
from ninja import NinjaAPI
from events.api import router as events_router

api = NinjaAPI()

api.add_router("/events/", events_router)    # You can add a router as an object
api.add_router("/news/", "news.api.router")  #   or by Python path
api.add_router("/blogs/", "blogs.api.router")
```

Теперь добавьте `api` в ваши URL, как обычно, и откройте в браузере `/api/docs` — вы должны увидеть все ваши роутеры, объединённые в единый API:


![Swagger UI Simple Routers](../img/simple-routers-swagger.png)


## Аутентификация роутера

Используйте аргумент `auth`, чтобы применить аутентификатор ко всем операциям, объявленным в роутере:

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

Или через конструктор роутера
```python
router = Router(auth=BasicAuth())
```

## Теги роутера

Вы можете использовать аргумент `tags`, чтобы применить теги ко всем операциям, объявленным в роутере:

```python
api.add_router("/events/", events_router, tags=["events"])
```

Или через конструктор роутера
```python
router = Router(tags=["events"])
```


## Вложенные роутеры

Иногда требуется разделить логику ещё дальше.
**Django Ninja** позволяет включать роутер внутрь другого роутера любое количество раз, а в конце подключить роутер верхнего уровня к основному экземпляру `api`.


По сути, это означает, что `add_router` есть как у экземпляра `api`, так и у экземпляра `router`:



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

Теперь у вас есть следующие эндпоинты

```
/api/add
/api/l1/add
/api/l1/l2/add
/api/l1/l2/l3/add
```

Отлично! Теперь посмотрите автоматически сгенерированную документацию:

![Swagger UI nested routers](../img/nested-routers-swagger.png)

!!! success

    Переходите к следующему разделу **[Аутентификация](authentication.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
