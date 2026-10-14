---
comments: true
---
# API 문서

## OpenAPI 문서

Ninja API를 설정하고 runserver를 시작한 후 - <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a> 로 이동하세요.

자동 생성된 인터랙티브 API 문서(<a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a> 기반)가 표시됩니다.


## CDN과 정적 파일

`INSTALLED_APPS`에 django ninja를 추가할 필요는 없습니다. 이 경우 인터랙티브 UI는 CDN을 통해 호스팅됩니다.

문서(Js/css)를 자신의 서버에서 호스팅하려면 - `INSTALLED_APPS`에 `"ninja"`를 넣기만 하면 됩니다. 이 경우 표준 django 정적 파일 호스팅 메커니즘이 이를 호스팅합니다.

## Redoc으로 전환


```python
from ninja import Redoc

api = NinjaAPI(docs=Redoc())

```
그러면 다른 자동 생성 문서(<a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a> 기반)가 표시됩니다.

## 문서 표시 설정 변경

Swagger 또는 Redoc에 커스텀 설정을 지정하려면 docs 클래스의 `settings` 인자를 사용할 수 있습니다.

```python
from ninja import Redoc, Swagger

api = NinjaAPI(docs=Swagger(settings={"persistAuthorization": True}))
...
api = NinjaAPI(docs=Redoc(settings={"disableSearch": True}))

```

그 외 설정에 대해서는 다음 문서를 참조하세요:

 - [Swagger 설정](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)
 - [Redoc 설정](https://redocly.com/docs/api-reference-docs/configuration/functionality/)



## 문서 숨기기

인터랙티브 문서를 표시할 필요가 없다면 - `docs_url` 인자를 `None`으로 설정하세요

```python
api = NinjaAPI(docs_url=None)
```

## 문서 보호

인증(또는 다른 목적의 데코레이터)을 적용하려면 `docs_decorator` 인자를 사용하세요:

```python
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(docs_decorator=staff_member_required)
```

## 커스텀 속성으로 OpenAPI 스키마 확장

커스텀 속성으로 OpenAPI 스키마를 확장할 수 있습니다. 예를 들어 `termsOfService`를 추가하는 경우입니다.

```python
api = NinjaAPI(
   openapi_extra={
       "info": {
           "termsOfService": "https://example.com/terms/",
       }
   },
   title="Demo API",
   description="This is a demo API with dynamic OpenAPI info section"
)
```

## 문서 URL 역방향 조회

뷰 이름 `openapi-view`를 참조하여 API 문서 뷰의 URL을 역방향 조회(reverse)할 수 있습니다.

Python 코드에서는 예를 들어:
```python
from django.urls import reverse

reverse('api-1.0.0:openapi-view')

>>> '/api/docs'
```

Django 템플릿에서는 예를 들어:
```Html
<a href="{% url 'api-1.0.0:openapi-view' %}">API Docs</a>

<a href="/api/docs">API Docs</a>
```

## 커스텀 문서 뷰어 만들기

자신만의 OpenAPI 뷰를 만들려면 - DocsBase를 상속하는 클래스를 만들고 `render_page` 메서드를 오버라이드하세요:



```python
from ninja.openapi.docs import DocsBase

class MyDocsViewer(DocsBase):
    def render_page(self, request, api):
        ... # return http response

...

api = NinjaAPI(docs=MyDocsViewer())

```

!!! success

    다음 섹션 **[에러 처리](errors.md)**로 계속 진행하세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
