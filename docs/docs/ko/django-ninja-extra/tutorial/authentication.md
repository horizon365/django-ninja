---
comments: true
---
# **인증**

**Django Ninja Extra**는 인가(authorization)와 인증(authentication) 측면에서 **Django Ninja**와 동일한 API를 제공하여, 두 패키지 간의 일관성과 사용 편의성을 보장합니다.

## **자동 OpenAPI 스키마**

다음은 클라이언트가 인증을 위해 헤더를 전달해야 하는 예제입니다:

`Authorization: Bearer supersecret`

```Python
from ninja.security import HttpBearer
from ninja_extra import api_controller, route
from ninja.constants import NOT_SET


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token

@api_controller(tags=['My Operations'], auth=NOT_SET, permissions=[])
class MyController:
    @route.get("/bearer", auth=AuthBearer())
    def bearer(self):
        return {"token": self.context.request.auth}

```

## **전역 인증** 
`api`와 APIController에 정의된 **모든** 라우트 메서드를 보호해야 한다면, `NinjaExtraAPI` 생성자에 `auth` 매개변수를 전달할 수 있습니다:


```Python
from ninja_extra import NinjaExtraAPI
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaExtraAPI(auth=GlobalAuth())

```
django-ninja의 [인증](https://django-ninja.cn/guides/authentication/)에 대해 더 알아보세요.

## 비동기 인증 클래스

Ninja Extra는 `ninja_extra.security` 패키지에서 Django Ninja가 제공하는 모든 `Auth` 베이스 클래스에 대한 비동기 지원을 추가하며, 유사한 인터페이스를 유지합니다. 이 비동기 인증 클래스를 사용할 때는 엔드포인트 핸들러가 **반드시** 비동기(async) 함수여야 한다는 점에 유의해야 합니다.

예를 들어, 첫 번째 인증 예제를 `AsyncHttpBearer` 클래스로 다시 작성해 보겠습니다.

```Python
from ninja_extra import api_controller, route
from ninja_extra.security import AsyncHttpBearer
from ninja.constants import NOT_SET


class AuthBearer(AsyncHttpBearer):
    async def authenticate(self, request, token):
        # await some actions
        if token == "supersecret":
            return token


@api_controller(tags=['My Operations'], auth=NOT_SET, permissions=[])
class MyController:
    @route.get("/bearer", auth=AuthBearer())
    async def bearer(self):
        return {"token": self.context.request.auth}

```
위 예제에서 `HttpBearer`를 `AsyncHttpBearer`로 변경하고 bearer를 `async` 엔드포인트로 변경했습니다. 
`AuthBearer`를 `MyController`의 **인증**에 적용하려면, `MyController` 아래의 모든 라우트 핸들러가 비동기 라우트 핸들러여야 합니다.


## **JWT 인증**
JWT 인증을 사용하려면 [ninja-jwt](https://pypi.org/project/django-ninja-jwt/)를 참고하세요

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
