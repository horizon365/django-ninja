---
comments: true
---
# 인증

## 소개

**Django Ninja**는 <a href="https://swagger.io/docs/specification/authentication/" target="_blank">모든 보안 스펙</a>을 공부하고 익히지 않고도 표준적인 방식으로 인증과 권한 부여를 쉽고 빠르게 처리할 수 있게 도와주는 여러 도구를 제공합니다.

핵심 아이디어는 API operation을 기술할 때 authentication 객체를 정의할 수 있다는 것입니다.
```python hl_lines="2 7"
{!./src/tutorial/authentication/code001.py!}
```

이 예제에서 클라이언트는 Django 세션 인증(기본적으로 쿠키 기반)을 사용할 때만 `pets` 메서드를 호출할 수 있으며, 그렇지 않으면 HTTP-401 에러가 반환됩니다.
슈퍼유저만 권한을 부여하고 싶다면 대신 `from ninja.security import django_auth_superuser`를 사용할 수 있습니다.
## 자동 OpenAPI 스키마

다음은 클라이언트가 인증을 위해 헤더를 전달해야 하는 예제입니다:

`Authorization: Bearer supersecret`

```python hl_lines="4 5 6 7 10"
{!./src/tutorial/authentication/bearer01.py!}
```

이제 <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a> 문서로 이동하세요.


![Swagger UI Auth](../img/auth-swagger-ui.png)

이제 **Authorize** 버튼을 클릭하면 인증 토큰을 입력하라는 프롬프트가 표시됩니다.

![Swagger UI Auth](../img/auth-swagger-ui-prompt.png)

테스트 호출을 하면 모든 요청에 권한 부여 헤더가 전달됩니다.

## 전역 인증

API의 **모든** 메서드를 보호해야 한다면 `NinjaAPI` 생성자에 `auth` 인자를 전달할 수 있습니다:


```python hl_lines="11 19"
from ninja import NinjaAPI, Form
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaAPI(auth=GlobalAuth())

# @api.get(...)
# def ...

# @api.post(...)
# def ...
```

그리고 일부 메서드를 오버라이드해야 하는 경우, `auth` 인자를 전달하여 operation 레벨에서 다시 지정할 수 있습니다. 이 예제에서는 `/token` operation에 대해 인증이 비활성화됩니다:
```python hl_lines="19"
{!./src/tutorial/authentication/global01.py!}
```

## 사용 가능한 인증 옵션

### 커스텀 함수


"`auth=`" 인자는 모든 callable을 받습니다. **NinjaAPI**는 callable이 **참(truthy)**으로 평가되는 값(불리언 `True`로 변환되는 값)을 반환할 때만 인증을 통과시킵니다. 이 반환 값은 `request.auth` 속성에 할당됩니다.

```python hl_lines="1 2 3 6"
{!./src/tutorial/authentication/code002.py!}
```


### API 키

일부 API는 권한 부여를 위해 API 키를 사용합니다. API 키는 클라이언트가 API 호출 시 자신을 식별하기 위해 제공하는 토큰입니다. 키는 쿼리 문자열로 보낼 수 있습니다:
```
GET /something?api_key=abcdef12345
```

또는 요청 헤더로:

```
GET /something HTTP/1.1
X-API-Key: abcdef12345
```

또는 쿠키로:

```
GET /something HTTP/1.1
Cookie: X-API-KEY=abcdef12345
```

**Django Ninja**는 이러한 상황을 처리할 수 있도록 내장 클래스를 제공합니다.


#### Query에서

```python hl_lines="1 2 5 6 7 8 9 10 11 12"
{!./src/tutorial/authentication/apikey01.py!}
```

이 예제에서는 `GET['api_key']`에서 토큰을 가져와 데이터베이스에서 해당 `Client`를 찾습니다. Client 인스턴스는 `request.auth` 속성으로 설정됩니다.

참고: **`param_name`**은 검사할 GET 파라미터의 이름입니다. 설정하지 않으면 기본값 `"key"`가 사용됩니다.


#### Header에서

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey02.py!}
```

#### Cookie에서

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey03.py!}
```



### HTTP Bearer

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/bearer01.py!}
```

### HTTP Basic 인증

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/basic01.py!}
```


## 다중 인증기

**`auth`** 인자는 여러 개의 인증기를 전달하는 것도 허용합니다:

```python hl_lines="18"
{!./src/tutorial/authentication/multiple01.py!}
```

이 경우 **Django Ninja**는 먼저 `GET`에서 API 키를 확인하고, 설정되어 있지 않거나 유효하지 않으면 `header` 키를 확인합니다.
둘 다 유효하지 않으면 응답에 인증 에러가 발생(raise)됩니다.


## 라우터 인증

라우터에 `auth` 인자를 사용하면 해당 라우터 내에 선언된 모든 operation에 인증기를 적용할 수 있습니다:

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

또는 라우터 생성자 사용
```python
router = Router(auth=BasicAuth())
```


## 커스텀 예외

예외 핸들러를 가진 예외를 발생시키면 operation과 동일한 방식으로 해당 핸들러의 응답이 반환됩니다:

```python hl_lines="1 4"
{!./src/tutorial/authentication/bearer02.py!}
```


## 비동기 인증

**Django Ninja**는 비동기 인증을 기본적으로 지원합니다. 기본 인증 클래스는 async 호환이 아니지만, 커스텀 비동기 인증 callable을 정의하고 `auth`로 전달할 수 있습니다.

```python
async def async_auth(request):
    ...


@api.get("/pets", auth=async_auth)
def pets(request):
    ...
```


자세한 내용은 [에러 처리](errors.md)를 참조하세요.

!!! success

    다음 섹션 **[테스트](testing.md)**로 계속 진행하세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
