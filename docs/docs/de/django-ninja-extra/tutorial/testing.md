---
comments: true
---
# **APIController testen**

**Django Ninja Extra** verfügt über einen Testclient, TestClient, der `pytest` verwendet, um nahtloses Testen für die Klasse `ControllerBase` bereitzustellen.

Es gibt zwei Testclients:

- `TestClient`: Für synchrone Routenfunktionen.
- `TestAsyncClient`: Für asynchrone Routenfunktionen.

Sowohl `TestClient` als auch `TestAsyncClient` erben von Djangos Ninjas `TestClient`, der grundlegende Funktionalität für Requests an die Anwendung bereitstellt,
und alle verfügen über ähnliche Methoden wie `get`, `post`, `put`, `patch`, `delete` und `options`, um Requests an die Anwendung zu senden.

Um beispielsweise einen GET-Request an den Endpoint `/users` zu testen, können Sie den TestClient wie folgt verwenden:

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
Analog können Sie für das Testen asynchroner Routenfunktionen den TestAsyncClient wie folgt verwenden:

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
