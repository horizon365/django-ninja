---
comments: true
---
# अपनी API को routers के साथ विभाजित करना

वास्तविक दुनिया में, सारी logic को एक ही file में रखना लगभग असंभव है।

**Django Ninja** routers का उपयोग करके अपनी API को कई modules में विभाजित करने का एक सरल तरीका प्रदान करता है।

मान लीजिए आपके पास निम्नलिखित संरचना वाला एक Django project है:


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

प्रत्येक Django application में एक API जोड़ने के लिए, प्रत्येक application में एक `api.py` module बनाएँ:

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

अब आइए `events/api.py` में कुछ operations जोड़ें। Trick यह है कि `NinjaAPI` class का उपयोग करने के बजाय, आप **Router** class का उपयोग करते हैं:

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

फिर `news` app के `news/api.py` के लिए भी वही करें:

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
और `blogs/api.py` के लिए भी।


अंत में, आइए इन सबको एक साथ जोड़ें।
अपने top-level project folder में (`urls.py` के बगल में), एक `NinjaAPI` instance के साथ एक और `api.py` file बनाएँ:

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

यह इस तरह दिखना चाहिए:

```python
from ninja import NinjaAPI

api = NinjaAPI()

```

अब हम सभी routers को अलग-अलग applications से import करते हैं और उन्हें मुख्य API instance में शामिल करते हैं:

```python hl_lines="2 6 7 8"
from ninja import NinjaAPI
from events.api import router as events_router

api = NinjaAPI()

api.add_router("/events/", events_router)    # You can add a router as an object
api.add_router("/news/", "news.api.router")  #   or by Python path
api.add_router("/blogs/", "blogs.api.router")
```

अब, हमेशा की तरह `api` को अपने URLs में जोड़ें और browser में `/api/docs` खोलें, आपको आपके सभी routers एक single API में संयुक्त दिखाई देंगे:


![Swagger UI Simple Routers](../img/simple-routers-swagger.png)


## Router authentication

किसी router में घोषित सभी operations पर एक authenticator लागू करने के लिए `auth` argument का उपयोग करें:

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

या router constructor का उपयोग करते हुए
```python
router = Router(auth=BasicAuth())
```

## Router tags

किसी router में घोषित सभी operations पर tags लागू करने के लिए आप `tags` argument का उपयोग कर सकते हैं:

```python
api.add_router("/events/", events_router, tags=["events"])
```

या router constructor का उपयोग करते हुए
```python
router = Router(tags=["events"])
```


## Nested routers

कभी-कभी आपको logic को और भी विभाजित करने की आवश्यकता होती है।
**Django Ninja** आपको एक router को दूसरे router के भीतर जितनी बार चाहें include करने देता है, और अंत में top-level router को मुख्य `api` instance में include करने देता है।


मूल रूप से, इसका अर्थ है कि आपके पास `api` instance और `router` instance दोनों पर `add_router` है:



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

अब आपके पास निम्नलिखित endpoints हैं

```
/api/add
/api/l1/add
/api/l1/l2/add
/api/l1/l2/l3/add
```

बहुत बढ़िया! अब auto-generated दस्तावेज़ीकरण देखने जाएँ:

![Swagger UI nested routers](../img/nested-routers-swagger.png)

!!! success

    अगले भाग पर जाएँ **[Authentication](authentication.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
