
Ninja JWT는 Django Ninja의 `HttpBearer`를 사용하여 API 엔드포인트에 도달한 사용자를 인증합니다.
인증된 사용자는 `request.user` 또는 `request.auth`에서 찾을 수 있습니다.

### 라우트 인증 - 클래스 기반

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=JWTAuth())
    def some_endpoint(self):
        ...
```

### 라우트 인증 - 함수 기반

```python
from ninja import router
from ninja_jwt.authentication import JWTAuth

router = router('')

@router.get('/some-endpoint', auth=JWTAuth())
def some_endpoint(request):
    ...
```

커스텀 인증 구현
-------
`JWTAuth`의 다른 구현을 사용하고 싶다면 `JWTBaseAuthentication`을 서브클래싱해야 합니다.
`bearer`가 아닌 다른 방식을 사용하려면 [Django Ninja - 인증](https://django-ninja.rest-framework.com/tutorial/authentication/) 문서를 더 읽어보세요.

예제:
```python
from ninja.security import APIKeyHeader
from ninja_jwt.authentication import JWTBaseAuthentication
from ninja import router

class ApiKey(APIKeyHeader, JWTBaseAuthentication):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        return self.jwt_authenticate(request, token=key)


header_key = ApiKey()
router = router('')

@router.get("/headerkey", auth=header_key)
def apikey(request):
    return f"Token = {request.auth}"

```

### 비동기 라우트 인증
비동기 라우트 인증에 관심이 있다면 `AsyncJWTAuth` 클래스를 사용할 수 있습니다

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import AsyncJWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=AsyncJWTAuth())
    async def some_endpoint(self):
        ...
```
참고: `some_endpoint`는 비동기여야 합니다. `AsyncJWTAuth`로 표시된 모든 엔드포인트 함수는 비동기여야 합니다.

!!! warning
    비동기 기능은 Django 3.0보다 높은 버전에서만 사용할 수 있습니다.

!!! success

    다음 장 **[설정](settings.md)**으로 계속 진행하세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
