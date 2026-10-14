---
comments: true
---
# Schema को गतिशील रूप से बनाना

भीतर की परत में (under the hood), [`ModelSchema`](django-pydantic.md#modelschema) `create_schema` function का उपयोग करता है।
यह एक अधिक उन्नत (और कम सुरक्षित) तरीका है — इसका उपयोग सावधानी से करें।

## `create_schema`

**Django Ninja** एक helper function `create_schema` के साथ आता है:

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


इस उदाहरण को देखें:

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
    डिफ़ॉल्ट रूप से, `create_schema` सभी model fields का उपयोग करके schema बनाता है।
    इससे अनचाहे data के आकस्मिक exposure का जोखिम हो सकता है (जैसे ऊपर दिए गए उदाहरण में hashed password)।
    <br>
    Attributes की सूची को स्पष्ट रूप से परिभाषित करने के लिए **हमेशा** `fields` या `exclude` argument का उपयोग करें।

### `fields` का उपयोग करना

```python hl_lines="1"
UserSchema = create_schema(User, fields=['id', 'username'])

# Will create schema like this:
#
# class UserSchema(Schema):
#     id: int
#     username: str

```

### `exclude` का उपयोग करना

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

### `depth` का उपयोग करना

`depth` argument आपको Django model के related fields (foreign keys, one-to-one, many-to-many) को introspect करने की अनुमति देता है।

```python hl_lines="1 7"
UserSchema = create_schema(User, depth=1, fields=['username', 'groups'])

# Will create the following schema:
#
# class UserSchema(Schema):
#    username: str
#    groups: List[Group]
```

ध्यान दें कि यहाँ groups `List[Group]` बन जाता है — many-to-many field को 1 स्तर गहरा introspect किया गया और groups के लिए भी एक schema बनाया गया:

```python
class Group(Schema):
    id: int
    name: str
    permissions: List[int]
```

!!! done

    अगले अध्याय पर जाएँ! **[Overriding Pydantic Configuration](config-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
