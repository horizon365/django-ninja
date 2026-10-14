---
comments: true
---
# **Pencarian**

**Django Ninja Extra** menyediakan model pencarian (searching) yang intuitif menggunakan dekorator `searching` dari module searching Django-Ninja-Extra. Fitur ini mengharapkan queryset atau list dari hasil fungsi route.

> Fitur ini terinspirasi dari [DRF SearchFilter](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)

## **Atribut**

`def searching(func_or_searching_class: Any = NOT_SET, **searching_params: Any) -> Callable[..., Any]:`

- func_or_searching_class: Mendefinisikan fungsi route atau kelas searching. Default: `ninja_extra.searching.Searching`
- searching_params: Parameter tambahan yang digunakan untuk menginisialisasi kelas searching

### Mengubah Kelas Searching Default

Untuk mengubah kelas searching default, Anda perlu menambahkan variabel `NINJA_EXTRA` di `settings.py` dengan key `SEARCHING_CLASS` dan nilai yang mendefinisikan path menuju kelas searching tersebut

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'SEARCHING_CLASS': 'someapp.somemodule.CustomSearching'
}
```

## **Penggunaan**

- Jika Anda tidak menentukan parameter `search_fields`, hasil akan dikembalikan tanpa perubahan.
- Sebagai contoh, untuk mencari users berdasarkan username atau email:
  > http://example.com/api/users?search=someuser
- Anda juga dapat menggunakan notasi double underscore dari lookup API untuk melakukan lookup terhadap relasi pada field foreign key atau many-to-many:
  > search_fields = ['username', 'email', 'profile__profession']
- Secara default, pencarian menggunakan pencocokan sebagian (partial match) yang tidak peka huruf besar/kecil. Parameter search dapat berisi beberapa istilah pencarian, yang harus dipisahkan dengan spasi dan/atau koma. Jika beberapa istilah pencarian digunakan, hanya objek yang cocok dengan semua istilah yang diberikan yang akan dikembalikan dalam list. Perilaku pencarian dapat dibatasi dengan menambahkan berbagai karakter sebelum `search_fields`.

  * '^' Pencarian berdasarkan awalan (starts-with).
  * '=' Kecocokan persis (exact match).
  * '@' Pencarian full-text. (Saat ini hanya didukung oleh [backend PostgreSQL](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/) milik Django.)
  * '$' Pencarian regex.

  Sebagai contoh:

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

## Catatan

> Jika Anda menggunakan dekorator `paginate`, dekorator `ordering`, dan dekorator `searching` secara bersamaan, maka `paginate` harus diletakkan di atas dekorator `ordering`, dan dekorator `ordering` harus diletakkan di atas dekorator `searching`. Karena data difilter terlebih dahulu, lalu diurutkan, dan terakhir dipaginasi, misalnya:
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
