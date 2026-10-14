---
comments: true
---
# テスト

**Django Ninja** は標準の [django テストクライアント](https://docs.djangoproject.com/en/dev/topics/testing/tools/)と完全に互換性がありますが、それに加えてミドルウェア/URL パースのレイヤーを経由せずに API だけをテストできるテストクライアントも提供しており、テストの実行が高速になります。

次の API をテストするには:
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

Django のテストクラスを使用できます:
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
クライアントのリクエストメソッドにキーワード引数を渡すことで、リクエストオブジェクトに任意の属性を追加できます:
```python
class HelloTest(TestCase):
    def test_hello(self):
        client = TestClient(router)
        # request.company_id will now be set within the view
        response = client.get("/hello", company_id=1)
```

!!! success

    次のセクション **[API ドキュメント](api-docs.md)** に進みましょう

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
