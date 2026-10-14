---
comments: true
---
# **Pengurutan**

**Django Ninja Extra** menyediakan model pengurutan (ordering) yang intuitif menggunakan dekorator `ordering` dari module ordering Django-Ninja-Extra. Fitur ini mengharapkan queryset atau list dari hasil fungsi route.

> Fitur ini terinspirasi dari [DRF OrderingFilter](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter)

## **Atribut**

`def ordering(func_or_ordering_class: Any = NOT_SET, **ordering_params: Any) -> Callable[..., Any]:`

- func_or_ordering_class: Mendefinisikan fungsi route atau kelas ordering. Default: `ninja_extra.ordering.Ordering`
- ordering_params: Parameter tambahan yang digunakan untuk menginisialisasi kelas ordering

### Mengubah Kelas Ordering Default

Untuk mengubah kelas ordering default, Anda perlu menambahkan variabel `NINJA_EXTRA` di `settings.py` dengan key `ORDERING_CLASS` dan nilai yang mendefinisikan path menuju kelas ordering tersebut.

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'ORDERING_CLASS': 'someapp.somemodule.CustomOrdering'
}
```

## **Penggunaan**

- Jika Anda tidak menentukan parameter `ordering_fields`, semua field dari queryset akan digunakan untuk pengurutan.
- Sebagai contoh, untuk mengurutkan users berdasarkan username
  > http://example.com/api/users?ordering=username
- Client juga dapat menentukan urutan terbalik dengan menambahkan awalan `-` pada nama field, misalnya:
  > http://example.com/api/users?ordering=-username
- Beberapa pengurutan juga dapat ditentukan sekaligus:
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

## Catatan

> Jika Anda menggunakan dekorator `paginate` sekaligus dekorator `ordering`, dekorator `paginate` harus diletakkan di atas dekorator `ordering`, karena data diurutkan terlebih dahulu lalu dipaginasi, misalnya:
>
> ```python
>    @route.get('', response=List[UserSchema])
>    @paginate
>    @ordering(Ordering, ordering_fields=['username', 'email'])
>    def get_users(self):
>        return user_model.objects.all()
> ```

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
