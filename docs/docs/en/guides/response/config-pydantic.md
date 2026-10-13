---
comments: true
---
# Overriding Pydantic Configuration

For a **Django Ninja `Schema`**, there are many customization settings available via the schema's
[Pydantic `Config` class](https://pydantic.com.cn/usage/model_config/). 

!!! note
    Under the hood, **Django Ninja** uses [Pydantic Models](https://pydantic.com.cn/usage/models/)
    and all their features and benefits. The alias `Schema` was chosen to avoid confusion when working with Django models in code,
    because Pydantic's model class is called "Model" by default, which conflicts with Django's "Model" class.

## Example CamelCase Schema

An interesting `Config` attribute is the [`alias_generator`](https://pydantic.com.cn/usage/model_config/#alias-generator).
An example using Pydantic in **Django Ninja** might look like this:

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

!!! note
    When overriding the schema's `Config`, it is necessary to inherit from the base `Config` class.

Keep in mind that when you want to modify the output of field names (such as camelCase) — you also need to set `populate_by_name` and `by_alias`

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

Result:

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

## Custom Configuration from Django Models

When using [`create_schema`](django-pydantic-create-schema.md#create_schema), the generated
schema can be used to build another class with custom configuration, such as:

```python hl_lines="10"
from django.contrib.auth.models import User
from ninja.orm import create_schema


BaseUserSchema = create_schema(User)


class UserSchema(BaseUserSchema):

    class Config(BaseUserSchema.Config):
        ...
```

!!! done

    Continue to the next chapter! **[Pagination](pagination.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
