---
comments: true
---
# 路由器

现实世界的应用程序几乎不可能将所有逻辑都放入单个文件中。 

**Django Ninja** 提供了一种简单的方法，可以使用路由器将您的 API 拆分为多个模块。

假设您有一个 Django 项目，结构如下：


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

要向每个 Django 应用程序添加 API，在每个应用程序中创建一个 `api.py` 模块:

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

现在让我们在 `events/api.py` 中添加一些操作。诀窍是，您不是使用 `NinjaAPI` 类，而是使用 **Router** 类:

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

然后对 `news` app 的 `news/api.py` 也进行同样的操作:

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
然后还有`blogs/api.py`。


最后，让我们将它们组合在一起。
在您的顶级项目文件夹 (在 `urls.py` 旁边)，创建另一个带有 `NinjaAPI` 实例的 `api.py` 文件 :

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

它应该看起来像这样：

```python
from ninja import NinjaAPI

api = NinjaAPI()

```

现在我们从各个应用程序导入所有路由器，并将它们包含到主 API 实例中：

```python hl_lines="2 6 7 8"
from ninja import NinjaAPI
from events.api import router as events_router

api = NinjaAPI()

api.add_router("/events/", events_router)    # You can add a router as an object
api.add_router("/news/", "news.api.router")  #   or by Python path
api.add_router("/blogs/", "blogs.api.router")
```

现在，像往常一样将 `api` 添加到您的 URL 中，并在 `/api/docs` 打开您的浏览器， 您应该看到您所有的路由器组合成一个单一的 API：


![Swagger UI Simple Routers](../img/simple-routers-swagger.png)


## 路由器认证

使用 `auth` 参数将认证器应用于路由器声明的所有操作：

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

或者使用路由器构造函数
```python
router = Router(auth=BasicAuth())
```

## 路由器标签

您可以使用 `tags` 参数将标签应用于路由器声明的所有操作：

```python
api.add_router("/events/", events_router, tags=["events"])
```

或者使用路由器构造函数
```python
router = Router(tags=["events"])
```


## 嵌套路由器

有时您还需要将逻辑进一步细分。
**Django Ninja** 使您可以将一个路由器包含在另一个路由器中任意多次，最后将顶级路由器包含在主 `api` 实例中。


基本上，这意味着您在 `api` 实例和 `router` 实例上都有 `add_router` :



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

现在您有以下端点

```
/api/add
/api/l1/add
/api/l1/l2/add
/api/l1/l2/l3/add
```

太棒了！现在去看看自动生成的文档：

![Swagger UI 嵌套路由](../img/nested-routers-swagger.png)
