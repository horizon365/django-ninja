
Parfois, vous souhaiterez peut-être créer manuellement un token pour un utilisateur. Cela peut être fait comme suit :

```python
from ninja_jwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
```

La fonction `get_tokens_for_user` ci-dessus renverra la représentation sérialisée d'un nouveau refresh token et d'un access token pour l'utilisateur donné.
De manière générale, les tokens de n'importe quelle sous-classe de `ninja_jwt.tokens.Token` peuvent être créés de cette manière.

!!! success

    Poursuivez avec le chapitre suivant **[Types de tokens](token_types.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
