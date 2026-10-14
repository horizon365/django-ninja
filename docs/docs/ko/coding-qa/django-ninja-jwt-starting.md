---
comments: true
---
## 소개
JWT는 오래전부터 알고 있었지만 실제로 사용해 본 적은 없었습니다. 최근 tus 재개 가능 업로드 프로토콜을 조사하면서 hooks-http 수준까지 들어가게 되었는데, 목표는 파일 업로드 중 인증을 하는 것이었습니다. 자연스럽게 `django-ninja-jwt` 패키지가 떠올랐습니다. 간단할 것이라고 생각했지만, [중국어 문서](https://django-ninja.cn/django-ninja-jwt/)를 읽고 나서야 이것이 단순히 간단한 정도가 아니라 놀라울 정도로 간결하다는 것을 알게 되었습니다.

## 시작하기

가이드에 따르면 `dango-ninja-jwt`와 `django-ninja-extra`만 설치한 후 `NinjaAPI`를 `njaExtraAPI`로 교체하면 되며, 한 줄이면 충분합니다.

```python
api.register_controllers(NinjaJWTDefaultController)
```

솔직히 어리둥절할 정도입니다.

잠깐 — 먼저 문서를 살펴봅시다. 새로운 엔드포인트 세 개가 나타납니다: `pair`, `refresh`, `verify`.
![JWT swagger UI token](../img/jwt-token.png)
오른쪽 상단의 자물쇠 아이콘에 주목하세요 — 나중에 유용하게 쓰일 것입니다. 이 아이콘은 `JWTAuth` 함수를 사용할 때만 나타납니다.

### pair
첫 번째는 `pair` 엔드포인트입니다. 사용자 이름과 비밀번호를 제공하면 인증 토큰과 리프레시 토큰을 반환한다는 의미입니다.
요청 본문 형식은 다음과 같습니다:
```json
{
  "password": "string",
  "username": "string"
}
```
참고: 여기서 `username`이 아래에 나타나는데, 일반적으로 예상하는 것과는 조금 다릅니다.
Execute를 클릭하면 다음과 같은 결과를 얻게 됩니다:
```json
{
  "data": {
    "username": "lyq",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzE0NzU2NCwiaWF0IjoxNzQyNTQyNzY0LCJqdGkiOiI4MTZmMzg2YWYwNmY0NmVhOWY1YzlkMDJjYzQxZjFkOCIsInVzZXJfaWQiOjF9.G-mTefGtP-cTXWVrxAsqXGGKnZ1442jw67ilvTY5gcQ",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNjI5MTY0LCJpYXQiOjE3NDI1NDI3NjQsImp0aSI6IjdiMGY1Y2Y5NTVlZDRiMzQ5M2M3MmY4NzJmNDdkMzUxIiwidXNlcl9pZCI6MX0.JO9PxVA-rX6TPo9Db00eOuOorThjgX3nTjBT-CuOh90"
  }
}
```
### refresh
위의 `access` 토큰은 인증에 사용할 수 있지만, 기본적으로 유효 기간이 제한되어 있습니다. `refresh` 토큰은 `access`보다 유효 기간이 길며, 이전 토큰이 만료된 후 새로운 `access` 토큰을 얻는 데 사용됩니다.
리프레시되면 이전 `access` 토큰은 무효화됩니다.

이 시점에서 `access`를 오른쪽 상단의 자물쇠 아이콘에 복사해 넣을 수 있습니다. 이렇게 하면 현재 페이지의 모든 엔드포인트에서 이를 사용할 수 있어 디버깅에 편리합니다.
### verify
세 번째 엔드포인트인 `verify`로 이동하여 `access` 토큰이 유효한지 확인할 수 있습니다.

전반적으로 `django-ninja-jwt`는 단순히 세 개의 엔드포인트를 만들어 주어 토큰을 획득하고, 리프레시하고, 테스트하기 편리하게 해 줍니다.

## 커스터마이징
이 세 개의 엔드포인트만으로는 부족합니다 — 최소한 우리 자신의 특정 엔드포인트에 인증을 추가해야 합니다.
여기서 필요한 것이 `JWTAuth`입니다. 이것을 사용한 후에야 자물쇠 아이콘이 나타납니다.
```python
from ninja_jwt.authentication import JWTAuth
@route.get('/some', auth=JWTAuth())
def some_endpoint(request):
    """Convenient for showing the auth button on the docs page"""
    return request.auth.username
```
그리고 `some` 엔드포인트에도 별도의 자물쇠 아이콘이 있습니다.
![JWT swagger UI token custom](../img/jwt-token-custom.png)
위의 `some` 엔드포인트에서 인증이 성공하면 현재 로그인한 사용자의 사용자 이름으로 응답합니다. 실패하면 401 응답을 반환합니다.
백엔드 개발자는 프론트엔드 팀에 이 값을 함께 보내라고 알려야 합니다 — [pair](#pair) 섹션으로 이동해 토큰을 획득하고, 주기적으로 [refresh](#refresh)로 이동해 리프레시하도록 해야 합니다.

### 토큰 유효 기간 설정

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Access token lifetime
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh token lifetime
    'AUTH_HEADER_TYPES': ('Bearer',),
}

```
### 추가 커스터마이징
ninja 라우트에서 `@route.get('/some', auth=JWTAuth())`를 사용하는 것이 요구 사항을 충족하지 못한다면, 함수 내부에서 `authenticate`를 호출할 수 있습니다.

```python
@route.get('/some')
def some_endpoint(request):
    auth = JWTAuth()
    # If it fails, a 401 is raised internally
    if auth.authenticate(request, token):
        return request.auth.username

```
위의 `token`은 `request` 객체에서 직접 추출해야 합니다.
