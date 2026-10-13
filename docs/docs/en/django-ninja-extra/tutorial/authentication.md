---
comments: true
---
# **Authentication**

**Django Ninja Extra** provides the same API as **Django Ninja** in terms of authorization and authentication, ensuring consistency and ease of use between the two packages.

## **Automatic OpenAPI Schema**

Here is an example where the client needs to pass a header for authentication:

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

## **Global Authentication** 

If you need to protect **all** route methods defined in the `api` and APIController, you can pass the `auth` parameter to the `NinjaExtraAPI` constructor:


```Python
from ninja_extra import NinjaExtraAPI
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaExtraAPI(auth=GlobalAuth())

```
Read more about [authentication](https://django-ninja.cn/guides/authentication/) on django-ninja.

## Async Authentication Classes

Ninja Extra adds async support to all the `Auth` base classes provided by Django Ninja in the `ninja_extra.security` package,
and maintains a similar interface. It is important to note that when using these async authentication classes, the endpoint handler **must** be an async function.

For example, let's rewrite the first authentication example with the `AsyncHttpBearer` class.

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
In the above example, we changed `HttpBearer` to `AsyncHttpBearer` and changed bearer to an `async` endpoint. 
If `AuthBearer` is to be applied to `MyController` **authentication**, then all route handlers under `MyController` must be async route handlers.


## **JWT Authentication**
If you want to use JWT authentication. See [ninja-jwt](https://pypi.org/project/django-ninja-jwt/)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
