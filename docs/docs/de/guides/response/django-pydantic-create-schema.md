---
comments: true
---
# Ein Schema dynamisch generieren

Unter der Haube verwendet [`ModelSchema`](django-pydantic.md#modelschema) die Funktion `create_schema`.
Dies ist ein fortgeschrittenerer (und weniger sicherer) Ansatz – verwenden Sie ihn mit Vorsicht.

## `create_schema`

**Django Ninja** wird mit einer Hilfsfunktion `create_schema` ausgeliefert:

```python
def create_schema(
    model, # django model
    name = "", # name for the generated class, if empty model names is used
    depth = 0, # if > 0 schema will also be created for the nested ForeignKeys and Many2Many (with the provided depth of lookup)
    fields: list[str] = None, # if passed - ONLY these fields will added to schema
    exclude: list[str] = None, # if passed - these fields will be excluded from schema
    optional_fields: list[str] | str = None, # if passed - these fields will not be required on schema (use '__all__' to mark ALL fields required)
    custom_fields: list[tuple(str, Any, Any)] = None, # if passed - this will override default field types (or add new fields)
)
```


Sehen Sie sich dieses Beispiel an:

```python hl_lines="2 4"
from django.contrib.auth.models import User
from ninja.orm import create_schema

UserSchema = create_schema(User)

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str
#     first_name: str
#     last_name: str
#     password: str
#     last_login: datetime
#     is_superuser: bool
#     email: str
#     ... and the rest

```

!!! warning
    Standardmäßig baut `create_schema` das Schema mit allen Modellfeldern auf.
    Das kann dazu führen, dass versehentlich unerwünschte Daten offengelegt werden (wie etwa das gehashte Passwort im obigen Beispiel).
    <br>
    **Verwenden Sie immer** das Argument `fields` oder `exclude`, um die Liste der Attribute explizit zu definieren.

### Verwendung von `fields`

```python hl_lines="1"
UserSchema = create_schema(User, fields=['id', 'username'])

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str

```

### Verwendung von `exclude`

```python hl_lines="1 2"
UserSchema = create_schema(User, exclude=[
    'password', 'last_login', 'is_superuser', 'is_staff', 'groups', 'user_permissions']
)

# Will create schema without excluded fields:
# 
# class UserSchema(Schema):
#    id: int
#    username: str
#    first_name: str
#    last_name: str
#    email: str
#    is_active: bool
#    date_joined: datetime
```

### Verwendung von `depth`

Das Argument `depth` erlaubt es Ihnen, verbundene Felder des Django-Modells zu introspektieren (Foreign Keys, One-to-One, Many-to-Many).

```python hl_lines="1 7"
UserSchema = create_schema(User, depth=1, fields=['username', 'groups'])

# Will create the following schema:
#
# class UserSchema(Schema):
#    username: str
#    groups: List[Group]
```

Beachten Sie, dass `groups` hier zu `List[Group]` wird – das Many-to-Many-Feld wurde 1 Ebene tief introspektiert, und es wurde ebenfalls ein Schema für die Gruppen erstellt:

```python
class Group(Schema):
    id: int
    name: str
    permissions: List[int]
```

!!! done

    Weiter zum nächsten Kapitel! **[Pydantic-Konfiguration überschreiben](config-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
