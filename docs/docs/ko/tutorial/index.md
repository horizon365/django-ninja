---
comments: true
---
# 튜토리얼 - 첫걸음

이 튜토리얼은 **Django Ninja**의 대부분의 기능을 사용하는 방법을 보여줍니다.

이 튜토리얼은 <a href="https://www.djangoproject.com/" target="_blank">Django 프레임워크</a>의 기본 사항, 즉 프로젝트를 생성하고 실행하는 방법 등은 최소한 알고 있다고 가정합니다.

## 설치

```console
pip install django-ninja
```

!!! note

    필수는 아니지만, `ninja`를 `INSTALLED_APPS`에 추가할 수도 있습니다.
    그 경우 OpenAPI/Swagger UI(또는 Redoc)가 번들된 JavaScript 패키지에서 로드됩니다 (이쪽이 더 빠릅니다) (그렇지 않으면 JavaScript 번들이 CDN에서 제공됩니다)

## Django 프로젝트 생성하기

새 Django 프로젝트를 시작합니다 (또는 이미 Django 프로젝트가 있다면 다음 단계로 넘어가세요).

```
django-admin startproject myproject
```

## API 생성하기

API를 위한 모듈을 만들어 보겠습니다. Django 프로젝트의 루트 `urls.py`와 같은 위치에 `api.py` 파일을 생성합니다:

```python
from ninja import NinjaAPI

api = NinjaAPI()
```

이제 `urls.py`로 가서 다음을 추가합니다:

```python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## 우리의 첫 operation

**Django Ninja**는 각 HTTP 메서드(`GET`, `POST`,
`PUT` 등)에 대한 데코레이터를 함께 제공합니다. `api.py` 파일에 간단한 "hello world" operation을 추가해 보겠습니다.

```python hl_lines="5-7"
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"
```

이제 브라우저로 가서 <a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a>를 열면 간단한 JSON 응답이 반환됩니다:
```json
"Hello world"
```

!!! success

    다음 장 **[입력 파라미터 처리하기](step2.md)**로 계속 진행하세요.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
