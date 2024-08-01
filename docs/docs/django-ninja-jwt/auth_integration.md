
Ninja JWT 使用 Django Ninja 的 `HttpBearer` 作为对到达你的 API 端点的用户进行身份验证的一种方式。
经过身份验证的用户可以在 `request.user` 或 `request.auth` 中找到。

### 路由身份验证 - Class Based（基于类的）

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=JWTAuth())
    def some_endpoint(self):
        ...
```

### 路由身份验证 - Function Based（基于函数）

```python
from ninja import router
from ninja_jwt.authentication import JWTAuth

router = router('')

@router.get('/some-endpoint', auth=JWTAuth())
def some_endpoint(request):
    ...
```

自定义身份验证实现
-------
如果你希望使用 `JWTAuth` 的不同实现, 那么你需要从 `JWTBaseAuthentication` 继承。
如果你想使用的不是 `bearer`， 请阅读更多关于 [Django Ninja - Authentication](https://django-ninja.rest-framework.com/tutorial/authentication/)。

示例:
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

### Asynchronous Route Authentication
如果你对异步路由身份验证感兴趣，有 `AsyncJWTAuth` 类可以使用

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import AsyncJWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=AsyncJWTAuth())
    async def some_endpoint(self):
        ...
```
注意：`some_endpoint` 必须是异步的。任何用 `AsyncJWTAuth` 标记的端点函数都必须是异步的。

!!! 警告
    异步功能仅在 Django 版本 > 3.0 时可用。

!!! 大功告成

    继续下一章节 **[配置](settings.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
