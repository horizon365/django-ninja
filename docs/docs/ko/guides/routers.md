---
comments: true
---
# 라우터로 API 분할하기

실제 환경에서는 모든 로직을 단일 파일에 유지하는 것이 거의 불가능합니다. 

**Django Ninja**는 라우터를 사용해 API를 여러 모듈로 분할하는 간단한 방법을 제공합니다.

다음과 같은 구조의 Django 프로젝트가 있다고 가정해 보겠습니다:


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

각 Django 애플리케이션에 API를 추가하려면 각 애플리케이션에 `api.py` 모듈을 생성하세요:

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

이제 `events/api.py`에 몇 가지 operation을 추가해 보겠습니다. 요령은 `NinjaAPI` 클래스 대신 **Router** 클래스를 사용하는 것입니다:

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

그다음 `news` 앱의 `news/api.py`에도 동일하게 적용합니다:

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
그리고 `blogs/api.py`에도 마찬가지입니다.


마지막으로 이것을 하나로 합쳐 보겠습니다.
최상위 프로젝트 폴더(`urls.py` 옆)에 `NinjaAPI` 인스턴스를 담은 또 다른 `api.py` 파일을 생성합니다:

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

다음과 같이 작성하면 됩니다:

```python
from ninja import NinjaAPI

api = NinjaAPI()

```

이제 각 애플리케이션의 모든 라우터를 임포트하여 메인 API 인스턴스에 포함시킵니다:

```python hl_lines="2 6 7 8"
from ninja import NinjaAPI
from events.api import router as events_router

api = NinjaAPI()

api.add_router("/events/", events_router)    # You can add a router as an object
api.add_router("/news/", "news.api.router")  #   or by Python path
api.add_router("/blogs/", "blogs.api.router")
```

이제 평소처럼 `api`를 URL에 추가하고 브라우저에서 `/api/docs`를 열면, 모든 라우터가 하나의 API로 결합된 것을 볼 수 있습니다:


![Swagger UI Simple Routers](../img/simple-routers-swagger.png)


## 라우터 인증

`auth` 인자를 사용하여 라우터 내에 선언된 모든 operation에 인증기를 적용할 수 있습니다:

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

또는 라우터 생성자 사용
```python
router = Router(auth=BasicAuth())
```

## 라우터 태그

`tags` 인자를 사용하여 라우터 내에 선언된 모든 operation에 태그를 적용할 수 있습니다:

```python
api.add_router("/events/", events_router, tags=["events"])
```

또는 라우터 생성자 사용
```python
router = Router(tags=["events"])
```


## 중첩 라우터

때로는 로직을 더 분할해야 하는 경우도 있습니다.
**Django Ninja**는 라우터 안에 라우터를 원하는 만큼 포함시킬 수 있게 해주며, 최종적으로 최상위 라우터를 메인 `api` 인스턴스에 포함시킵니다.


기본적으로 `api` 인스턴스와 `router` 인스턴스 모두에 `add_router`가 있다는 의미입니다:



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

이제 다음과 같은 endpoint들이 생깁니다

```
/api/add
/api/l1/add
/api/l1/l2/add
/api/l1/l2/l3/add
```

멋지죠! 이제 자동 생성된 문서를 확인해 보세요:

![Swagger UI nested routers](../img/nested-routers-swagger.png)

!!! success

    다음 섹션 **[인증](authentication.md)**으로 계속 진행하세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
