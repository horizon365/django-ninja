---
comments: true
---
# チュートリアル - 最初の一歩

このチュートリアルでは、**Django Ninja** の機能のほとんどを使う方法を紹介します。

このチュートリアルでは、<a href="https://www.djangoproject.com/" target="_blank">Django フレームワーク</a> の基礎、たとえばプロジェクトの作成方法や実行方法などを知っていることを前提としています。

## インストール

```console
pip install django-ninja
```

!!! note

    これは必須ではありませんが、`ninja` を `INSTALLED_APPS` に追加することもできます。
    その場合、OpenAPI/Swagger UI（または Redoc）はバンドルされた JavaScript パッケージから読み込まれます（こちらの方が高速です）（そうしない場合、JavaScript バンドルは CDN から提供されます）

## Django プロジェクトを作成する

新しい Django プロジェクトを開始します（すでに Django プロジェクトを持っている場合は、次のステップに進んでください）。

```
django-admin startproject myproject
```

## API を作成する

API 用のモジュールを作成しましょう。Django プロジェクトのルートにある `urls.py` と同じ場所に `api.py` ファイルを作成します：

```python
from ninja import NinjaAPI

api = NinjaAPI()
```

次に `urls.py` に移動して、次のように追加します：

```python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## 最初の操作

**Django Ninja** には、各 HTTP メソッド（`GET`、`POST`、
`PUT` など）に対応するデコレーターが同梱されています。`api.py` ファイルに、シンプルな "hello world" 操作を追加してみましょう。

```python hl_lines="5-7"
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"
```

次にブラウザーで <a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a> を開くと、シンプルな JSON レスポンスが返されます：
```json
"Hello world"
```

!!! success

    次の章 **[入力パラメータの扱い](step2.md)** に進みましょう。
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
