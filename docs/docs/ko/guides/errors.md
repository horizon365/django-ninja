---
comments: true
---
# 에러 처리

**Django Ninja**는 커스텀 예외 핸들러를 설치하여 에러나 처리된 예외 발생 시 응답이 반환되는 방식을 제어할 수 있게 해줍니다.

## 커스텀 예외 핸들러

특정 시점에 의도적으로 사용 불가 상태가 되도록 설계된 외부 서비스에 의존하는 API를 만들고 있다고 가정해 보겠습니다. 예외가 발생할 때 기본 500 에러를 던지는 대신, 그 에러를 처리하여 클라이언트에게 친절한 응답(나중에 다시 시도하라고 안내)을 반환할 수 있습니다.
이를 위해 다음을 수행해야 합니다:

 - 1) 예외를 생성하거나(또는 기존 예외를 사용)
 - 2) api.exception_handler 데코레이터 사용


예제:


```python hl_lines="9 10"
api = NinjaAPI()

class ServiceUnavailableError(Exception):
    pass


# initializing handler

@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=503,
    )


# some logic that throws exception

@api.get("/service")
def some_operation(request):
    if random.choice([True, False]):
        raise ServiceUnavailableError()
    return {"message": "Hello"}

```

예외 핸들러 함수는 2개의 인자를 받습니다:

 - **request** - Django의 HTTP 요청
 - **exc** - 실제 예외

이 함수는 HTTP 응답을 반환해야 합니다

## 기본 예외 핸들러 오버라이드

기본적으로 **Django Ninja**는 다음 예외 핸들러들을 초기화합니다:


#### `ninja.errors.AuthenticationError`

인증 데이터가 유효하지 않을 때 발생합니다

#### `ninja.errors.ValidationError`

요청 데이터가 검증에 실패할 때 발생합니다

#### `ninja.errors.HttpError`

코드 어디에서나 상태 코드와 함께 HTTP 에러를 던지는 데 사용됩니다
#### `django.http.Http404`
 
Django의 기본 404 예외입니다 (예를 들어 get_object_or_404를 사용하여 반환할 수 있습니다)
#### `Exception`
 
애플리케이션에서 처리되지 않은 그 외 모든 예외입니다.
기본 동작
 
  - **`settings.DEBUG`가 `True`인 경우** - 일반 텍스트로 트레이스백을 반환합니다 (콘솔이나 Swagger UI에서 디버깅할 때 유용)
  - **그 외의 경우** - Django의 기본 예외 처리 메커니즘을 사용합니다 (에러 로깅, ADMINS에게 이메일 전송)


### 기본 핸들러 오버라이드

검증 에러의 기본 출력을 변경해야 하는 경우 - ValidationError 예외 핸들러를 오버라이드하세요:

```python hl_lines="1 4"
from ninja.errors import ValidationError
...

@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return HttpResponse("Invalid input", status=422)
```


## 예외를 통한 HTTP 응답 던지기

커스텀 예외를 만들고 그에 대한 핸들러를 작성하는 대안으로 - HTTP 예외를 던질 수도 있으며, 이렇게 하면 원하는 코드를 담은 HTTP 응답이 반환됩니다

```python
from ninja.errors import HttpError

@api.get("/some/resource")
def some_operation(request):
    if True:
        raise HttpError(503, "Service Unavailable. Please retry later.")

```
!!! success

    다음 섹션 **[URL 역방향 조회](urls.md)**로 계속 진행하세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
