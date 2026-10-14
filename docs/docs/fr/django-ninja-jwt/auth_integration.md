
Ninja JWT utilise le `HttpBearer` de Django Ninja comme moyen d'authentifier les utilisateurs qui accèdent à vos endpoints d'API.
L'utilisateur authentifié peut être trouvé dans `request.user` ou `request.auth`.

### Authentification des routes - Basée sur les classes

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=JWTAuth())
    def some_endpoint(self):
        ...
```

### Authentification des routes - Basée sur les fonctions

```python
from ninja import router
from ninja_jwt.authentication import JWTAuth

router = router('')

@router.get('/some-endpoint', auth=JWTAuth())
def some_endpoint(request):
    ...
```

Implémentation d'authentification personnalisée
-------
Si vous souhaitez utiliser une implémentation différente de `JWTAuth`, vous devez hériter de `JWTBaseAuthentication`.
Si vous souhaitez utiliser autre chose que `bearer`, consultez la documentation [Django Ninja - Authentification](https://django-ninja.rest-framework.com/tutorial/authentication/).

Exemple :
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

### Authentification asynchrone des routes
Si l'authentification asynchrone des routes vous intéresse, une classe `AsyncJWTAuth` est disponible

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import AsyncJWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=AsyncJWTAuth())
    async def some_endpoint(self):
        ...
```
Remarque : `some_endpoint` doit être asynchrone. Toute fonction d'endpoint marquée avec `AsyncJWTAuth` doit être asynchrone.

!!! warning
    La fonctionnalité asynchrone n'est disponible que pour les versions de Django > 3.0.

!!! success

    Poursuivez avec le chapitre suivant **[Paramètres](settings.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
