---
comments: true
---
# 覆盖 Pydantic 配置

对于一个 **Django Ninja `Schema` 模式**, 有许多可用的自定义设置，通过模式的
[Pydantic `Config` 类](https://pydantic-docs.helpmanual.io/usage/model_config/). 

!!! 注意
    在底层 **Django Ninja** 使用 [Pydantic Models 模型](https://pydantic-docs.helpmanual.io/usage/models/)
    及其所有的特性和优点。 选择别名 `Schema` 是为了在代码中使用 Django 模型时避免混淆，
    因为 Pydantic 的模型类默认被称为“模型”，与 Django 的“模型”类冲突。

## 示例驼峰命名模式

一个有趣的 `Config` 属性是 [`alias_generator 别名生成器`](https://pydantic-docs.helpmanual.io/usage/model_config/#alias-generator).
在 **Django Ninja** 中使用 Pydantic 的示例可能看起来像这样:

```python hl_lines="12 13"
from ninja import Schema


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))


class CamelModelSchema(Schema):
    str_field_name: str
    float_field_name: float

    class Config(Schema.Config):
        alias_generator = to_camel
```

!!! 注意
    当覆盖 schema 模式的 `Config`时，有必要从基础 `Config` 类继承。

请记住，当你想要修改字段名称的输出（如驼峰命名）时 - 你还需要设置 `populate_by_name` 和 `by_alias`

```python hl_lines="6 9"
class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ["id", "email"]
        alias_generator = to_camel
        populate_by_name = True  # !!!!!! <--------


@api.get("/users", response=list[UserSchema], by_alias=True) # !!!!!! <-------- by_alias
def get_users(request):
    return User.objects.all()

```

结果:

```JSON
[
  {
    "Id": 1,
    "Email": "tim@apple.com"
  },
  {
    "Id": 2,
    "Email": "sarah@smith.com"
  }
  ...
]

```

## 来自 Django 模型的自定义配置

当使用 [`create_schema`](django-pydantic-create-schema.md#create_schema)时，生成的
模式可以用于构建另一个具有自定义配置的类，如：

```python hl_lines="10"
from django.contrib.auth.models import User
from ninja.orm import create_schema


BaseUserSchema = create_schema(User)


class UserSchema(BaseUserSchema):

    class Config(BaseUserSchema.Config):
        ...
```

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
