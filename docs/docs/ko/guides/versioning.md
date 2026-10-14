---
comments: true
---
# 버저닝

## 서로 다른 API 버전

**Django Ninja**를 사용하면 하나의 Django 프로젝트에서 여러 API 버전을 쉽게 운영할 수 있습니다.
해야 할 일은 서로 다른 `version` 인자를 가진 두 개 이상의 NinjaAPI 인스턴스를 생성하는 것뿐입니다:

**api_v1.py**:

```python hl_lines="4"
from ninja import NinjaAPI


api = NinjaAPI(version='1.0.0')

@api.get('/hello')
def hello(request):
    return {'message': 'Hello from V1'}

```


api_**v2**.py:

```python hl_lines="4"
from ninja import NinjaAPI


api = NinjaAPI(version='2.0.0')

@api.get('/hello')
def hello(request):
    return {'message': 'Hello from V2'}
```


그다음 **urls.py**에서:

```python hl_lines="8 9"
...
from api_v1 import api as api_v1
from api_v2 import api as api_v2


urlpatterns = [
    ...
    path('api/v1/', api_v1.urls),
    path('api/v2/', api_v2.urls),
]

```


이제 각 버전마다 서로 다른 OpenAPI 문서 페이지에 접근할 수 있습니다:

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## 서로 다른 비즈니스 로직

같은 방식으로, 서로 다른 컴포넌트나 도메인에 대해 서로 다른 API를 정의할 수 있습니다:
```python hl_lines="4 7"
...


api = NinjaAPI(auth=token_auth, urls_namespace='public_api')
...

api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')
...


urlpatterns = [
    ...
    path('api/', api.urls),
    path('internal-api/', api_private.urls),
]

```
!!! note
    서로 다른 **NinjaAPI** 인스턴스를 사용하는 경우, 서로 다른 `version` 또는 서로 다른 `urls_namespace`를 정의해야 합니다.

!!! success

    How-to 시리즈가 완료되었습니다!

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
