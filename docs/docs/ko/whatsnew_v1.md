---
comments: true
---
# Django Ninja 1.0에 오신 것을 환영합니다


시작하려면 다음 명령어로 최신 버전을 설치하세요:
```
pip install -U django-ninja
```

django-ninja v1은 Python 3.7 이상과 호환됩니다.


Django Ninja 0.x 시리즈도 여전히 지원되지만, 보안 업데이트와 중요 버그 수정만 제공됩니다.


✨ Django Ninja 1.0의 새로운 기능

## Pydantic2 지원

Pydantic 버전 2는 Rust로 재작성되었으며 다음과 같은 많은 개선 사항과 기능이 포함되어 있습니다:

 - 더 안전한 타입.
 - 더 나은 확장성.
 - 더 나은 성능.

우리의 테스트에 따르면, 평균적인 프로젝트는 약 10%의 성능 향상을 얻을 수 있으며, 일부 엣지 파싱/직렬화 시나리오에서는 4배의 성능 향상을 얻을 수 있습니다.
반면, breaking change가 도입되었습니다 — pydantic 1과 2는 완전히 호환되지 않습니다 — 하지만 우리는 이 전환을 최대한 쉽게 만들려고 노력했습니다.
'Schema' 클래스를 사용하셨다면 ninja v1로의 마이그레이션은 간단할 것입니다. 그렇지 않다면 [pydantic 마이그레이션 가이드](https://pydantic.com.cn/migration/)를 따라 주세요.


pydantic2가 제공하는 몇 가지 새로운 기능

### pydantic context

Pydantic은 이제 검증(validation)과 직렬화 중에 context를 지원하며, Django Ninja는 request와 response 처리 중에 "request" 객체를 전달합니다.
```Python hl_lines="6 7"
class Payload(Schema):
    id: int
    name: str
    request_path: str

    @staticmethod
    def resolve_request_path(data, context):
        request = context["request"]
        return request.get_full_path()

```

response 단계에서는 "response_code"도 context에 전달됩니다.

## Schema.Meta

Pydantic은 이제 BaseModel.Config 클래스를 deprecated 처리했습니다. 하지만 다른 모든 Django 부분과 일관성을 유지하기 위해, 우리는 ModelSchema를 위한 "Meta" 클래스를 도입했습니다 — Django의 ModelForms와 유사하게 동작합니다:
```Python hl_lines="2 4"
class TxItem(ModelSchema):
    class Meta:
        model = Transaction
        fields = ["id", "account", "amount", "timestamp"]

```

("Config" 클래스는 여전히 지원되지만, 이제는 deprecated 되었습니다)


## 더 짧고 깔끔한 파라미터 문법

```python
@api.post('/some')
def some_form(request, username: Form[str], password: Form[str]):
    return True
```

대신에 (기존에는)

```python
@api.post('/some')
def some_form(request, username: str = Form(...), password: str = Form(...)):
    return True
```

또는

```python
@api.post('/some')
def some_form(request, data: Form[AuthSchema]):
    return True
```


대신에 (기존에는)

```python
@api.post('/some')
def some_form(request, data: AuthSchema = Form(...)):
    return True
```



그리고 에디터의 모든 자동 완성 기능도 지원합니다.


반면에, **기존 문법도 여전히 지원되므로**, 최신 django-ninja 버전으로 프로젝트를 손쉽게 이전할 수 있습니다.


#### + Annotated

typing.Annotated도 이제 지원됩니다:

```Python
@api.get("/annotated")
def annotated(request, data: Annotated[SomeData, Form()]):
    return {"data": data.dict()}

```


## Async auth 지원

이제 async 인증기(authenticator)가 지원됩니다. `authenticate` 메서드에 `async`를 추가하기만 하면 됩니다:

```Python
class Auth(HttpBearer):
    async def authenticate(self, request, token):
        await asyncio.sleep(1)
        if token == "secret":
            return token

```


## 변경된 CSRF 동작


cookie 기반 인증을 사용하는 경우 더 이상 `csrf=True`가 필요하지 않습니다. 대신 CSRF 방지 기능이 자동으로 활성화됩니다. 이를 통해 CSRF가 적용된 인증기와 cookie가 필요 없는 다른 방식들을 혼합하여 사용할 수도 있습니다:

```Python
api = NinjaAPI(auth=[django_auth, Auth()])
```


## Documentation

문서 뷰어(documenation viewer)는 이제 설정 가능하고 플러그인 방식으로 교체할 수 있습니다. 기본적으로 django-ninja는 Swagger와 Redoc을 함께 제공합니다:
```Python
from ninja import NinjaAPI, Redoc, Swagger


# use redoc
api = NinjaAPI(docs=Redoc()))

# use swagger:
api = NinjaAPI(docs=Swagger())

# set configuration for swagger:
api = NinjaAPI(docs=Swagger({"persistAuthorization": True}))
```

사용자는 이제 `DocsBase` 클래스를 서브클래싱하여 커스텀 문서 뷰어를 만들 수 있습니다.

## Router

add_router는 문자열 경로를 지원합니다:

```Python
api = NinjaAPI()


api.add_router('/app1', 'myproject.app1.router')
api.add_router('/app2', 'myproject.app2.router')
api.add_router('/app3', 'myproject.app3.router')
api.add_router('/app4', 'myproject.app4.router')
api.add_router('/app5', 'myproject.app5.router')
```


## Decorators

django-ninja가 .get/.post 등으로 view를 장식할 때, 함수의 결과(대부분의 경우 HttpResponse가 아니라 직렬화 가능한 객체)를 래핑하기 때문에, http response를 다루는 일부 내장 또는 서드파티 데코레이터와는 동작하지 않을 가능성이 높습니다. 예를 들어:
```python hl_lines="4"
from django.views.decorators.cache import cache_page

@api.get("/test")
@cache_page(5) # <----- will not work!
def test_view(request):
    return {"some": "Complex data"}
```
이 예제는 동작하지 않습니다.

이제 django-ninja는 http response와 함께 동작하는 데코레이터를 주입할 수 있는 decorate_view 데코레이터를 도입했습니다:
```python hl_lines="1 4"
from ninja.decorators import decorate_view

@api.get("/test")
@decorate_view(cache_page(5))
def test_view(request):
    return str(datetime.now())
```


## Pagination

`paginate_queryset` 메서드는 이제 `request` 객체를 받습니다


#### 하위 호환되지 않는 항목
 - resolve_xxx(self, ...) - (self) 해석 지원은 pydantic의 내장 기능으로 대체되어 deprecated 되었습니다.
 - pydantic v1은 더 이상 지원되지 않습니다
 - python 3.6은 더 이상 지원되지 않습니다

그나저나 — 이 프로젝트가 마음에 드시고 아직 GitHub 별표를 누르지 않으셨다면 — 꼭 눌러 주세요! [github star](img/github-star.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
