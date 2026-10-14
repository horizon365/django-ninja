
때로는 사용자를 위해 토큰을 수동으로 생성하고 싶을 수 있습니다. 다음과 같이 수행할 수 있습니다:

```python
from ninja_jwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
```

위의 `get_tokens_for_user` 함수는 주어진 사용자에 대한 새 refresh 토큰과 access 토큰의 직렬화된 표현을 반환합니다.
일반적으로 `ninja_jwt.tokens.Token`의 모든 서브클래스의 토큰은 이런 방식으로 생성할 수 있습니다.

!!! success

    다음 장 **[토큰 타입](token_types.md)**으로 계속 진행하세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
