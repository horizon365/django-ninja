---
comments: true
---
# **Recherche (Searching)**

**Django Ninja Extra** fournit un modèle de recherche intuitif à l'aide du décorateur `searching` du module searching de Django-Ninja-Extra. Il attend un queryset ou une liste provenant du résultat de la fonction de route.

> Cette fonctionnalité s'est inspirée du [DRF SearchFilter](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)

## **Attributs**

`def searching(func_or_searching_class: Any = NOT_SET, **searching_params: Any) -> Callable[..., Any]:`

- func_or_searching_class : Définit une fonction de route ou une classe de recherche. Par défaut : `ninja_extra.searching.Searching`
- searching_params : Paramètres supplémentaires utilisés pour initialiser la classe de recherche

### Changer la classe de recherche par défaut

Pour changer la classe de recherche par défaut, vous devez ajouter une variable `NINJA_EXTRA` dans `settings.py` avec la clé `SEARCHING_CLASS` et une valeur définissant le chemin vers la classe de recherche

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'SEARCHING_CLASS': 'someapp.somemodule.CustomSearching'
}
```

## **Utilisation**

- Si vous ne spécifiez pas le paramètre `search_fields`, les résultats inchangés seront renvoyés.
- Par exemple, pour rechercher des utilisateurs par username ou email :
  > http://example.com/api/users?search=someuser
- Vous pouvez également utiliser la notation à double tiret bas de l'API lookup pour effectuer des recherches sur des champs liés par clé étrangère ou de type many-to-many :
  > search_fields = ['username', 'email', 'profile__profession']
- Par défaut, la recherche utilise une correspondance partielle insensible à la casse. Le paramètre de recherche peut contenir plusieurs termes de recherche, qui doivent être séparés par des espaces et/ou des virgules. Si plusieurs termes de recherche sont utilisés, seuls les objets correspondant à tous les termes fournis seront renvoyés dans la liste. Le comportement de recherche peut être restreint en ajoutant divers caractères avant les `search_fields`.

  * '^' Recherche par préfixe (commence par).
  * '=' Correspondance exacte.
  * '@' Recherche plein texte. (Actuellement prise en charge uniquement par le [backend PostgreSQL de Django](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/).)
  * '$' Recherche par expression régulière.

  Par exemple :

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

## Remarque

> Si vous utilisez simultanément le décorateur `paginate`, le décorateur `ordering` et le décorateur `searching`, alors `paginate` doit être placé au-dessus du décorateur `ordering`, et le décorateur `ordering` doit être placé au-dessus du décorateur `searching`. En effet, les données sont d'abord filtrées, puis triées, et enfin paginées, par exemple :
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
