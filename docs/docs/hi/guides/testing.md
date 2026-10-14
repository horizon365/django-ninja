---
comments: true
---
# Testing

**Django Ninja** standard [django testing client](https://docs.djangoproject.com/en/dev/topics/testing/tools/) के साथ पूरी तरह संगत है, लेकिन यह एक testing client भी प्रदान करता है ताकि आप केवल API का परीक्षण middleware/URL parsing layer के बिना कर सकें, जिससे tests तेज़ी से चलते हैं।

निम्नलिखित API का परीक्षण करने के लिए:
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

आप Django test class का उपयोग कर सकते हैं:
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
आप client की request method को keyword arguments पास करके request object में arbitrary attributes जोड़ सकते हैं:
```python
class HelloTest(TestCase):
    def test_hello(self):
        client = TestClient(router)
        # request.company_id will now be set within the view
        response = client.get("/hello", company_id=1)
```

!!! success

    अगले भाग पर जाएँ **[API documentation](api-docs.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
