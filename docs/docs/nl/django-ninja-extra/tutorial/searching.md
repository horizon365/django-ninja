---
comments: true
---
# **Searching**

**Django Ninja Extra** biedt een intuïtief zoekmodel met behulp van de decorator `searching` uit de searching-module van Django-Ninja-Extra. Deze verwacht een queryset of lijst als resultaat van de routefunctie.

> Deze functie was geïnspireerd door [DRF SearchFilter](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)

## **Attributen**

`def searching(func_or_searching_class: Any = NOT_SET, **searching_params: Any) -> Callable[..., Any]:`

- func_or_searching_class: Definieert een routefunctie of een searching-klasse. Standaard: `ninja_extra.searching.Searching`
- searching_params: Aanvullende parameters die worden gebruikt om de searching-klasse te initialiseren

### De Standaard Searching-klasse Wijzigen

Om de standaard searching-klasse te wijzigen, moet je een variabele `NINJA_EXTRA` toevoegen in `settings.py` met de sleutel `SEARCHING_CLASS` en een waarde die het pad naar de searching-klasse definieert

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'SEARCHING_CLASS': 'someapp.somemodule.CustomSearching'
}
```

## **Gebruik**

- Als je de parameter `search_fields` niet specificeert, worden de ongewijzigde resultaten geretourneerd.
- Bijvoorbeeld, om gebruikers te zoeken op username of e-mail:
  > http://example.com/api/users?search=someuser
- Je kunt ook de dubbele-onderstreepnotatie van de lookup-API gebruiken om gerelateerde lookups uit te voeren op foreign key- of many-to-many-velden:
  > search_fields = ['username', 'email', 'profile__profession']
- Standaard gebruikt de zoekopdracht hoofdletterongevoelige partiële matching. De zoekparameter kan meerdere zoektermen bevatten, die moeten worden gescheiden door spaties en/of komma's. Als er meerdere zoektermen worden gebruikt, worden alleen objecten die aan alle opgegeven termen voldoen, in de lijst geretourneerd. Het zoekgedrag kan worden beperkt door verschillende tekens vóór de `search_fields` toe te voegen.

  * '^' Zoeken op begint-met.
  * '=' Exacte overeenkomst.
  * '@' Full-text zoeken. (Momenteel alleen ondersteund door Django's [PostgreSQL-backend](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/).)
  * '$' Regex-zoekopdracht.

  Bijvoorbeeld:

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

## Opmerking

> Als je de decorator `paginate`, de decorator `ordering` en de decorator `searching` tegelijk gebruikt, moet `paginate` boven de decorator `ordering` staan, en moet de decorator `ordering` boven de decorator `searching` staan. Omdat de gegevens eerst worden gefilterd, vervolgens gesorteerd en ten slotte gepagineerd, bijvoorbeeld:
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
