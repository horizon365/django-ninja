---
comments: true
---
# Testing

**Django Ninja** sepenuhnya kompatibel dengan [django testing client](https://docs.djangoproject.com/en/dev/topics/testing/tools/) standar, tetapi juga menyediakan testing client agar Anda dapat menguji hanya API-nya tanpa lapisan middleware/parsing URL, sehingga test berjalan lebih cepat.

Untuk menguji API berikut:
```python
from ninja import NinjaAPI, Schema

api = NinjaAPI()
router = Router()

class HelloResponse(Schema):
    msg: str
    
@router.get("/hello", response=HelloResponse)
def hello(request):
    return {"msg": "Hello World"}

api.add_router("", router)
```

Anda dapat menggunakan test class Django:
```python
from django.test import TestCase
from ninja.testing import TestClient

class HelloTest(TestCase):
    def test_hello(self):
        client = TestClient(router)
        response = client.get("/hello")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"msg": "Hello World"})
```
Anda dapat menambahkan atribut arbitrer ke objek request dengan meneruskan keyword arguments ke method request milik client:
```python
class HelloTest(TestCase):
    def test_hello(self):
        client = TestClient(router)
        # request.company_id will now be set within the view
        response = client.get("/hello", company_id=1)
```

!!! success

    Lanjutkan ke bagian berikutnya **[Dokumentasi API](api-docs.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
