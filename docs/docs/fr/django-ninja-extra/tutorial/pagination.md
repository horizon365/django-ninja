---
comments: true
---
# **Pagination**

**Django Ninja Extra** fournit un modèle de pagination intuitif à l'aide du décorateur `paginate` du module pagination de Django-Ninja-Extra. Il attend une liste ou un queryset provenant du résultat de la fonction de route.

## **Attributs**

`def paginate(func_or_pgn_class: Any = NOT_SET, **paginator_params: Any) -> Callable[..., Any]:`

- func_or_pgn_class : Définit une fonction de route ou une classe de pagination. Par défaut : `ninja_extra.pagination.LimitOffsetPagination`
- paginator_params : Paramètres supplémentaires utilisés pour initialiser la classe de pagination

### **Utilisation de Ninja LimitOffsetPagination**
Lors de l'utilisation de `ninja_extra.pagination.LimitOffsetPagination`, vous devez utiliser `NinjaPaginationResponseSchema` comme enveloppe de schéma de réponse de pagination.

Par exemple : 
```python
from ninja_extra.schemas import NinjaPaginationResponseSchema

...

@route.get('', response=NinjaPaginationResponseSchema[UserSchema])
@paginate()
def list_items(self):
    return item_model.objects.all()
```
    

### **Changer la classe de pagination par défaut**
Pour changer la classe de pagination par défaut, vous devez ajouter une variable `NINJA_EXTRA` dans `settings.py` avec la clé `PAGINATION_CLASS` et une valeur définissant le chemin vers la classe de pagination.
```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'PAGINATION_CLASS': 'ninja_extra.pagination.PageNumberPaginationExtra'
}
```

## **Utilisation**
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
