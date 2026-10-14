---
comments: true
---
# **Тестирование APIController**

**Django Ninja Extra** имеет тестовый клиент TestClient, который использует `pytest` для обеспечения бесшовного тестирования класса `ControllerBase`.

Существует два тестовых клиента:

- `TestClient`: для синхронных функций маршрутов.
- `TestAsyncClient`: для асинхронных функций маршрутов.

И `TestClient`, и `TestAsyncClient` наследуются от `TestClient` из Django Ninja, который предоставляет базовую функциональность для отправки запросов приложению,
и оба имеют похожие методы, такие как `get`, `post`, `put`, `patch`, `delete` и `options`, для отправки запросов приложению.

Например, чтобы протестировать GET-запрос к эндпоинту `/users`, вы можете использовать TestClient следующим образом:

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
Аналогично, для тестирования асинхронных функций маршрутов вы можете использовать TestAsyncClient следующим образом:

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
