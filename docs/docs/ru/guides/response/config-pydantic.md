---
comments: true
---
# Переопределение конфигурации Pydantic

Для **`Schema` в Django Ninja** доступно множество настроек кастомизации через
[класс `Config` Pydantic](https://pydantic.com.cn/usage/model_config/). 

!!! note
    «Под капотом» **Django Ninja** использует [модели Pydantic](https://pydantic.com.cn/usage/models/)
    со всеми их возможностями и преимуществами. Псевдоним `Schema` был выбран, чтобы избежать путаницы при работе с моделями Django в коде,
    потому что класс модели Pydantic по умолчанию называется «Model», что конфликтует с классом «Model» в Django.

## Пример схемы CamelCase

Интересным атрибутом `Config` является [`alias_generator`](https://pydantic.com.cn/usage/model_config/#alias-generator).
Пример использования Pydantic в **Django Ninja** может выглядеть так:

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
    При переопределении `Config` схемы необходимо наследоваться от базового класса `Config`.

Имейте в виду, что когда вы хотите изменить вывод имён полей (например, camelCase) — вам также нужно установить `populate_by_name` и `by_alias`

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

Результат:

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

## Пользовательская конфигурация из моделей Django

При использовании [`create_schema`](django-pydantic-create-schema.md#create_schema) сгенерированная
схема может использоваться для построения другого класса с пользовательской конфигурацией, например:

```python hl_lines="10"
from django.contrib.auth.models import User
from ninja.orm import create_schema


BaseUserSchema = create_schema(User)


class UserSchema(BaseUserSchema):

    class Config(BaseUserSchema.Config):
        ...
```

!!! done

    Переходите к следующей главе! **[Пагинация](pagination.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
