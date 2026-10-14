---
comments: true
---
# **Поиск (Searching)**

**Django Ninja Extra** предоставляет интуитивную модель поиска с использованием декоратора `searching` из модуля поиска Django-Ninja-Extra. Он ожидает queryset или список в качестве результата функции маршрута.

> Эта возможность была вдохновлена [DRF SearchFilter](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)

## **Атрибуты**

`def searching(func_or_searching_class: Any = NOT_SET, **searching_params: Any) -> Callable[..., Any]:`

- func_or_searching_class: определяет функцию маршрута или класс поиска. По умолчанию: `ninja_extra.searching.Searching`
- searching_params: дополнительные параметры, используемые для инициализации класса поиска

### Изменение класса поиска по умолчанию

Чтобы изменить класс поиска по умолчанию, нужно добавить переменную `NINJA_EXTRA` в `settings.py` с ключом `SEARCHING_CLASS` и значением, определяющим путь к классу поиска

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'SEARCHING_CLASS': 'someapp.somemodule.CustomSearching'
}
```

## **Использование**

- Если вы не укажете параметр `search_fields`, результаты будут возвращены без изменений.
- Например, чтобы искать пользователей по имени пользователя (username) или email:
  > http://example.com/api/users?search=someuser
- Вы также можете использовать нотацию двойного подчёркивания lookup API для выполнения поиска по связанным полям внешних ключей или полей «многие-ко-многим»:
  > search_fields = ['username', 'email', 'profile__profession']
- По умолчанию поиск использует частичное совпадение без учёта регистра. Параметр поиска может содержать несколько поисковых терминов, которые должны быть разделены пробелами и/или запятыми. При использовании нескольких поисковых терминов в списке будут возвращены только объекты, соответствующие всем указанным терминам. Поведение поиска можно ограничить, добавив различные символы перед `search_fields`.

  * '^' Поиск по началу строки (starts-with).
  * '=' Точное совпадение.
  * '@' Полнотекстовый поиск. (В настоящее время поддерживается только [PostgreSQL-бэкендом Django](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/).)
  * '$' Поиск по регулярному выражению.

  Например:

    > search_fields = ['=username', '=email']

```python
from typing import List
from ninja_extra.searching import searching, Searching
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
    @searching(Searching, search_fields=['username', 'email'])
    def get_users(self):
        return user_model.objects.all()

    @route.get('/iexact-email', response=List[UserSchema])
    @searching(search_fields=['=email'])
    def get_users_with_search_iexact_email(self):
        return [u for u in user_model.objects.all()]


api = NinjaExtraAPI(title='Searching Test')
api.register_controllers(UserController)
```

## Примечание

> Если вы одновременно используете декоратор `paginate`, декоратор `ordering` и декоратор `searching`, то `paginate` должен располагаться выше декоратора `ordering`, а декоратор `ordering` — выше декоратора `searching`. Потому что данные сначала фильтруются, затем сортируются и в конце разбиваются на страницы, например:
>
> ```python
>    @route.get('', response=List[UserSchema])
>    @paginate
>    @ordering(Ordering, ordering_fields=['username', 'email'])
>    @searching(Searching, search_fields=['username', 'email'])
>    def get_users(self):
>        return user_model.objects.all()
> ```

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
