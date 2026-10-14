---
comments: true
---
# **Paginasi**

**Django Ninja Extra** menyediakan model paginasi yang intuitif menggunakan dekorator `paginate` dari module pagination Django-Ninja-Extra. Fitur ini mengharapkan list atau queryset dari hasil fungsi route.

## **Atribut**

`def paginate(func_or_pgn_class: Any = NOT_SET, **paginator_params: Any) -> Callable[..., Any]:`

- func_or_pgn_class: Mendefinisikan fungsi route atau kelas pagination. Default: `ninja_extra.pagination.LimitOffsetPagination`
- paginator_params: Parameter tambahan yang digunakan untuk menginisialisasi kelas pagination

### **Menggunakan Ninja LimitOffsetPagination**
Saat menggunakan `ninja_extra.pagination.LimitOffsetPagination`, Anda harus menggunakan `NinjaPaginationResponseSchema` sebagai pembungkus response schema paginasi.

Sebagai contoh: 
```python
from ninja_extra.schemas import NinjaPaginationResponseSchema

...

@route.get('', response=NinjaPaginationResponseSchema[UserSchema])
@paginate()
def list_items(self):
    return item_model.objects.all()
```
    

### **Mengubah Kelas Pagination Default**
Untuk mengubah kelas pagination default, Anda perlu menambahkan variabel `NINJA_EXTRA` di `settings.py` dengan key `PAGINATION_CLASS` dan nilai yang mendefinisikan path menuju kelas pagination tersebut.
```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'PAGINATION_CLASS': 'ninja_extra.pagination.PageNumberPaginationExtra'
}
```

## **Penggunaan**
```python
from typing import List
from ninja_extra.pagination import (
    paginate, PageNumberPaginationExtra, PaginatedResponseSchema
)
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
    @route.get('', response=PaginatedResponseSchema[UserSchema])
    @paginate(PageNumberPaginationExtra, page_size=50)
    def get_users(self):
        return user_model.objects.all()
    
    @route.get('/limit', response=List[UserSchema])
    @paginate
    def get_users_with_limit(self):
        # this will use default paginator class - ninja_extra.pagination.LimitOffsetPagination
        return user_model.objects.all()

    
api = NinjaExtraAPI(title='Pagination Test')
api.register_controllers(UserController)
```

![Preview](../images/pagination_example.gif)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
