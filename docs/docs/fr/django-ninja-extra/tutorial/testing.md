---
comments: true
---
# **Tester l'APIController**

**Django Ninja Extra** dispose d'un client de test, TestClient, qui utilise `pytest` pour fournir des tests fluides de la classe `ControllerBase`.

Il existe deux clients de test :

- `TestClient` : Pour les fonctions de route synchrones.
- `TestAsyncClient` : Pour les fonctions de route asynchrones.

`TestClient` et `TestAsyncClient` héritent tous deux du `TestClient` de Django Ninja, qui fournit les fonctionnalités de base pour effectuer des requêtes vers l'application,
et ils disposent tous de méthodes similaires telles que `get`, `post`, `put`, `patch`, `delete` et `options` pour effectuer des requêtes vers l'application.

Par exemple, pour tester une requête GET vers l'endpoint `/users`, vous pouvez utiliser le TestClient comme suit :

```python
import pytest
from .controllers import UserController
from ninja_extra.testing import TestClient


@pytest.mark.django_db
class TestMyMathController:
    def test_get_users(self):
        client = TestClient(UserController)
        response = client.get('/users')
        assert response.status_code == 200
        assert response.json()[0] == {
            'first_name': 'Ninja Extra',
            'username': 'django_ninja',
            'email': 'john.doe@gmail.com'
        }

```
De même, pour tester des fonctions de route asynchrones, vous pouvez utiliser le TestAsyncClient comme suit :

```python
from ninja_extra import api_controller, route
from ninja_extra.testing import TestAsyncClient


@api_controller('', tags=['Math'])
class MyMathController:
    @route.get('/add',)
    async def add(self, a: int, b: int):
        """add a to b"""
        return {"result": a - b}

    
class TestMyMathController:
    def test_get_users_async(self):
        client = TestAsyncClient(MyMathController)
        response = client.get('/add', query=dict(a=3, b=5))
        assert response.status_code == 200
        assert response.json() == {"result": -2}

```

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
