---
comments: true
---
# Tutorial - Omgaan met responses

## Response-schema's definiëren

**Django Ninja** laat je response-schema's definiëren ten behoeve van validatie en documentatie.

We maken een derde operatie die informatie over de huidige Django-gebruiker teruggeeft.

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

Dit zet het `User`-object van Django om naar een dictionary die alleen de gedefinieerde velden bevat.

### Meerdere response-types

Laten we een andere response teruggeven als de huidige gebruiker niet is ingelogd.

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

Zoals je ziet kun je een tuple van twee elementen teruggeven, die wordt geïnterpreteerd als de HTTP-responsecode en de gegevens.

!!! success

    Dit is het einde van de tutorial! Bekijk de **[andere tutorials](other/crud.md)** of de **[How-to guides](../guides/input/operations.md)** voor meer informatie.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
