---
comments: true
---
# CSRF (Cross-Site Request Forgery)

## 사이트 간 요청 위조란 무엇인가?
> [사이트 간 요청 위조(Cross-site request forgery)](https://en.wikipedia.org/wiki/Cross-site_request_forgery)는 악성 웹사이트가 로그인한 사용자(브라우저에서 악성 웹사이트를 방문한 사용자)의 자격 증명을 사용하여 여러분의 웹사이트(또는 이 문서에서 다루지 않는 다른 위치)에서 어떤 동작을 수행하도록 의도된 링크, form 버튼 또는 일부 JavaScript를 포함할 때 발생합니다.


## Django Ninja로 사이트 간 요청 위조를 방어하는 방법
### 요청에 자동으로 포함되지 않는 인증 방식 사용하기
사이트 간 요청 위조 공격은 [cookies](https://en.wikipedia.org/wiki/HTTP_cookie)나 [Basic access authentication](https://en.wikipedia.org/wiki/Basic_access_authentication)처럼 다른 웹사이트에서 시작된 요청에 자동으로 포함되는 인증 방식에 의존합니다.
`Authorization: Bearer`처럼 자동으로 포함되지 않는 인증 방식을 사용하면 이 공격을 완화할 수 있습니다.


### Django의 내장 사이트 간 요청 위조 방지 기능 사용하기
cookie를 사용하는 기본 Django 인증을 사용하고 있다면, 기본 [Django 사이트 간 요청 위조 방지 기능](https://docs.djangoproject.com/en/4.2/ref/csrf/)도 함께 사용해야 합니다.


기본적으로 **Django Ninja**는 모든 operation에 대해 사이트 간 요청 위조 방지 기능이 **꺼져(OFF)** 있습니다.
이를 켜려면 NinjaAPI 클래스의 `csrf` 인자를 사용해야 합니다:

```python hl_lines="3"
from ninja import NinjaAPI

api = NinjaAPI(csrf=True)
```

<span style="color: red;">경고</span>: 사이트 간 요청 위조 방지를 끈 상태에서 cookie 기반 인증을 사용하는 것은 안전하지 않습니다! (예: `CookieKey` 또는 `django_auth`).


**Django Ninja**는 cookie 기반 인증의 경우 사이트 간 요청 위조 방지를 자동으로 활성화합니다.


```python hl_lines="8"
from ninja import NinjaAPI
from ninja.security import APIKeyCookie

class CookieAuth(APIKeyCookie):
    def authenticate(self, request, key):
        return key == "test"

api = NinjaAPI(auth=CookieAuth())

```


또는 django-auth 기반인 경우입니다 (cookie 기반 인증을 상속함):

```python hl_lines="4"
from ninja import NinjaAPI
from ninja.security import django_auth

api = NinjaAPI(auth=django_auth)
```


#### Django `ensure_csrf_cookie` 데코레이터
보호되지 않은 route에 Django [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie) 데코레이터를 사용하여 사이트 간 요청 위조 토큰을 위한 `Set-Cookie` 헤더가 포함되도록 할 수 있습니다. 다음에 유의하세요:
- route 데코레이터는 [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie) 데코레이터보다 먼저(즉, 위에서) 실행되어야 합니다.
- 해당 route에 `csrf_exempt`를 적용해야 합니다.
- `ensure_csrf_cookie` 데코레이터는 Django `HttpResponse`에만 동작하며, 대부분의 Django Ninja 데코레이터처럼 dictionary에는 동작하지 않습니다.
```python hl_lines="4"
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

@api.post("/csrf")
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request):
    return HttpResponse()
```
이 route에 대한 요청은 Django가 적절한 `Set-Cookie` 헤더와 함께 응답하도록 트리거합니다.


#### 프론트엔드 코드
[How to use Django's CSRF protection](https://docs.djangoproject.com/en/4.2/howto/csrf/) 문서의 [Using CSRF protection with AJAX](https://docs.djangoproject.com/en/4.2/howto/csrf/#using-csrf-protection-with-ajax)와 [Setting the token on the AJAX request](https://docs.djangoproject.com/en/4.2/howto/csrf/#setting-the-token-on-the-ajax-request) 섹션을 참조하여 프론트엔드 코드에서 사이트 간 요청 위조 방지 토큰을 처리하는 방법을 알아볼 수 있습니다.


## CORS에 대하여
프론트엔드와 API를 서로 다른 사이트에 구성하고 싶을 수 있습니다 (그런 경우 [django-cors-headers](https://github.com/adamchainz/django-cors-headers)를 확인해 보세요).
사이트 간 요청 위조와 직접적인 관련은 없지만, 프론트엔드가 사용하는 사이트와 다른 사이트에 사이트 간 요청 위조 cookie를 정의할 때는 [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy)가 기본적으로 이를 허용하지 않으므로 CORS(Cross-Origin Resource Sharing)가 도움이 될 수 있습니다.
그런 경우 [django-cors-headers README](https://github.com/adamchainz/django-cors-headers#readme)를 확인해 보세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
