---
comments: true
---
# **Suche (Searching)**

**Django Ninja Extra** bietet ein intuitives Suchmodell unter Verwendung des Decorators `searching` aus dem Searching-Modul von Django-Ninja-Extra. Er erwartet ein Queryset oder eine Liste aus dem Ergebnis der Routenfunktion.

> Diese Funktion wurde von [DRF SearchFilter](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter) inspiriert

## **Attribute**

`def searching(func_or_searching_class: Any = NOT_SET, **searching_params: Any) -> Callable[..., Any]:`

- func_or_searching_class: Definiert eine Routenfunktion oder eine Searching-Klasse. Standard: `ninja_extra.searching.Searching`
- searching_params: Zusätzliche Parameter, die zur Initialisierung der Searching-Klasse verwendet werden

### Die Standard-Searching-Klasse ändern

Um die Standard-Searching-Klasse zu ändern, müssen Sie eine Variable `NINJA_EXTRA` in der `settings.py` mit dem Schlüssel `SEARCHING_CLASS` und einem Wert hinzufügen, der den Pfad zur Searching-Klasse definiert

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'SEARCHING_CLASS': 'someapp.somemodule.CustomSearching'
}
```

## **Verwendung**

- Wenn Sie den Parameter `search_fields` nicht angeben, werden die unveränderten Ergebnisse zurückgegeben.
- Um Benutzer beispielsweise nach Benutzername oder E-Mail zu durchsuchen:
  > http://example.com/api/users?search=someuser
- Sie können auch die Doppel-Unterstrich-Notation der Lookup-API verwenden, um verwandte Lookups auf Fremdschlüssel- oder Many-to-Many-Feldern durchzuführen:
  > search_fields = ['username', 'email', 'profile__profession']
- Standardmäßig verwendet die Suche eine case-insensitive Teilübereinstimmung. Der Suchparameter kann mehrere Suchbegriffe enthalten, die durch Leerzeichen und/oder Kommas getrennt werden sollten. Werden mehrere Suchbegriffe verwendet, werden nur Objekte, die alle angegebenen Begriffe erfüllen, in der Liste zurückgegeben. Das Suchverhalten kann durch Voranstellen verschiedener Zeichen vor die `search_fields` eingeschränkt werden.

  * '^' Suche nach Präfix (starts-with).
  * '=' Exakte Übereinstimmung.
  * '@' Volltextsuche. (Derzeit nur von Djangos [PostgreSQL-Backend](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/) unterstützt.)
  * '$' Regex-Suche.

  Zum Beispiel:

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

## Hinweis

> Wenn Sie den Decorator `paginate`, den Decorator `ordering` und den Decorator `searching` gleichzeitig verwenden, sollte `paginate` über dem Decorator `ordering` stehen, und der Decorator `ordering` sollte über dem Decorator `searching` stehen. Denn die Daten werden zuerst gefiltert, dann sortiert und schließlich paginiert, zum Beispiel:
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
