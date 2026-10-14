---
comments: true
---
# **Пагинация**

**Django Ninja Extra** предоставляет интуитивную модель пагинации с использованием декоратора `paginate` из модуля пагинации Django-Ninja-Extra. Он ожидает список или queryset в качестве результата функции маршрута.

## **Атрибуты**

`def paginate(func_or_pgn_class: Any = NOT_SET, **paginator_params: Any) -> Callable[..., Any]:`

- func_or_pgn_class: определяет функцию маршрута или класс пагинации. По умолчанию: `ninja_extra.pagination.LimitOffsetPagination`
- paginator_params: дополнительные параметры, используемые для инициализации класса пагинации

### **Использование Ninja LimitOffsetPagination**
При использовании `ninja_extra.pagination.LimitOffsetPagination` в качестве обёртки схемы ответа пагинации следует использовать `NinjaPaginationResponseSchema`.

Например: 
```python
from ninja_extra.schemas import NinjaPaginationResponseSchema

...

@route.get('', response=NinjaPaginationResponseSchema[UserSchema])
@paginate()
def list_items(self):
    return item_model.objects.all()
```
    

### **Изменение класса пагинации по умолчанию**
Чтобы изменить класс пагинации по умолчанию, нужно добавить переменную `NINJA_EXTRA` в `settings.py` с ключом `PAGINATION_CLASS` и значением, определяющим путь к классу пагинации.
```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'PAGINATION_CLASS': 'ninja_extra.pagination.PageNumberPaginationExtra'
}
```

## **Использование**
```python
from typing import List
from ninja_extra.pagination import (
    paginate, PageNumberPaginationExtra, PaginatedResponseSchema
)
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
    @route.get('', response=PaginatedResponseSchema[UserSchema])
    @paginate(PageNumberPaginationExtra, page_size=50)
    def get_users(self):
        return user_model.objects.all()
    
    @route.get('/limit', response=List[UserSchema])
    @paginate
    def get_users_with_limit(self):
        # this will use default paginator class - ninja_extra.pagination.LimitOffsetPagination
        return user_model.objects.all()

    
api = NinjaExtraAPI(title='Pagination Test')
api.register_controllers(UserController)
```

![Preview](../images/pagination_example.gif)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
