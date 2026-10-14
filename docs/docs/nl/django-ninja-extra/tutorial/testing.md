---
comments: true
---
# **APIController Testen**

**Django Ninja Extra** heeft een testclient, TestClient, die `pytest` gebruikt om naadloos testen van de klasse `ControllerBase` mogelijk te maken.

Er zijn twee testclients:

- `TestClient`: Voor synchrone routefuncties.
- `TestAsyncClient`: Voor asynchrone routefuncties.

Zowel `TestClient` als `TestAsyncClient` erven van Django Ninja's `TestClient`, die basisfunctionaliteit biedt voor het doen van verzoeken aan de applicatie,
en ze hebben allemaal vergelijkbare methoden zoals `get`, `post`, `put`, `patch`, `delete` en `options` om verzoeken aan de applicatie te doen.

Bijvoorbeeld, om een GET-verzoek naar het endpoint `/users` te testen, kun je de TestClient als volgt gebruiken:

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
Op vergelijkbare wijze kun je voor het testen van asynchrone routefuncties TestAsyncClient als volgt gebruiken:

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
