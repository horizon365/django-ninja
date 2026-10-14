---
comments: true
---
# Redéfinir la configuration Pydantic

Pour un **`Schema` Django Ninja**, de nombreux paramètres de personnalisation sont disponibles via la
[classe `Config` Pydantic](https://pydantic.com.cn/usage/model_config/) du schéma.

!!! note
    Sous le capot, **Django Ninja** utilise les [Models Pydantic](https://pydantic.com.cn/usage/models/)
    avec toutes leurs fonctionnalités et avantages. L'alias `Schema` a été choisi pour éviter toute confusion lors de la manipulation des models Django dans le code,
    parce que la classe de model de Pydantic s'appelle « Model » par défaut, ce qui entre en conflit avec la classe « Model » de Django.

## Exemple de Schema CamelCase

Un attribut `Config` intéressant est [`alias_generator`](https://pydantic.com.cn/usage/model_config/#alias-generator).
Un exemple d'utilisation de Pydantic dans **Django Ninja** pourrait ressembler à ceci :

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
    Lorsque vous redéfinissez le `Config` du schéma, il est nécessaire d'hériter de la classe `Config` de base.

Gardez à l'esprit que lorsque vous souhaitez modifier la sortie des noms de champs (par exemple en camelCase) — vous devez également définir `populate_by_name` et `by_alias`

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

Résultat :

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

## Configuration personnalisée à partir des models Django

Lorsque vous utilisez [`create_schema`](django-pydantic-create-schema.md#create_schema), le schéma
généré peut servir à construire une autre classe avec une configuration personnalisée, comme par exemple :

```python hl_lines="10"
from django.contrib.auth.models import User
from ninja.orm import create_schema


BaseUserSchema = create_schema(User)


class UserSchema(BaseUserSchema):

    class Config(BaseUserSchema.Config):
        ...
```

!!! done

    Poursuivez avec le chapitre suivant ! **[Pagination](pagination.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
