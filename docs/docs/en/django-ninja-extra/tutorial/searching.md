---
comments: true
---
# **Searching**

**Django Ninja Extra** provides an intuitive searching model using the `searching` decorator from the Django-Ninja-Extra searching module. It expects a queryset or list from the route function result.

> This feature was inspired by [DRF SearchFilter](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)

## **Attributes**

`def searching(func_or_searching_class: Any = NOT_SET, **searching_params: Any) -> Callable[..., Any]:`

- func_or_searching_class: Defines a route function or a searching class. Default: `ninja_extra.searching.Searching`
- searching_params: Additional parameters used to initialize the searching class

### Change the Default Searching Class

To change the default searching class, you need to add a `NINJA_EXTRA` variable in `settings.py` with the key `SEARCHING_CLASS` and a value defining the path to the searching class

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'SEARCHING_CLASS': 'someapp.somemodule.CustomSearching'
}
```

## **Usage**

- If you do not specify the `search_fields` parameter, the unchanged results will be returned.
- For example, to search users by username or email:
  > http://example.com/api/users?search=someuser
- You can also use the lookup API double-underscore notation to perform related lookups on foreign key or many-to-many fields:
  > search_fields = ['username', 'email', 'profile__profession']
- By default, the search will use case-insensitive partial matching. The search parameter may contain multiple search terms, which should be separated by spaces and/or commas. If multiple search terms are used, then only objects that match all the provided terms will be returned in the list. The search behavior can be restricted by adding various characters before the `search_fields`.

  * '^' Search by starts-with.
  * '=' Exact match.
  * '@' Full-text search. (Currently only supported by Django's [PostgreSQL backend](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/).)
  * '$' Regex search.

  For example:

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

## Note

> If you use the `paginate` decorator, the `ordering` decorator, and the `searching` decorator at the same time, then `paginate` should be above the `ordering` decorator, and the `ordering` decorator should be above the `searching` decorator. Because the data is filtered first, then sorted, and finally paginated, for example:
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
