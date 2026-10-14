---
comments: true
---
# **Menguji APIController**

**Django Ninja Extra** memiliki test client, TestClient, yang menggunakan `pytest` untuk menyediakan pengujian yang mulus bagi kelas `ControllerBase`.

Terdapat dua test client:

- `TestClient`: Untuk fungsi route synchronous.
- `TestAsyncClient`: Untuk fungsi route asynchronous.

Baik `TestClient` maupun `TestAsyncClient` mewarisi dari `TestClient` milik Django Ninja yang menyediakan fungsionalitas dasar untuk membuat request ke aplikasi,
dan keduanya memiliki method serupa seperti `get`, `post`, `put`, `patch`, `delete`, dan `options` untuk membuat request ke aplikasi.

Sebagai contoh, untuk menguji request GET ke endpoint `/users`, Anda dapat menggunakan TestClient sebagai berikut:

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
Serupa dengan itu, untuk menguji fungsi route asynchronous, Anda dapat menggunakan TestAsyncClient sebagai berikut:

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
