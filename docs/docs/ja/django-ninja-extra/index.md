![Test](https://github.com/eadwinCode/django-ninja-extra/workflows/Test/badge.svg)
[![PyPI version](https://badge.fury.io/py/django-ninja-extra.svg)](https://badge.fury.io/py/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/v/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/pyversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/djversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![Codecov](https://img.shields.io/codecov/c/gh/eadwinCode/django-ninja-extra)](https://codecov.io/gh/eadwinCode/django-ninja-extra)
[![Downloads](https://pepy.tech/badge/django-ninja-extra)](https://pepy.tech/project/django-ninja-extra)

# Django Ninja Extra ドキュメント

**Django Ninja Extra** は、**クラスベース** のアプローチと追加機能を提供し、[**Django Ninja**](https://django-ninja.cn) を使った RESTful API 開発を加速させます。

**主な特徴：**

**Django-Ninja** の全機能：

- **シンプル**： 使いやすく直感的であるよう設計されています。
- **高速な実行**： **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** と **<a href="/async-support/">async support</a>** のおかげで、非常に高いパフォーマンスを発揮します。
- **高速なコーディング**： 型ヒントと自動ドキュメント生成により、ビジネスロジックに集中できます。
- **標準準拠**： 標準に基づいています：**OpenAPI**（旧 Swagger）と **JSON Schema**。
- **Django フレンドリー**： （言うまでもなく）Django のコアと ORM と緊密に統合されています。

さらに **Extra**：

- **クラスベース**： API をクラスベースの方法で設計できます。
- **パーミッション**： route レベルまたはコントローラレベルで定義されたパーミッションと認証により、エンドポイントへのアクセスを簡単に保護できます。
- **依存性注入**： コントローラクラスは Python の [**Injector** ](https://injector.readthedocs.io/en/latest/) や [**django_injector**](https://github.com/blubber/django_injector) の使用をサポートしています。これにより、API の依存サービスを APIController クラスに注入し、必要な場所で使用できます。

---

### バージョン要件
- Python >= 3.6
- django >= 2.1 
- pydantic >= 1.6 
- Django-Ninja >= 0.16.1


完全なドキュメントについては、[このリンクをご覧ください](https://django-ninja.cn/django-ninja-extra/)。

## インストール

```
pip install django-ninja-extra
```
インストール後、`ninja_extra` を `INSTALLED_APPS` に追加してください

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```

## 使い方

Django プロジェクトで、`urls.py` の隣に新しい `api.py` ファイルを作成します：

```Python
from ninja_extra import NinjaExtraAPI, api_controller, http_get

api = NinjaExtraAPI()

# Function-based definition
@api.get("/add", tags=['Math'])
def add(request, a: int, b: int):
    return {"result": a + b}

# Class-based definition
@api_controller('/', tags=['Math'], permissions=[])
class MathAPI:

    @http_get('/subtract',)
    def subtract(self, a: int, b: int):
        """Subtracts a from b"""
        return {"result": a - b}

    @http_get('/divide',)
    def divide(self, a: int, b: int):
        """Divides a by b"""
        return {"result": a / b}
    
    @http_get('/multiple',)
    def multiple(self, a: int, b: int):
        """Multiples a with b"""
        return {"result": a * b}
    
api.register_controllers(
    MathAPI
)
```

次に `urls.py` に移動し、以下を追加します：

```Python
...
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # <---------- !
]
```

### インタラクティブな API ドキュメント

<a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a> にアクセスしてみてください

自動生成されたインタラクティブな API ドキュメント（<a href="https://github.com/swagger-api/swagger-ui" target="_blank">Swagger UI</a> による）が表示されます：

![Swagger UI](images/ui_swagger_preview_readme.gif)

## チュートリアル
- [django-ninja - django-ninja-extra のパーミッション、コントローラ、スロットリングを使う！](https://www.youtube.com/watch?v=yQqig-c2dd4) - django-ninja-extra のパーミッション、コントローラ、スロットリングの使い方を学ぶ
- [BookStore API](https://github.com/eadwinCode/bookstoreapi) - django-ninja-extra を ninja schema および ninja-jwt と組み合わせて使う方法を示すサンプルプロジェクト

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
