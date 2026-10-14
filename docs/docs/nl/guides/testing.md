---
comments: true
---
# Testen

**Django Ninja** is volledig compatibel met de standaard [django testing client](https://docs.djangoproject.com/en/dev/topics/testing/tools/), maar biedt ook een testing client waarmee je alleen de API kunt testen zonder de middleware/URL parsing laag, waardoor de tests sneller draaien.

Om de volgende API te testen:
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

Je kunt de Django test class gebruiken:
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
Je kunt willekeurige attributen toevoegen aan het request object door keyword argumenten door te geven aan de request methode van de client:
```python
class HelloTest(TestCase):
    def test_hello(self):
        client = TestClient(router)
        # request.company_id will now be set within the view
        response = client.get("/hello", company_id=1)
```

!!! success

    Ga verder naar de volgende sectie **[API-documentatie](api-docs.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
