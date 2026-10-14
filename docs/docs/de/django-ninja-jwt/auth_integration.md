
Ninja JWT verwendet Djangos Ninjas `HttpBearer` als Möglichkeit, Benutzer zu authentifizieren, die Ihre API-Endpunkte erreichen.
Der authentifizierte Benutzer ist in `request.user` oder `request.auth` zu finden.

### Routenauthentifizierung – Klassenbasiert

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=JWTAuth())
    def some_endpoint(self):
        ...
```

### Routenauthentifizierung – Funktionsbasiert

```python
from ninja import router
from ninja_jwt.authentication import JWTAuth

router = router('')

@router.get('/some-endpoint', auth=JWTAuth())
def some_endpoint(request):
    ...
```

Eigene Authentifizierungs-Implementierung
-------
Wenn Sie eine andere Implementierung von `JWTAuth` verwenden möchten, müssen Sie `JWTBaseAuthentication` subclassen.
Wenn Sie etwas anderes als `bearer` verwenden möchten, lesen Sie mehr über [Django Ninja - Authentication](https://django-ninja.rest-framework.com/tutorial/authentication/).

Beispiel:
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

### Asynchrone Routenauthentifizierung
Wenn Sie an einer asynchronen Routenauthentifizierung interessiert sind, steht eine Klasse `AsyncJWTAuth` zur Verfügung

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import AsyncJWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=AsyncJWTAuth())
    async def some_endpoint(self):
        ...
```
Hinweis: `some_endpoint` muss asynchron sein. Jede Endpoint-Funktion, die mit `AsyncJWTAuth` markiert ist, muss asynchron sein.

!!! warning
    Die asynchrone Funktionalität ist nur für Django-Versionen > 3.0 verfügbar.

!!! success

    Fahren Sie mit dem nächsten Kapitel fort: **[Einstellungen](settings.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
