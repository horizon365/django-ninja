---
comments: true
---
# **APIController のテスト**

**Django Ninja Extra** にはテストクライアント TestClient があり、`pytest` を使って `ControllerBase` クラスのシームレスなテストを提供します。

テストクライアントには 2 種類あります：

- `TestClient`: 同期ルート関数用。
- `TestAsyncClient`: 非同期ルート関数用。

`TestClient` と `TestAsyncClient` はどちらも Django Ninja の `TestClient` を継承しており、アプリケーションにリクエストを送るための基本機能を備えています。
また、どちらにもアプリケーションへのリクエストを行うための `get`、`post`、`put`、`patch`、`delete`、`options` といった同様のメソッドがあります。

たとえば、`/users` エンドポイントへの GET リクエストをテストするには、TestClient を次のように使います：

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
同様に、非同期ルート関数のテストには TestAsyncClient を次のように使います：

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
