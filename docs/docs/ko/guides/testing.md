---
comments: true
---
# 테스트

**Django Ninja**는 표준 [django testing client](https://docs.djangoproject.com/en/dev/topics/testing/tools/)와 완전히 호환되지만, 미들웨어/URL 파싱 레이어 없이 API만 테스트할 수 있어 테스트 실행이 더 빨라지는 테스팅 클라이언트도 제공합니다.

다음 API를 테스트하려면:
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

Django 테스트 클래스를 사용할 수 있습니다:
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
클라이언트의 요청 메서드에 키워드 인자를 전달하여 request 객체에 임의의 속성을 추가할 수 있습니다:
```python
class HelloTest(TestCase):
    def test_hello(self):
        client = TestClient(router)
        # request.company_id will now be set within the view
        response = client.get("/hello", company_id=1)
```

!!! success

    다음 섹션 **[API 문서](api-docs.md)**로 계속 진행하세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
