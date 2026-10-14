
Soms wil je handmatig een token voor een gebruiker aanmaken. Dit kan als volgt:

```python
from ninja_jwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
```

De bovenstaande functie `get_tokens_for_user` geeft de geserialiseerde representatie van een nieuw refresh token en access token voor de opgegeven gebruiker terug.
In het algemeen kunnen tokens van elke subklasse van `ninja_jwt.tokens.Token` op deze manier worden aangemaakt.

!!! success

    Ga verder naar het volgende hoofdstuk **[Tokentypes](token_types.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
