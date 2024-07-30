---
comments: true
---
# 测试

**Django Ninja** 与标准的 [django 测试客户端](https://docs.djangoproject.com/en/dev/topics/testing/tools/)完全兼容，但也提供了一个测试客户端，以便于仅测试 API，而无需中间件/URL 解析层，从而使测试运行得更快。

要测试以下 API:
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

你可以使用 Django 测试类：
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
可以通过向客户端请求方法传递关键字参数来向请求对象添加任意属性：
```python
class HelloTest(TestCase):
    def test_hello(self):
        client = TestClient(router)
        # request.company_id will now be set within the view
        response = client.get("/hello", company_id=1)
```

!!! 大功告成

    继续下一小节 **[API 文档](api-docs.md)**

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
