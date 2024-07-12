---
comments: true
---
# **测试 APIController**

**Django Ninja Extra** 有一个测试客户端 TestClient，它使用 `pytest` 为 `ControllerBase` 类提供无缝测试。

有两个测试客户端：

- `TestClient`: 用于同步路由函数。
- `TestAsyncClient`: 用于异步路由函数。

`TestClient` 和 `TestAsyncClient` 都继承自 Django Ninja 的  `TestClient` 该类为向应用程序发出请求提供基本功能，
并且它们都有类似的方法如 `get`, `post`, `put`, `patch`, `delete` 和 `options`， 用于向应用程序发出请求。

例如，要测试对 `/users` 端点的 GET 请求, 你可以使用如下 TestClient :

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
类似地，对于测试异步路由函数，你可以如下使用 TestAsyncClient：

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

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
