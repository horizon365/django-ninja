---
comments: true
---
# **버저닝(Versioning)**

## **서로 다른 API 버전 번호**

**Django Ninja Extra**를 사용하면 단일 Django 프로젝트에서 여러 API 버전을 매우 쉽게 운영할 수 있습니다.

서로 다른 `version` 매개변수를 가진 두 개 이상의 NinjaAPI 인스턴스를 만들기만 하면 됩니다:


**`api_v1.py`**:

```Python
from ninja_extra import NinjaExtraAPI, route, api_controller

@api_controller
class MyV1Controller:
    @route.get('/hello')
    def hello(self):
        return {'message': 'Hello from V1'}
    
    @route.get('/example')
    def example(self):
        return {'message': 'Hello from V1 Example'}

    
api = NinjaExtraAPI(version='1.0.0')
api.register_controllers(MyV1Controller)
```


api_**v2**.py:
API 컨트롤러를 재사용하고 특정 라우트를 변경할 수 있습니다.

```Python
from ninja_extra import NinjaExtraAPI, route, api_controller
from .api_v1 import MyV1Controller

@api_controller
class MyV2Controller(MyV1Controller):
    @route.get('/example')
    def example(self):
        return {'message': 'Hello from V2 Example'}

    
api = NinjaExtraAPI(version='2.0.0')
api.register_controllers(MyV2Controller)
```


그다음 **urls.py**에서:

```Python hl_lines="8 9"
...
from api_v1 import api as api_v1
from api_v2 import api as api_v2


urlpatterns = [
    ...
    path('api/v1/', api_v1.urls),
    path('api/v2/', api_v2.urls),
]

```


이제 각 버전에 대해 서로 다른 OpenAPI 문서 페이지에 접근할 수 있습니다:

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## **서로 다른 비즈니스 로직**

같은 방식으로, 컴포넌트나 도메인별로 서로 다른 API를 정의할 수 있습니다:

```Python
...


api = NinjaExtraAPI(auth=token_auth, urls_namespace='public_api')
...

api_private = NinjaExtraAPI(auth=session_auth, urls_namespace='private_api')
...


urlpatterns = [
    ...
    path('api/', api.urls),
    path('internal-api/', api_private.urls),
]

```
!!! note
    서로 다른 **NinjaExtraAPI** 인스턴스를 사용하는 경우, 서로 다른 `version` 또는 서로 다른 `urls_namespace`를 정의해야 합니다.
    **NinjaAPI** 인스턴스도 마찬가지입니다.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
