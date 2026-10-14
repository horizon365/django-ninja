---
comments: true
---
# Test

**Django Ninja** est entièrement compatible avec le [client de test django](https://docs.djangoproject.com/en/dev/topics/testing/tools/) standard, mais il fournit également un client de test qui vous permet de tester uniquement l'API sans la couche de middleware/analyse d'URL, ce qui rend l'exécution des tests plus rapide.

Pour tester l'API suivante :
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

Vous pouvez utiliser la classe de test Django :
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
Vous pouvez ajouter des attributs arbitraires à l'objet request en passant des arguments mot-clés à la méthode de requête du client :
```python
class HelloTest(TestCase):
    def test_hello(self):
        client = TestClient(router)
        # request.company_id will now be set within the view
        response = client.get("/hello", company_id=1)
```

!!! success

    Poursuivez avec la section suivante **[Documentation de l'API](api-docs.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
