---
comments: true
---
# Pydantic-Konfiguration überschreiben

Für ein **Django-Ninja-`Schema`** stehen viele Anpassungsmöglichkeiten über die
[Pydantic-`Config`-Klasse](https://pydantic.com.cn/usage/model_config/) des Schemas zur Verfügung. 

!!! note
    Unter der Haube verwendet **Django Ninja** [Pydantic Models](https://pydantic.com.cn/usage/models/)
    und alle ihre Features und Vorteile. Der Alias `Schema` wurde gewählt, um Verwirrung bei der Arbeit mit Django-Modellen im Code zu vermeiden,
    da die Model-Klasse von Pydantic standardmäßig „Model" heißt, was mit Djangos „Model"-Klasse kollidiert.

## Beispiel: CamelCase-Schema

Ein interessantes `Config`-Attribut ist der [`alias_generator`](https://pydantic.com.cn/usage/model_config/#alias-generator).
Ein Beispiel für die Verwendung von Pydantic in **Django Ninja** könnte so aussehen:

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
    Wenn Sie das `Config` des Schemas überschreiben, müssen Sie von der Basis-`Config`-Klasse erben.

Beachten Sie: Wenn Sie die Ausgabe der Feldnamen ändern möchten (z. B. camelCase), müssen Sie außerdem `populate_by_name` und `by_alias` setzen

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

Ergebnis:

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

## Benutzerdefinierte Konfiguration aus Django-Modellen

Bei der Verwendung von [`create_schema`](django-pydantic-create-schema.md#create_schema) kann das generierte
Schema dazu verwendet werden, eine weitere Klasse mit benutzerdefinierter Konfiguration aufzubauen, zum Beispiel:

```python hl_lines="10"
from django.contrib.auth.models import User
from ninja.orm import create_schema


BaseUserSchema = create_schema(User)


class UserSchema(BaseUserSchema):

    class Config(BaseUserSchema.Config):
        ...
```

!!! done

    Weiter zum nächsten Kapitel! **[Paginierung](pagination.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
