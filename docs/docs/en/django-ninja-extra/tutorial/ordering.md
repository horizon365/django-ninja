---
comments: true
---
# **Ordering**

**Django Ninja Extra** provides an intuitive ordering model using the `ordering` decorator from the Django-Ninja-Extra ordering module. It expects a queryset or list from the route function result.

> This feature was inspired by [DRF OrderingFilter](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter)

## **Attributes**

`def ordering(func_or_ordering_class: Any = NOT_SET, **ordering_params: Any) -> Callable[..., Any]:`

- func_or_ordering_class: Defines a route function or an ordering class. Default: `ninja_extra.ordering.Ordering`
- ordering_params: Additional parameters used to initialize the ordering class

### Change the Default Ordering Class

To change the default ordering class, you need to add a `NINJA_EXTRA` variable in `settings.py` with the key `ORDERING_CLASS` and a value defining the path to the ordering class.

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'ORDERING_CLASS': 'someapp.somemodule.CustomOrdering'
}
```

## **Usage**

- If you do not specify the `ordering_fields` parameter, all fields of the queryset will be used for ordering.
- For example, to order users by username
  > http://example.com/api/users?ordering=username
- The client can also specify reverse ordering by prefixing the field name with `-`, for example:
  > http://example.com/api/users?ordering=-username
- Multiple orderings can also be specified:
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

## Note

> If you use both the `paginate` decorator and the `ordering` decorator, the `paginate` decorator should be above the `ordering` decorator, because the data is sorted first and then paginated, for example:
>
> ```python
>    @route.get('', response=List[UserSchema])
>    @paginate
>    @ordering(Ordering, ordering_fields=['username', 'email'])
>    def get_users(self):
>        return user_model.objects.all()
> ```

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
