---
comments: true
---
# **Testing APIController**

**Django Ninja Extra** has a test client, TestClient, that uses `pytest` to provide seamless testing for the `ControllerBase` class.

There are two test clients:

- `TestClient`: For synchronous route functions.
- `TestAsyncClient`: For asynchronous route functions.

Both `TestClient` and `TestAsyncClient` inherit from Django Ninja's `TestClient`, which provides basic functionality for making requests to the application,
and they all have similar methods such as `get`, `post`, `put`, `patch`, `delete`, and `options` for making requests to the application.

For example, to test a GET request to the `/users` endpoint, you can use the TestClient as follows:

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
Similarly, for testing asynchronous route functions, you can use TestAsyncClient as follows:

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
