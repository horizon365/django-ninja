---
comments: true
---
# Tutorial - Responses verarbeiten

## Response-Schemas definieren

**Django Ninja** ermöglicht es Ihnen, Response-Schemas für Validierung und Dokumentation zu definieren.

Wir erstellen eine dritte Operation, die Informationen über den aktuellen Django-Benutzer zurückgibt.

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

Dies konvertiert das `User`-Objekt von Django in ein Dictionary, das nur die definierten Felder enthält.

### Mehrere Response-Typen

Lassen Sie uns eine andere Response zurückgeben, wenn der aktuelle Benutzer nicht authentifiziert ist.

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

Wie Sie sehen, können Sie ein zweiteiliges Tupel zurückgeben, das als HTTP-Response-Code und Daten interpretiert wird.

!!! success

    Dies ist das Ende des Tutorials! Sehen Sie sich die **[weiteren Tutorials](other/crud.md)** oder die **[How-to-Leitfäden](../guides/input/operations.md)** für weitere Informationen an.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
