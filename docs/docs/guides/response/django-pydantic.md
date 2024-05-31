---
comments: true
---
# 来自 Django 模型的 Schemas 模式


Schemas 模式对于定义验证规则和响应非常有用，但有时您需要将数据库模型反映到模式中并保持更改同步。
## ModelSchema 模型模式

`ModelSchema` 是一个特殊的基类，可以自动从您的模型生成模式。

您所需要做的就是在您的模式 `Meta` 上设置 `model` 和 `fields`:


```python hl_lines="2 5 6 7"
from django.contrib.auth.models import User
from ninja import ModelSchema

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str
#     first_name: str
#     last_name: str
```

### 使用所有模型字段

要使用模型的所有字段 - 您可以将 `__all__` 传递给 `fields`:

```python hl_lines="4"
class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = "__all__"
```
!!! 警告
    不建议使用 __all__ 。
    <br>
    这可能导致意外的不必要数据暴露（例如上述示例中的哈希密码）。
    <br>
    一般建议 - 使用 `fields` 明确定义您希望在 API 中可见的字段列表。

### 排除模型字段

要使用 **除** 少数几个之外的所有字段，您可以使用 `exclude` 配置:

```python hl_lines="4"
class UserSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ['password', 'last_login', 'user_permissions']

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str
#     first_name: str
#     last_name: str
#     email: str
#     is_superuser: bool
#     ... and the rest

```

### 覆盖字段

要更改某些字段的默认注释，或添加新字段，只需像往常一样使用带注释的属性。
```python hl_lines="1 2 3 4 8"
class GroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSchema(ModelSchema):
    groups: List[GroupSchema] = []

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

```


### 使字段可选

对于 PATCH API 操作，通常您需要使模式的所有字段可选。为此，您可以使用配置 fields_optional

```python hl_lines="5"
class PatchGroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description'] # Note: all these fields are required on model level
        fields_optional = '__all__'
```

您也可以只定义几个可选字段而不是所有：
```python
     fields_optional = ['description']
```
