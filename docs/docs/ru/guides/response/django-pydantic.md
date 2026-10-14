---
comments: true
---
# Генерация схем из моделей Django


Схемы очень полезны для определения правил валидации и ответов, но иногда нужно отразить модели базы данных в схемы и поддерживать изменения в синхронизации.
## ModelSchema

`ModelSchema` — это специальный базовый класс, который может автоматически генерировать схему из вашей модели.

Всё, что нужно сделать, — задать `model` и `fields` в `Meta` вашей схемы:


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

### Использование всех полей модели

Чтобы использовать все поля модели — передайте `__all__` в `fields`:

```python hl_lines="4"
class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = "__all__"
```
!!! warning
    Использование __all__ не рекомендуется.
    <br>
    Это может привести к случайному раскрытию нежелательных данных (например, хэшированного пароля в примере выше).
    <br>
    Общая рекомендация — используйте `fields`, чтобы явно определить список полей, которые должны быть видимы в вашем API.

### Исключение полей модели

Чтобы использовать все поля, **кроме** некоторых, вы можете использовать конфигурацию `exclude`:

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

### Переопределение полей

Чтобы изменить аннотации по умолчанию для некоторых полей или добавить новые поля, просто используйте аннотированные свойства, как обычно.
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


### Сделать поля необязательными

Для операций PATCH API обычно нужно сделать все поля схемы необязательными. Для этого можно использовать конфигурацию fields_optional

```python hl_lines="5"
class PatchGroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description'] # Note: all these fields are required on model level
        fields_optional = '__all__'
```

Вы также можете определить лишь несколько необязательных полей вместо всех:
```python
     fields_optional = ['description']
```

!!! done

    Переходите к следующей главе! **[Динамическая генерация схемы](django-pydantic-create-schema.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
