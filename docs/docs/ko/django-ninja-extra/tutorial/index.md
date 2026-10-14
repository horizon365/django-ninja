---
comments: true
---
# **튜토리얼 / 레퍼런스**

이 튜토리얼은 **Django Ninja Extra**와 그 기능 대부분을 사용하는 방법을 보여줍니다.
특히 **Django Ninja**를 사용할 줄 안다고 가정합니다.


!!! info
    여기 내용의 상당 부분은 Django-Ninja에서 가져온 것입니다. 따라서 먼저 Django-Ninja 프레임워크를 학습하면 대부분의 내용이 쉽게 이해될 것입니다.

## **설치**

```
pip install django-ninja-extra
```

설치 후 `INSTALLED_APPS`에 `ninja_extra`를 추가합니다

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```


## **Django 프로젝트 만들기**

(이미 기존 Django 프로젝트가 있다면 다음 단계로 건너뛰세요).

새 Django 프로젝트를 시작합니다(또는 기존 프로젝트를 사용합니다).

```
django-admin startproject myproject
```


## **첫 번째 단계**

API를 위한 모듈을 만들어 보겠습니다. **urls.py**와 같은 디렉터리 위치에 **api.py** 파일을 생성합니다:


`api.py`


```Python
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()

# function definition using Django-Ninja default router
@api.get("/hello")
def hello(request):
    return "Hello world"

```

이제 **urls.py**로 가서 다음을 추가합니다:


```Python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## **오퍼레이션 메서드 정의하기**
"오퍼레이션(operation)"은 HTTP "메서드" 중 하나입니다:

 - GET
 - POST
 - PUT
 - DELETE
 - PATCH
 - ... 등등

이것들은 Django-Ninja가 API 또는 Django-Ninja 라우터에 정의한 오퍼레이션들입니다.

동일한 오퍼레이션들이 `route` 클래스를 통해 APIController에 노출됩니다.

`route` 클래스는 APIController 인스턴스 메서드를 라우트 함수 또는 엔드포인트로 변환하는 추가 데코레이터입니다.

한편, 여기서의 `route`는 `ControllerRouter` 클래스의 줄임말로, APIController를 Django-Ninja 라우터에 단순히 적응(adapt)시키는 어댑터 클래스입니다. 또한 모든 APIController 클래스에 정의된 라우트에 대한 전역적인 제어도 제공합니다.

```Python
from ninja_extra import (
    api_controller, 
    http_get, http_post, http_put, http_delete, http_patch, http_generic
)
from ninja.constants import NOT_SET

@api_controller('', tags=['My Operations'], auth=NOT_SET, permissions=[])
class MyAPIController:
    @http_get("/path")
    def get_operation(self):
        ...
    
    @http_post("/path")
    def post_operation(self):
        ...
    
    @http_put("/path")
    def put_operation(self):
        ...
    
    @http_delete("/path")
    def delete_operation(self):
        ...
    
    @http_patch("/path")
    def patch_operation(self):
        ...
    
    # If you need to handle multiple methods with a single function, you can use the `generic` method as shown above
    @http_generic(["POST", "PATCH"]) 
    def mixed(request):
        ...

api.register_controllers(MyAPIController)
```
컨트롤러 설정을 완료하려면, 등록하기 전에 APIController를 `ControllerRouter`로 데코레이트해야 합니다.


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
