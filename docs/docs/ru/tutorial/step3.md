---
comments: true
---
# Учебник — Обработка ответов

## Определение схем ответов

**Django Ninja** позволяет определять схемы ответов для целей валидации и документирования.

Мы создадим третью операцию, которая возвращает информацию о текущем пользователе Django.

```python
from ninja import Schema

class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # Unauthenticated users do not have the following fields, so provide default values.
    email: str = None
    first_name: str = None
    last_name: str = None

@api.get("/me", response=UserSchema)
def me(request):
    return request.user
```

Это преобразует объект `User` из Django в словарь, содержащий только определённые поля.

### Несколько типов ответов

Давайте вернём другой ответ, если текущий пользователь не аутентифицирован.

```python hl_lines="2-5 7-8 10 12-13"
class UserSchema(Schema):
    username: str
    email: str
    first_name: str
    last_name: str

class Error(Schema):
    message: str

@api.get("/me", response={200: UserSchema, 403: Error})
def me(request):
    if not request.user.is_authenticated:
        return 403, {"message": "Please sign in first"}
    return request.user 
```

Как видите, вы можете вернуть кортеж из двух элементов, который будет интерпретирован как код HTTP-ответа и данные.

!!! success

    Это конец учебника! Ознакомьтесь с **[другими учебниками](other/crud.md)** или **[How-to руководствами](../guides/input/operations.md)** для получения дополнительной информации.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
