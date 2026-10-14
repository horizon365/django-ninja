---
comments: true
---
# **Paginering**

**Django Ninja Extra** biedt een intuïtief pagineringsmodel met behulp van de decorator `paginate` uit de pagination-module van Django-Ninja-Extra. Deze verwacht een lijst of queryset als resultaat van de routefunctie.

## **Attributen**

`def paginate(func_or_pgn_class: Any = NOT_SET, **paginator_params: Any) -> Callable[..., Any]:`

- func_or_pgn_class: Definieert een routefunctie of een pagination-klasse. Standaard: `ninja_extra.pagination.LimitOffsetPagination`
- paginator_params: Aanvullende parameters die worden gebruikt om de pagination-klasse te initialiseren

### **Gebruik van Ninja LimitOffsetPagination**
Wanneer je `ninja_extra.pagination.LimitOffsetPagination` gebruikt, moet je `NinjaPaginationResponseSchema` gebruiken als wrapper voor het pagination-response-schema.

Bijvoorbeeld: 
```python
from ninja_extra.schemas import NinjaPaginationResponseSchema

...

@route.get('', response=NinjaPaginationResponseSchema[UserSchema])
@paginate()
def list_items(self):
    return item_model.objects.all()
```
    

### **De Standaard Pagination-klasse Wijzigen**
Om de standaard pagination-klasse te wijzigen, moet je een variabele `NINJA_EXTRA` toevoegen in `settings.py` met de sleutel `PAGINATION_CLASS` en een waarde die het pad naar de pagination-klasse definieert.
```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'PAGINATION_CLASS': 'ninja_extra.pagination.PageNumberPaginationExtra'
}
```

## **Gebruik**
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
