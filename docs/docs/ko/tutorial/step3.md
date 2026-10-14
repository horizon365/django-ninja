---
comments: true
---
# 튜토리얼 - 응답 처리하기

## Response schema 정의하기

**Django Ninja**는 검증과 문서화를 위해 response schema를 정의할 수 있게 해줍니다.

현재 Django 사용자에 대한 정보를 반환하는 세 번째 operation을 만들어 보겠습니다.

```python
from ninja import Schema

class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # Unauthenticated users do not have the following fields, so provide default values.
    email: str = None
    first_name: str = None
    last_name: str = None

@api.get("/me", response=UserSchema)
def me(request):
    return request.user
```

이렇게 하면 Django의 `User` 객체가 정의된 필드만 포함하는 dictionary로 변환됩니다.

### 여러 response 타입

현재 사용자가 인증되어 있지 않을 때 다른 응답을 반환하도록 해 보겠습니다.

```python hl_lines="2-5 7-8 10 12-13"
class UserSchema(Schema):
    username: str
    email: str
    first_name: str
    last_name: str

class Error(Schema):
    message: str

@api.get("/me", response={200: UserSchema, 403: Error})
def me(request):
    if not request.user.is_authenticated:
        return 403, {"message": "Please sign in first"}
    return request.user 
```

보시다시피, HTTP 응답 코드와 데이터로 해석되는 두 부분으로 이루어진 튜플을 반환할 수 있습니다.

!!! success

    튜토리얼이 여기서 끝입니다! 더 많은 정보는 **[다른 튜토리얼](other/crud.md)** 또는 **[How-to 가이드](../guides/input/operations.md)**를 확인하세요.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
