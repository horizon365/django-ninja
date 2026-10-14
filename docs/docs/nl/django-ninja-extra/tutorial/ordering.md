---
comments: true
---
# **Ordering**

**Django Ninja Extra** biedt een intuïtief ordering-model met behulp van de decorator `ordering` uit de ordering-module van Django-Ninja-Extra. Deze verwacht een queryset of lijst als resultaat van de routefunctie.

> Deze functie was geïnspireerd door [DRF OrderingFilter](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter)

## **Attributen**

`def ordering(func_or_ordering_class: Any = NOT_SET, **ordering_params: Any) -> Callable[..., Any]:`

- func_or_ordering_class: Definieert een routefunctie of een ordering-klasse. Standaard: `ninja_extra.ordering.Ordering`
- ordering_params: Aanvullende parameters die worden gebruikt om de ordering-klasse te initialiseren

### De Standaard Ordering-klasse Wijzigen

Om de standaard ordering-klasse te wijzigen, moet je een variabele `NINJA_EXTRA` toevoegen in `settings.py` met de sleutel `ORDERING_CLASS` en een waarde die het pad naar de ordering-klasse definieert.

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'ORDERING_CLASS': 'someapp.somemodule.CustomOrdering'
}
```

## **Gebruik**

- Als je de parameter `ordering_fields` niet specificeert, worden alle velden van de queryset gebruikt voor ordering.
- Bijvoorbeeld, om gebruikers te sorteren op username
  > http://example.com/api/users?ordering=username
- De client kan ook omgekeerde ordering specificeren door het veld vooraf te laten gaan door een `-`, bijvoorbeeld:
  > http://example.com/api/users?ordering=-username
- Er kunnen ook meerdere orderingen worden gespecificeerd:
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

## Opmerking

> Als je zowel de decorator `paginate` als de decorator `ordering` gebruikt, moet de decorator `paginate` boven de decorator `ordering` staan, omdat de gegevens eerst worden gesorteerd en daarna gepagineerd, bijvoorbeeld:
>
> ```python
>    @route.get('', response=List[UserSchema])
>    @paginate
>    @ordering(Ordering, ordering_fields=['username', 'email'])
>    def get_users(self):
>        return user_model.objects.all()
> ```

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
