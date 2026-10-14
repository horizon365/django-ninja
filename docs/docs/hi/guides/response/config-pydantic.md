---
comments: true
---
# Pydantic Configuration को override करना

एक **Django Ninja `Schema`** के लिए, schema की
[Pydantic `Config` class](https://pydantic.com.cn/usage/model_config/) के माध्यम से कई customization settings उपलब्ध हैं।

!!! note
    भीतर की परत में (under the hood), **Django Ninja** [Pydantic Models](https://pydantic.com.cn/usage/models/)
    और उनकी सभी सुविधाओं व लाभों का उपयोग करता है। Code में Django models के साथ काम करते समय confusion से बचने के लिए `Schema` alias चुना गया था,
    क्योंकि Pydantic की model class डिफ़ॉल्ट रूप से "Model" कहलाती है, जो Django की "Model" class से टकराव करती है।

## CamelCase Schema उदाहरण

एक दिलचस्प `Config` attribute [`alias_generator`](https://pydantic.com.cn/usage/model_config/#alias-generator) है।
**Django Ninja** में Pydantic का उपयोग करने वाला एक उदाहरण इस तरह दिख सकता है:

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
    Schema की `Config` को override करते समय, base `Config` class से inherit करना आवश्यक है।

ध्यान रखें कि जब आप field नामों के आउटपुट को बदलना चाहते हैं (जैसे camelCase) — तो आपको `populate_by_name` और `by_alias` भी सेट करने की आवश्यकता है

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

परिणाम:

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

## Django Models से Custom Configuration

[`create_schema`](django-pydantic-create-schema.md#create_schema) का उपयोग करते समय, बनाए गए
schema का उपयोग custom configuration वाली एक और class बनाने के लिए किया जा सकता है, जैसे:

```python hl_lines="10"
from django.contrib.auth.models import User
from ninja.orm import create_schema


BaseUserSchema = create_schema(User)


class UserSchema(BaseUserSchema):

    class Config(BaseUserSchema.Config):
        ...
```

!!! done

    अगले अध्याय पर जाएँ! **[Pagination](pagination.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
