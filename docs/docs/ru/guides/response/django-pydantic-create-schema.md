---
comments: true
---
# Динамическая генерация схемы

«Под капотом» [`ModelSchema`](django-pydantic.md#modelschema) использует функцию `create_schema`.
Это более продвинутый (и менее безопасный) подход — используйте его с осторожностью.

## `create_schema`

**Django Ninja** поставляется со вспомогательной функцией `create_schema`:

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


Взгляните на этот пример:

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
    По умолчанию `create_schema` строит схему, используя все поля модели.
    Это может привести к случайному раскрытию нежелательных данных (например, хэшированного пароля, как в примере выше).
    <br>
    **Всегда** используйте аргумент `fields` или `exclude`, чтобы явно определить список атрибутов.

### Использование `fields`

```python hl_lines="1"
UserSchema = create_schema(User, fields=['id', 'username'])

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str

```

### Использование `exclude`

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

### Использование `depth`

Аргумент `depth` позволяет интроспектировать связанные поля модели Django (внешние ключи, один-к-одному, многие-ко-многим).

```python hl_lines="1 7"
UserSchema = create_schema(User, depth=1, fields=['username', 'groups'])

# Will create the following schema:
#
# class UserSchema(Schema):
#    username: str
#    groups: List[Group]
```

Обратите внимание, что здесь groups становится `List[Group]` — поле многие-ко-многим было интроспектировано на 1 уровень вглубь, и для groups также была создана схема:

```python
class Group(Schema):
    id: int
    name: str
    permissions: List[int]
```

!!! done

    Переходите к следующей главе! **[Переопределение конфигурации Pydantic](config-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
