---
comments: true
---
# **APIController का Testing**

**Django Ninja Extra** में एक test client, TestClient है, जो `ControllerBase` class के लिए सहज testing प्रदान करने के लिए `pytest` का उपयोग करता है।

दो test clients हैं:

- `TestClient`: Synchronous route functions के लिए।
- `TestAsyncClient`: Asynchronous route functions के लिए।

`TestClient` और `TestAsyncClient` दोनों Django Ninja के `TestClient` से inherit होते हैं, जो application को requests भेजने के लिए basic functionality प्रदान करता है,
और उन सभी में application को requests भेजने के लिए `get`, `post`, `put`, `patch`, `delete`, और `options` जैसे समान methods होते हैं।

उदाहरण के लिए, `/users` endpoint पर एक GET request test करने के लिए, आप TestClient का उपयोग इस प्रकार कर सकते हैं:

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
इसी प्रकार, asynchronous route functions को test करने के लिए, आप TestAsyncClient का उपयोग इस प्रकार कर सकते हैं:

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
