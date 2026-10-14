
Ninja JWT は、Django Ninja の `HttpBearer` を、API エンドポイントに到達したユーザーを認証する手段として使用します。
認証されたユーザーは `request.user` または `request.auth` から取得できます。

### ルート認証 - クラスベース

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=JWTAuth())
    def some_endpoint(self):
        ...
```

### ルート認証 - 関数ベース

```python
from ninja import router
from ninja_jwt.authentication import JWTAuth

router = router('')

@router.get('/some-endpoint', auth=JWTAuth())
def some_endpoint(request):
    ...
```

カスタム認証の実装
-------
`JWTAuth` の別の実装を使いたい場合は、`JWTBaseAuthentication` をサブクラス化する必要があります。
`bearer` 以外のものを使いたい場合は、[Django Ninja - 認証](https://django-ninja.rest-framework.com/tutorial/authentication/) を参照してください。

例：
```python
from ninja.security import APIKeyHeader
from ninja_jwt.authentication import JWTBaseAuthentication
from ninja import router

class ApiKey(APIKeyHeader, JWTBaseAuthentication):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        return self.jwt_authenticate(request, token=key)


header_key = ApiKey()
router = router('')

@router.get("/headerkey", auth=header_key)
def apikey(request):
    return f"Token = {request.auth}"

```

### 非同期ルート認証
非同期のルート認証に興味がある場合は、`AsyncJWTAuth` クラスが利用可能です

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import AsyncJWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=AsyncJWTAuth())
    async def some_endpoint(self):
        ...
```
注意： `some_endpoint` は非同期でなければなりません。`AsyncJWTAuth` を付けたエンドポイント関数はすべて非同期でなければなりません。

!!! warning
    非同期機能は Django バージョン 3.0 以上でのみ利用可能です。

!!! success

    次の章 **[設定](settings.md)** に進みましょう。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
