---
comments: true
---
# Dynamisch een Schema Genereren

Onder de motorkap gebruikt [`ModelSchema`](django-pydantic.md#modelschema) de functie `create_schema`.
Dit is een meer geavanceerde (en minder veilige) aanpak — gebruik het met de nodige voorzichtigheid.

## `create_schema`

**Django Ninja** wordt geleverd met een hulpfunctie `create_schema`:

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


Bekijk dit voorbeeld:

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
    Standaard bouwt `create_schema` het schema met alle modelvelden.
    Dit kan leiden tot onbedoelde blootstelling van ongewenste data (zoals het gehashte wachtwoord in het voorbeeld hierboven).
    <br>
    Gebruik **altijd** het argument `fields` of `exclude` om de lijst met attributen expliciet te definiëren.

### `fields` gebruiken

```python hl_lines="1"
UserSchema = create_schema(User, fields=['id', 'username'])

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str

```

### `exclude` gebruiken

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

### `depth` gebruiken

Met het argument `depth` kun je gerelateerde velden van het Django model introspecteren (foreign keys, one-to-one, many-to-many).

```python hl_lines="1 7"
UserSchema = create_schema(User, depth=1, fields=['username', 'groups'])

# Will create the following schema:
#
# class UserSchema(Schema):
#    username: str
#    groups: List[Group]
```

Let op: hier wordt groups `List[Group]` — het many-to-many veld is 1 niveau diep geïntrospecteerd en er is ook een schema gemaakt voor groups:

```python
class Group(Schema):
    id: int
    name: str
    permissions: List[int]
```

!!! done

    Ga verder naar het volgende hoofdstuk! **[Pydantic Configuratie Overriden](config-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
