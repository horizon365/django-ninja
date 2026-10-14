
Manchmal möchten Sie möglicherweise manuell ein Token für einen Benutzer erstellen. Dies kann wie folgt geschehen:

```python
from ninja_jwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
```

Die obige Funktion `get_tokens_for_user` gibt die serialisierte Repräsentation eines neuen Refresh-Tokens und Access-Tokens für den angegebenen Benutzer zurück.
Im Allgemeinen können Token jeder Unterklasse von `ninja_jwt.tokens.Token` auf diese Weise erstellt werden.

!!! success

    Fahren Sie mit dem nächsten Kapitel fort: **[Token-Typen](token_types.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
