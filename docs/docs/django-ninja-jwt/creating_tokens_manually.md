
有时，你可能希望为用户手动创建一个令牌。这可以按如下方式进行：

```python
from ninja_jwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
```

上述函数 `get_tokens_for_user` 将返回给定用户的新刷新令牌和访问令牌的序列化表示。
一般来说，`ninja_jwt.tokens.Token` 的任何子类的令牌都可以通过这种方式创建。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
