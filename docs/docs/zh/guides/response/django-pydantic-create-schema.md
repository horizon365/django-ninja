---
comments: true
---
# 动态生成 Schema

在底层， [`ModelSchema`](django-pydantic.md#modelschema) 使用了 `create_schema` 函数。
这是一种更高级（且不太安全）的方法——请谨慎使用。

## `create_schema`

**Django Ninja** 带有一个辅助函数 `create_schema`:

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


看这个例子:

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

!!! 警告
    默认情况下 `create_schema` 使用所有模型字段构建模式。
    这可能导致意外的不必要数据暴露（如哈希密码，在上述例子中）。
    <br>
    **始终** 使用 `fields` 或 `exclude` 参数来明确定义属性列表。

### 使用 `fields`

```python hl_lines="1"
UserSchema = create_schema(User, fields=['id', 'username'])

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str

```

### 使用 `exclude`

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

### 使用 `depth`

`depth` 参数允许你深入检查 Django 模型到相关字段（外键、一对一、多对多）。

```python hl_lines="1 7"
UserSchema = create_schema(User, depth=1, fields=['username', 'groups'])

# Will create the following schema:
#
# class UserSchema(Schema):
#    username: str
#    groups: List[Group]
```

注意这里的组变成了 `List[Group]` - 多对多字段深入检查了 1 级并也为组创建了模式：

```python
class Group(Schema):
    id: int
    name: str
    permissions: List[int]
```

!!! 大功告成

    继续下一章节！ **[覆盖 Pydantic 配置](config-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
