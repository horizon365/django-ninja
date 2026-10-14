---
comments: true
---
# **Сортировка (Ordering)**

**Django Ninja Extra** предоставляет интуитивную модель сортировки с использованием декоратора `ordering` из модуля сортировки Django-Ninja-Extra. Он ожидает queryset или список в качестве результата функции маршрута.

> Эта возможность была вдохновлена [DRF OrderingFilter](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter)

## **Атрибуты**

`def ordering(func_or_ordering_class: Any = NOT_SET, **ordering_params: Any) -> Callable[..., Any]:`

- func_or_ordering_class: определяет функцию маршрута или класс сортировки. По умолчанию: `ninja_extra.ordering.Ordering`
- ordering_params: дополнительные параметры, используемые для инициализации класса сортировки

### Изменение класса сортировки по умолчанию

Чтобы изменить класс сортировки по умолчанию, нужно добавить переменную `NINJA_EXTRA` в `settings.py` с ключом `ORDERING_CLASS` и значением, определяющим путь к классу сортировки.

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'ORDERING_CLASS': 'someapp.somemodule.CustomOrdering'
}
```

## **Использование**

- Если вы не укажете параметр `ordering_fields`, для сортировки будут использоваться все поля queryset.
- Например, чтобы отсортировать пользователей по имени пользователя (username)
  > http://example.com/api/users?ordering=username
- Клиент также может указать обратную сортировку, добавив префикс `-` к имени поля, например:
  > http://example.com/api/users?ordering=-username
- Можно также указать несколько критериев сортировки:
  > http://example.com/api/users?ordering=username,email

```python
from typing import List
from ninja_extra.ordering import ordering, Ordering
from ninja_extra import api_controller, route, NinjaExtraAPI
from ninja import ModelSchema
from django.contrib.auth import get_user_model

user_model = get_user_model()


class UserSchema(ModelSchema):
    class Config:
        model = user_model
        model_fields = ['username', 'email']


@api_controller('/users')
class UserController:
    @route.get('', response=List[UserSchema])
    @ordering(Ordering, ordering_fields=['username', 'email'])
    def get_users(self):
        return user_model.objects.all()

    @route.get('/all-sort', response=List[UserSchema])
    @ordering
    def get_users_with_all_field_ordering(self):
        return [u for u in user_model.objects.all()]


api = NinjaExtraAPI(title='Ordering Test')
api.register_controllers(UserController)
```

## Примечание

> Если вы используете и декоратор `paginate`, и декоратор `ordering`, декоратор `paginate` должен располагаться выше декоратора `ordering`, потому что данные сначала сортируются, а затем разбиваются на страницы, например:
>
> ```python
>    @route.get('', response=List[UserSchema])
>    @paginate
>    @ordering(Ordering, ordering_fields=['username', 'email'])
>    def get_users(self):
>        return user_model.objects.all()
> ```

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
