---
comments: true
---
# Generating Schemas from Django Models


Schemas are very useful for defining validation rules and responses, but sometimes you need to reflect your database models into schemas and keep changes in sync.
## ModelSchema

`ModelSchema` is a special base class that can automatically generate a schema from your model.

All you need to do is set `model` and `fields` on your schema's `Meta`:


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

### Using All Model Fields

To use all fields of a model — you can pass `__all__` to `fields`:

```python hl_lines="4"
class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = "__all__"
```
!!! warning
    Using __all__ is not recommended.
    <br>
    This may lead to accidental exposure of unwanted data (such as the hashed password in the example above).
    <br>
    General recommendation - use `fields` to explicitly define the list of fields you want to be visible in your API.

### Excluding Model Fields

To use all fields **except** a select few, you can use the `exclude` configuration:

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

### Overriding Fields

To change the default annotations for some fields, or to add new fields, simply use annotated properties as usual.
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


### Making Fields Optional

For PATCH API operations, you typically need to make all fields of a schema optional. To do this, you can use the fields_optional configuration

```python hl_lines="5"
class PatchGroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description'] # Note: all these fields are required on model level
        fields_optional = '__all__'
```

You can also define only a few optional fields instead of all:
```python
     fields_optional = ['description']
```

!!! done

    Continue to the next chapter! **[Dynamically Generating a Schema](django-pydantic-create-schema.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
