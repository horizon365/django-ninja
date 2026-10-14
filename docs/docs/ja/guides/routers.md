---
comments: true
---
# ルーターによる API の分割

現実の世界では、すべてのロジックを 1 つのファイルにまとめておくことはほぼ不可能です。

**Django Ninja** は、ルーター（routers）を使って API を複数のモジュールに分割するシンプルな方法を提供しています。

次のような構造の Django プロジェクトがあるとします:


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

各 Django アプリケーションに API を追加するには、各アプリケーションに `api.py` モジュールを作成します:

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

次に、`events/api.py` にいくつかのオペレーションを追加してみましょう。コツは、`NinjaAPI` クラスの代わりに **Router** クラスを使用することです:

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

次に、`news` アプリの `news/api.py` でも同じことを行います:

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
同様に `blogs/api.py` も作成します。


最後に、すべてをまとめましょう。
プロジェクトのトップレベルフォルダ（`urls.py` の隣）に、`NinjaAPI` インスタンスを持つ別の `api.py` ファイルを作成します:

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

次のようになります:

```python
from ninja import NinjaAPI

api = NinjaAPI()

```

次に、個々のアプリケーションからすべてのルーターをインポートし、メインの API インスタンスに組み込みます:

```python hl_lines="2 6 7 8"
from ninja import NinjaAPI
from events.api import router as events_router

api = NinjaAPI()

api.add_router("/events/", events_router)    # ルーターはオブジェクトとして追加できます
api.add_router("/news/", "news.api.router")  #   または Python パスでも追加できます
api.add_router("/blogs/", "blogs.api.router")
```

いつもどおり `api` を URL に追加し、ブラウザで `/api/docs` を開くと、すべてのルーターが 1 つの API にまとめられているのがわかります:


![Swagger UI Simple Routers](../img/simple-routers-swagger.png)


## ルーターの認証

`auth` 引数を使用すると、ルーター内で宣言されたすべてのオペレーションに認証クラスを適用できます:

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

またはルーターのコンストラクタでも指定できます
```python
router = Router(auth=BasicAuth())
```

## ルーターのタグ

`tags` 引数を使用すると、ルーター内で宣言されたすべてのオペレーションにタグを適用できます:

```python
api.add_router("/events/", events_router, tags=["events"])
```

またはルーターのコンストラクタでも指定できます
```python
router = Router(tags=["events"])
```


## ネストされたルーター

ロジックをさらに分割する必要がある場合もあります。
**Django Ninja** では、ルーターを別のルーターの中に何度でも組み込むことができ、最後にトップレベルのルーターをメインの `api` インスタンスに組み込めます。

基本的に、これは `api` インスタンスと `router` インスタンスの両方に `add_router` があることを意味します:



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

これで、次のエンドポイントができあがります

```
/api/add
/api/l1/add
/api/l1/l2/add
/api/l1/l2/l3/add
```

素晴らしい！ 自動生成されたドキュメントを確認してみましょう:

![Swagger UI nested routers](../img/nested-routers-swagger.png)

!!! success

    次のセクション **[認証](authentication.md)** に進みましょう

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
