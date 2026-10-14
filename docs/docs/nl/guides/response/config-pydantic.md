---
comments: true
---
# Pydantic Configuratie Overriden

Voor een **Django Ninja `Schema`** zijn er veel aanpassingsinstellingen beschikbaar via de
[Pydantic `Config` class](https://pydantic.com.cn/usage/model_config/) van het schema. 

!!! note
    Onder de motorkap gebruikt **Django Ninja** [Pydantic Models](https://pydantic.com.cn/usage/models/)
    met al hun mogelijkheden en voordelen. De alias `Schema` is gekozen om verwarring te voorkomen bij het werken met Django models in code,
    omdat de model class van Pydantic standaard "Model" heet, wat botst met de "Model" class van Django.

## Voorbeeld CamelCase Schema

Een interessant `Config` attribuut is de [`alias_generator`](https://pydantic.com.cn/usage/model_config/#alias-generator).
Een voorbeeld met Pydantic in **Django Ninja** kan er als volgt uitzien:

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
    Wanneer je de `Config` van het schema overridet, is het noodzakelijk om te overerven van de basis `Config` class.

Houd er rekening mee dat wanneer je de uitvoer van veldnamen wilt wijzigen (zoals camelCase) — je ook `populate_by_name` en `by_alias` moet instellen

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

Resultaat:

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

## Aangepaste configuratie vanuit Django Models

Wanneer je [`create_schema`](django-pydantic-create-schema.md#create_schema) gebruikt, kan het gegenereerde
schema worden gebruikt om een andere class met aangepaste configuratie te bouwen, zoals:

```python hl_lines="10"
from django.contrib.auth.models import User
from ninja.orm import create_schema


BaseUserSchema = create_schema(User)


class UserSchema(BaseUserSchema):

    class Config(BaseUserSchema.Config):
        ...
```

!!! done

    Ga verder naar het volgende hoofdstuk! **[Paginering](pagination.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
