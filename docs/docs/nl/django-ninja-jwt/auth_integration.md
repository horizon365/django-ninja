
Ninja JWT gebruikt de `HttpBearer` van Django Ninja als manier om gebruikers te authenticeren die je API-endpoints bereiken.
De geauthenticeerde gebruiker is te vinden in `request.user` of `request.auth`.

### Route-authenticatie - Klasse-gebaseerd

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=JWTAuth())
    def some_endpoint(self):
        ...
```

### Route-authenticatie - Functie-gebaseerd

```python
from ninja import router
from ninja_jwt.authentication import JWTAuth

router = router('')

@router.get('/some-endpoint', auth=JWTAuth())
def some_endpoint(request):
    ...
```

Aangepaste authenticatie-implementatie
-------
Als je een andere implementatie van `JWTAuth` wilt gebruiken, moet je een subklasse van `JWTBaseAuthentication` maken.
Als je iets anders dan `bearer` wilt gebruiken, lees dan meer over [Django Ninja - Authenticatie](https://django-ninja.rest-framework.com/tutorial/authentication/).

Voorbeeld:
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

### Asynchrone route-authenticatie
Als je geïnteresseerd bent in asynchrone route-authenticatie, is er een klasse `AsyncJWTAuth` beschikbaar

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import AsyncJWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=AsyncJWTAuth())
    async def some_endpoint(self):
        ...
```
Let op: `some_endpoint` moet asynchroon zijn. Elke endpoint-functie die met `AsyncJWTAuth` is gemarkeerd, moet asynchroon zijn.

!!! warning
    De asynchrone functionaliteit is alleen beschikbaar voor Django-versies > 3.0.

!!! success

    Ga verder naar het volgende hoofdstuk **[Instellingen](settings.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
