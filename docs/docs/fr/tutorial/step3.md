---
comments: true
---
# Tutoriel - Gérer les réponses

## Définir des schémas de réponse

**Django Ninja** vous permet de définir des schémas de réponse à des fins de validation et de documentation.

Nous allons créer une troisième opération qui renvoie des informations sur l'utilisateur Django courant.

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

Cela convertira l'objet `User` de Django en un dictionnaire ne contenant que les champs définis.

### Plusieurs types de réponse

Renvoyons une réponse différente si l'utilisateur courant n'est pas authentifié.

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

Comme vous pouvez le voir, vous pouvez renvoyer un tuple à deux éléments qui sera interprété comme le code de réponse HTTP et les données.

!!! success

    C'est la fin du tutoriel ! Consultez les **[autres tutoriels](other/crud.md)** ou les **[Guides how-to](../guides/input/operations.md)** pour plus d'informations.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
