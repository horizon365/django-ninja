---
comments: true
---
# 응답 조정하기

때로는 응답이 제공되기 직전에 이를 변경하고 싶을 수 있습니다. 예를 들어 헤더를 추가하거나 쿠키를 수정하는 경우입니다.

이를 위해 `HttpResponse` 타입의 함수 인자를 선언하기만 하면 됩니다:

```python
from django.http import HttpRequest, HttpResponse

@api.get("/cookie/")
def feed_cookiemonster(request: HttpRequest, response: HttpResponse):
    # Set a cookie.
    response.set_cookie("cookie", "delicious")
    # Set a header.
    response["X-Cookiemonster"] = "blue"
    return {"cookiemonster_happy": True}
```


## 임시(Temporal) Response 객체

이 response 객체는 에러 응답을 포함해 Django Ninja가 만드는 모든 응답의 기반으로 사용됩니다.
Django `HttpResponse` 객체가 operation에 의해 직접 반환되는 경우에는 이 객체가 사용되지 *않습니다*.

당연히 이 response 객체에는 아직 content가 담겨 있지 않지만, `content_type`은 설정되어 있습니다(다만 변경하고 싶지는 않을 것입니다).

`status_code`는 반환 값에 따라 오버라이드됩니다(기본값은 200이며, 두 요소 튜플이 반환되면 그 상태 코드가 사용됩니다).


## 기본 Response 객체 변경

이 임시 response 객체는 `NinjaAPI.create_temporal_response` 메서드를 오버라이드하여 변경할 수 있습니다.

```python
    def create_temporal_response(self, request: HttpRequest) -> HttpResponse:
        response = super().create_temporal_response(request)
        # Do your magic here...
        return response
```

!!! done

    다음 챕터로 계속 진행하세요! **[Django Models로부터 Schema 생성하기](django-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
