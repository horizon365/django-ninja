---
comments: true
---
# Génération dynamique d'un Schema

Sous le capot, [`ModelSchema`](django-pydantic.md#modelschema) utilise la fonction `create_schema`.
Il s'agit d'une approche plus avancée (et moins sûre) — utilisez-la avec prudence.

## `create_schema`

**Django Ninja** est livré avec une fonction utilitaire `create_schema` :

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


Regardez cet exemple :

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
    Par défaut, `create_schema` construit le schéma en utilisant tous les champs du model.
    Cela peut conduire à une exposition accidentelle de données non souhaitées (telles que le mot de passe haché, dans l'exemple ci-dessus).
    <br>
    **Utilisez toujours** l'argument `fields` ou `exclude` pour définir explicitement la liste des attributs.

### Utilisation de `fields`

```python hl_lines="1"
UserSchema = create_schema(User, fields=['id', 'username'])

# Will create schema like this:
#
# class UserSchema(Schema):
#     id: int
#     username: str

```

### Utilisation de `exclude`

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

### Utilisation de `depth`

L'argument `depth` vous permet d'introspecter les champs liés du model Django (clés étrangères, un-à-un, plusieurs-à-plusieurs).

```python hl_lines="1 7"
UserSchema = create_schema(User, depth=1, fields=['username', 'groups'])

# Will create the following schema:
#
# class UserSchema(Schema):
#    username: str
#    groups: List[Group]
```

Notez qu'ici groups devient `List[Group]` — le champ plusieurs-à-plusieurs a été introspecté sur 1 niveau de profondeur et un schéma a également été créé pour les groupes :

```python
class Group(Schema):
    id: int
    name: str
    permissions: List[int]
```

!!! done

    Poursuivez avec le chapitre suivant ! **[Redéfinir la configuration Pydantic](config-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
