
Sometimes you may wish to manually create a token for a user. This can be done as follows:

```python
from ninja_jwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
```

The above function `get_tokens_for_user` will return the serialized representation of a new refresh token and access token for the given user.
In general, tokens of any subclass of `ninja_jwt.tokens.Token` can be created this way.

!!! success

    Continue to the next chapter **[Token Types](token_types.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
