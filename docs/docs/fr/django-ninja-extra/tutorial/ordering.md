---
comments: true
---
# **Tri (Ordering)**

**Django Ninja Extra** fournit un modèle de tri intuitif à l'aide du décorateur `ordering` du module ordering de Django-Ninja-Extra. Il attend un queryset ou une liste provenant du résultat de la fonction de route.

> Cette fonctionnalité s'est inspirée du [DRF OrderingFilter](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter)

## **Attributs**

`def ordering(func_or_ordering_class: Any = NOT_SET, **ordering_params: Any) -> Callable[..., Any]:`

- func_or_ordering_class : Définit une fonction de route ou une classe de tri. Par défaut : `ninja_extra.ordering.Ordering`
- ordering_params : Paramètres supplémentaires utilisés pour initialiser la classe de tri

### Changer la classe de tri par défaut

Pour changer la classe de tri par défaut, vous devez ajouter une variable `NINJA_EXTRA` dans `settings.py` avec la clé `ORDERING_CLASS` et une valeur définissant le chemin vers la classe de tri.

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'ORDERING_CLASS': 'someapp.somemodule.CustomOrdering'
}
```

## **Utilisation**

- Si vous ne spécifiez pas le paramètre `ordering_fields`, tous les champs du queryset seront utilisés pour le tri.
- Par exemple, pour trier les utilisateurs par username
  > http://example.com/api/users?ordering=username
- Le client peut également spécifier un tri inverse en préfixant le nom du champ avec `-`, par exemple :
  > http://example.com/api/users?ordering=-username
- Plusieurs tris peuvent également être spécifiés :
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

## Remarque

> Si vous utilisez à la fois le décorateur `paginate` et le décorateur `ordering`, le décorateur `paginate` doit être placé au-dessus du décorateur `ordering`, car les données sont d'abord triées puis paginées, par exemple :
>
> ```python
>    @route.get('', response=List[UserSchema])
>    @paginate
>    @ordering(Ordering, ordering_fields=['username', 'email'])
>    def get_users(self):
>        return user_model.objects.all()
> ```

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
