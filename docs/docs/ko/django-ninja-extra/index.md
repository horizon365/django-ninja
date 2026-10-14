![Test](https://github.com/eadwinCode/django-ninja-extra/workflows/Test/badge.svg)
[![PyPI version](https://badge.fury.io/py/django-ninja-extra.svg)](https://badge.fury.io/py/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/v/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/pyversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/djversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![Codecov](https://img.shields.io/codecov/c/gh/eadwinCode/django-ninja-extra)](https://codecov.io/gh/eadwinCode/django-ninja-extra)
[![Downloads](https://pepy.tech/badge/django-ninja-extra)](https://pepy.tech/project/django-ninja-extra)

# Django Ninja Extra 문서

**Django Ninja Extra**는 [**Django Ninja**](https://django-ninja.cn)를 사용한 RESTful API 개발을 가속화할 추가 기능과 함께 **클래스 기반** 접근 방식을 제공합니다.

**주요 기능:**

모든 **Django-Ninja** 기능:

- **간단함**: 사용하기 쉽고 직관적으로 설계되었습니다.
- **빠른 실행**: **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>**과 **<a href="/async-support/">비동기 지원</a> 덕분에 매우 높은 성능을 제공합니다.**
- **빠른 코딩**: 타입 힌트와 자동 문서화를 통해 비즈니스 로직에 집중할 수 있습니다.
- **표준 기반**: 표준에 기반: **OpenAPI**(이전 Swagger) 및 **JSON Schema**.
- **Django 친화적**: (당연하게도) Django 코어 및 ORM과 잘 통합됩니다.

추가로 **Extra**:

- **클래스 기반**: 클래스 기반 방식으로 API를 설계합니다.
- **권한**: 라우트 수준 또는 컨트롤러 수준에서 정의된 권한 및 인증을 통해 액세스 엔드포인트를 쉽게 보호합니다.
- **의존성 주입**: 컨트롤러 클래스는 Python [**Injector** ](https://injector.readthedocs.io/en/latest/) 또는 [**django_injector**](https://github.com/blubber/django_injector) 사용을 지원합니다. 이를 통해 API 의존성 서비스를 APIController 클래스에 주입하고 필요한 곳에서 사용할 수 있습니다.

---

### 버전 요구 사항
- Python >= 3.6
- django >= 2.1 
- pydantic >= 1.6 
- Django-Ninja >= 0.16.1


전체 문서는 [이 링크를 방문하세요](https://django-ninja.cn/django-ninja-extra/).

## 설치

```
pip install django-ninja-extra
```
설치 후 `ninja_extra`를 `INSTALLED_APPS`에 추가하세요

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```

## 사용법

Django 프로젝트에서 `urls.py` 옆에 새 `api.py` 파일을 생성하세요:

```Python
from ninja_extra import NinjaExtraAPI, api_controller, http_get

api = NinjaExtraAPI()

# Function-based definition
@api.get("/add", tags=['Math'])
def add(request, a: int, b: int):
    return {"result": a + b}

# Class-based definition
@api_controller('/', tags=['Math'], permissions=[])
class MathAPI:

    @http_get('/subtract',)
    def subtract(self, a: int, b: int):
        """Subtracts a from b"""
        return {"result": a - b}

    @http_get('/divide',)
    def divide(self, a: int, b: int):
        """Divides a by b"""
        return {"result": a / b}
    
    @http_get('/multiple',)
    def multiple(self, a: int, b: int):
        """Multiples a with b"""
        return {"result": a * b}
    
api.register_controllers(
    MathAPI
)
```

이제 `urls.py`로 이동하여 다음을 추가하세요:

```Python
...
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # <---------- !
]
```

### 대화형 API 문서

이제 <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>로 이동하세요

자동 대화형 API 문서(<a href="https://github.com/swagger-api/swagger-ui" target="_blank">Swagger UI</a> 기반)를 볼 수 있습니다:

![Swagger UI](images/ui_swagger_preview_readme.gif)

## 튜토리얼
- [django-ninja - Using django-ninja-extra permissions, controllers and throttling!](https://www.youtube.com/watch?v=yQqig-c2dd4) - django-ninja-extra 권한, 컨트롤러 및 쓰로틀링 사용 방법 배우기
- [BookStore API](https://github.com/eadwinCode/bookstoreapi) - ninja schema 및 ninja-jwt와 함께 django-ninja-extra를 사용하는 방법을 보여주는 샘플 프로젝트

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
