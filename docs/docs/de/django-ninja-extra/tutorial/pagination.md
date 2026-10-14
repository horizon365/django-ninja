---
comments: true
---
# **Pagination**

**Django Ninja Extra** bietet ein intuitives Paginierungsmodell unter Verwendung des Decorators `paginate` aus dem Pagination-Modul von Django-Ninja-Extra. Er erwartet eine Liste oder ein Queryset aus dem Ergebnis der Routenfunktion.

## **Attribute**

`def paginate(func_or_pgn_class: Any = NOT_SET, **paginator_params: Any) -> Callable[..., Any]:`

- func_or_pgn_class: Definiert eine Routenfunktion oder eine Pagination-Klasse. Standard: `ninja_extra.pagination.LimitOffsetPagination`
- paginator_params: Zusätzliche Parameter, die zur Initialisierung der Pagination-Klasse verwendet werden

### **Verwendung von Ninja LimitOffsetPagination**
Bei Verwendung von `ninja_extra.pagination.LimitOffsetPagination` sollten Sie `NinjaPaginationResponseSchema` als Wrapper für das Pagination-Response-Schema verwenden.

Zum Beispiel: 
```python
from ninja_extra.schemas import NinjaPaginationResponseSchema

...

@route.get('', response=NinjaPaginationResponseSchema[UserSchema])
@paginate()
def list_items(self):
    return item_model.objects.all()
```
    

### **Die Standard-Pagination-Klasse ändern**
Um die Standard-Pagination-Klasse zu ändern, müssen Sie eine Variable `NINJA_EXTRA` in der `settings.py` mit dem Schlüssel `PAGINATION_CLASS` und einem Wert hinzufügen, der den Pfad zur Pagination-Klasse definiert.
```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'PAGINATION_CLASS': 'ninja_extra.pagination.PageNumberPaginationExtra'
}
```

## **Verwendung**
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
