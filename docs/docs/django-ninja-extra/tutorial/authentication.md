---
comments: true
---
# **鉴权**

**Django Ninja Extra** 在授权和认证方面提供了与 **Django Ninja** 相同的 API, 确保了两个包之间的一致性和易用性。

## **自动 OpenAPI 模式**

这里有一个示例，其中客户端为了进行认证，需要传递一个头部：

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

## **全局鉴权** 

如果你需要保护在  `api` 和 APIController 中定义的 **所有** 路由方法，你可以将 `auth` 参数传递给 `NinjaExtraAPI` 构造函数:


```Python
from ninja_extra import NinjaExtraAPI
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaExtraAPI(auth=GlobalAuth())

```
在 django-ninja 上阅读更多关于 [鉴权](https://django-ninja.cn/guides/authentication/)的信息。

## 异步认证类

Ninja Extra 在 `ninja_extra.security` 包中为 Django Ninja 提供的所有 `Auth` 基类添加了异步支持，
并且保持了类似的接口。重要的是要注意，当使用这些异步认证类时，端点处理程序 **必须** 是异步函数。

例如，让我们用 `AsyncHttpBearer` 类重写第一个认证示例。

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
在上面的示例中，我们将 `HttpBearer` 改为 `AsyncHttpBearer` 并将 bearer 改成 `async` 端点. 
如果 `AuthBearer` 要应用于 `MyController` **鉴权**， 那么 `MyController` 下的所有路由处理程序都必须是异步路由处理程序。


## **JWT 鉴权**
如果你想使用 JWT 认证。请参阅 [ninja-jwt](https://pypi.org/project/django-ninja-jwt/)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
