---
comments: true
---
# スキーマの動的生成

内部的には、[`ModelSchema`](django-pydantic.md#modelschema) は `create_schema` 関数を使用しています。
これはより高度な（そして安全性の低い）アプローチです — 注意して使用してください。

## `create_schema`

**Django Ninja** にはヘルパー関数 `create_schema` が付属しています:

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


次の例を見てください:

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
    デフォルトでは、`create_schema` はすべてのモデルフィールドを使ってスキーマを構築します。
    これにより、望まないデータ（上記の例ではハッシュ化されたパスワードなど）が誤って露出する可能性があります。
    <br>
    属性のリストは **必ず** `fields` または `exclude` 引数を使って明示的に定義してください。

### `fields` の使用

```python hl_lines="1"
UserSchema = create_schema(User, fields=['id', 'username'])

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str

```

### `exclude` の使用

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

### `depth` の使用

`depth` 引数を使用すると、Django モデルのリレーションフィールド（外部キー、一対一、多対多）をインスペクトできます。

```python hl_lines="1 7"
UserSchema = create_schema(User, depth=1, fields=['username', 'groups'])

# Will create the following schema:
#
# class UserSchema(Schema):
#    username: str
#    groups: List[Group]
```

ここで groups は `List[Group]` になります — 多対多フィールドが 1 レベルの深さでインスペクトされ、groups のスキーマも作成されます:

```python
class Group(Schema):
    id: int
    name: str
    permissions: List[int]
```

!!! done

    次の章に進みましょう！ **[Pydantic 設定のオーバーライド](config-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
