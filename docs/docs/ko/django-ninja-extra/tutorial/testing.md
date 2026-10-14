---
comments: true
---
# **APIController 테스트**

**Django Ninja Extra**는 `pytest`를 사용하여 `ControllerBase` 클래스에 대한 매끄러운 테스트를 제공하는 테스트 클라이언트인 TestClient를 갖고 있습니다.

두 가지 테스트 클라이언트가 있습니다:

- `TestClient`: 동기 라우트 함수용입니다.
- `TestAsyncClient`: 비동기 라우트 함수용입니다.

`TestClient`와 `TestAsyncClient`는 모두 Django Ninja의 `TestClient`를 상속하며, 애플리케이션에 요청을 보내기 위한 기본 기능을 제공합니다.
또한 둘 다 애플리케이션에 요청을 보내기 위한 `get`, `post`, `put`, `patch`, `delete`, `options`와 같은 유사한 메서드들을 갖고 있습니다.

예를 들어, `/users` 엔드포인트에 대한 GET 요청을 테스트하려면 다음과 같이 TestClient를 사용할 수 있습니다:

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
마찬가지로 비동기 라우트 함수를 테스트하려면 다음과 같이 TestAsyncClient를 사용할 수 있습니다:

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
