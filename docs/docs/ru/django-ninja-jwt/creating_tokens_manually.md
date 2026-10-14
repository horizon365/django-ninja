
Иногда вам может понадобиться вручную создать токен для пользователя. Это можно сделать следующим образом:

```python
from ninja_jwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
```

Приведённая выше функция `get_tokens_for_user` вернёт сериализованное представление нового refresh-токена и access-токена для заданного пользователя.
В целом, токены любого подкласса `ninja_jwt.tokens.Token` могут быть созданы таким образом.

!!! success

    Перейдите к следующей главе **[Типы токенов](token_types.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
