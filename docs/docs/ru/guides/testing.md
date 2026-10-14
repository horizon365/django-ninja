---
comments: true
---
# Тестирование

**Django Ninja** полностью совместим со стандартным [тестовым клиентом Django](https://docs.djangoproject.com/en/dev/topics/testing/tools/), но также предоставляет собственный тестовый клиент, позволяющий тестировать только API без слоя middleware/разбора URL, что делает тесты быстрее.

Чтобы протестировать следующий API:
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

Вы можете использовать тестовый класс Django:
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
Вы можете добавлять произвольные атрибуты к объекту запроса, передавая именованные аргументы методу запроса клиента:
```python
class HelloTest(TestCase):
    def test_hello(self):
        client = TestClient(router)
        # request.company_id will now be set within the view
        response = client.get("/hello", company_id=1)
```

!!! success

    Переходите к следующему разделу **[Документация API](api-docs.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
