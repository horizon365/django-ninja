
Ninja JWT использует `HttpBearer` из Django Ninja как способ аутентификации пользователей, обращающихся к вашим API-эндпоинтам.
Аутентифицированный пользователь доступен в `request.user` или `request.auth`.

### Аутентификация маршрута — на основе классов

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=JWTAuth())
    def some_endpoint(self):
        ...
```

### Аутентификация маршрута — на основе функций

```python
from ninja import router
from ninja_jwt.authentication import JWTAuth

router = router('')

@router.get('/some-endpoint', auth=JWTAuth())
def some_endpoint(request):
    ...
```

Пользовательская реализация аутентификации
-------
Если вы хотите использовать другую реализацию `JWTAuth`, вам нужно создать подкласс `JWTBaseAuthentication`.
Если вы хотите использовать что-то иное, кроме `bearer`, прочитайте больше о [Django Ninja — Authentication](https://django-ninja.rest-framework.com/tutorial/authentication/).

Пример:
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

### Асинхронная аутентификация маршрутов
Если вас интересует асинхронная аутентификация маршрутов, доступен класс `AsyncJWTAuth`

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import AsyncJWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=AsyncJWTAuth())
    async def some_endpoint(self):
        ...
```
Примечание: `some_endpoint` должен быть асинхронным. Любая функция эндпоинта, помеченная `AsyncJWTAuth`, должна быть асинхронной.

!!! warning
    Асинхронная функциональность доступна только для версий Django > 3.0.

!!! success

    Перейдите к следующей главе **[Настройки](settings.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
