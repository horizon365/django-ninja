---
comments: true
---
# **認証**

**Django Ninja Extra** は、認可・認証の面で **Django Ninja** と同じ API を提供しており、両パッケージ間の一貫性と使いやすさを保証しています。

## **自動 OpenAPI Schema**

クライアントが認証用のヘッダーを渡す必要がある例を示します：

`Authorization: Bearer supersecret`

```Python
from ninja.security import HttpBearer
from ninja_extra import api_controller, route
from ninja.constants import NOT_SET


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token

@api_controller(tags=['My Operations'], auth=NOT_SET, permissions=[])
class MyController:
    @route.get("/bearer", auth=AuthBearer())
    def bearer(self):
        return {"token": self.context.request.auth}

```

## **グローバル認証** 

`api` と APIController に定義された **すべての** ルートメソッドを保護する必要がある場合は、`NinjaExtraAPI` コンストラクタに `auth` パラメータを渡します：


```Python
from ninja_extra import NinjaExtraAPI
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaExtraAPI(auth=GlobalAuth())

```
django-ninja における [認証](https://django-ninja.cn/guides/authentication/) について詳しく読むことができます。

## 非同期認証クラス

Ninja Extra は、Django Ninja が提供するすべての `Auth` 基底クラスに `ninja_extra.security` パッケージ内で非同期サポートを追加しており、同様のインターフェースを維持しています。重要なのは、これらの非同期認証クラスを使用する場合、エンドポイントハンドラは **必ず** 非同期関数でなければならないという点です。

たとえば、最初の認証の例を `AsyncHttpBearer` クラスで書き直してみましょう。

```Python
from ninja_extra import api_controller, route
from ninja_extra.security import AsyncHttpBearer
from ninja.constants import NOT_SET


class AuthBearer(AsyncHttpBearer):
    async def authenticate(self, request, token):
        # await some actions
        if token == "supersecret":
            return token


@api_controller(tags=['My Operations'], auth=NOT_SET, permissions=[])
class MyController:
    @route.get("/bearer", auth=AuthBearer())
    async def bearer(self):
        return {"token": self.context.request.auth}

```
上の例では、`HttpBearer` を `AsyncHttpBearer` に変更し、bearer を `async` エンドポイントに変更しました。 
`AuthBearer` を `MyController` の **認証** に適用する場合は、`MyController` 配下のすべてのルートハンドラが非同期ルートハンドラでなければなりません。


## **JWT 認証**
JWT 認証を使用したい場合は、[ninja-jwt](https://pypi.org/project/django-ninja-jwt/) を参照してください。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
