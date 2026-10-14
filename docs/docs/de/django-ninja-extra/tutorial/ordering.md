---
comments: true
---
# **Sortierung (Ordering)**

**Django Ninja Extra** bietet ein intuitives Sortiermodell unter Verwendung des Decorators `ordering` aus dem Ordering-Modul von Django-Ninja-Extra. Er erwartet ein Queryset oder eine Liste aus dem Ergebnis der Routenfunktion.

> Diese Funktion wurde von [DRF OrderingFilter](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter) inspiriert

## **Attribute**

`def ordering(func_or_ordering_class: Any = NOT_SET, **ordering_params: Any) -> Callable[..., Any]:`

- func_or_ordering_class: Definiert eine Routenfunktion oder eine Ordering-Klasse. Standard: `ninja_extra.ordering.Ordering`
- ordering_params: Zusätzliche Parameter, die zur Initialisierung der Ordering-Klasse verwendet werden

### Die Standard-Ordering-Klasse ändern

Um die Standard-Ordering-Klasse zu ändern, müssen Sie eine Variable `NINJA_EXTRA` in der `settings.py` mit dem Schlüssel `ORDERING_CLASS` und einem Wert hinzufügen, der den Pfad zur Ordering-Klasse definiert.

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'ORDERING_CLASS': 'someapp.somemodule.CustomOrdering'
}
```

## **Verwendung**

- Wenn Sie den Parameter `ordering_fields` nicht angeben, werden alle Felder des Querysets für die Sortierung verwendet.
- Um Benutzer beispielsweise nach Benutzername zu sortieren:
  > http://example.com/api/users?ordering=username
- Der Client kann auch eine umgekehrte Sortierung angeben, indem er dem Feldnamen ein `-` voranstellt, zum Beispiel:
  > http://example.com/api/users?ordering=-username
- Es können auch mehrere Sortierungen angegeben werden:
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

## Hinweis

> Wenn Sie sowohl den Decorator `paginate` als auch den Decorator `ordering` verwenden, sollte der Decorator `paginate` über dem Decorator `ordering` stehen, weil die Daten zuerst sortiert und dann paginiert werden, zum Beispiel:
>
> ```python
>    @route.get('', response=List[UserSchema])
>    @paginate
>    @ordering(Ordering, ordering_fields=['username', 'email'])
>    def get_users(self):
>        return user_model.objects.all()
> ```

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
