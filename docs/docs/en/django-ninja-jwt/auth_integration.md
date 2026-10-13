
Ninja JWT uses Django Ninja's `HttpBearer` as a way to authenticate users who reach your API endpoints.
The authenticated user can be found in `request.user` or `request.auth`.

### Route Authentication - Class Based

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=JWTAuth())
    def some_endpoint(self):
        ...
```

### Route Authentication - Function Based

```python
from ninja import router
from ninja_jwt.authentication import JWTAuth

router = router('')

@router.get('/some-endpoint', auth=JWTAuth())
def some_endpoint(request):
    ...
```

Custom Authentication Implementation
-------
If you wish to use a different implementation of `JWTAuth`, you need to subclass `JWTBaseAuthentication`.
If you want to use something other than `bearer`, read more about [Django Ninja - Authentication](https://django-ninja.rest-framework.com/tutorial/authentication/).

Example:
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
If you are interested in asynchronous route authentication, there is an `AsyncJWTAuth` class available

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import AsyncJWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=AsyncJWTAuth())
    async def some_endpoint(self):
        ...
```
Note: `some_endpoint` must be asynchronous. Any endpoint function marked with `AsyncJWTAuth` must be asynchronous.

!!! warning
    The asynchronous functionality is only available for Django versions > 3.0.

!!! success

    Continue to the next chapter **[Settings](settings.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
