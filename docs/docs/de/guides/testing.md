---
comments: true
---
# Testen

**Django Ninja** ist vollständig kompatibel mit dem standardmäßigen [Django-Testclient](https://docs.djangoproject.com/en/dev/topics/testing/tools/), stellt aber auch einen eigenen Testclient bereit, damit Sie nur die API ohne die Middleware-/URL-Parsing-Schicht testen können – so laufen die Tests schneller.

Um die folgende API zu testen:
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

können Sie die Django-Testklasse verwenden:
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
Beliebige Attribute können Sie dem Request-Objekt hinzufügen, indem Sie Schlüsselwortargumente an die Request-Methode des Clients übergeben:
```python
class HelloTest(TestCase):
    def test_hello(self):
        client = TestClient(router)
        # request.company_id will now be set within the view
        response = client.get("/hello", company_id=1)
```

!!! success

    Fahren Sie mit dem nächsten Abschnitt fort: **[API-Dokumentation](api-docs.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
