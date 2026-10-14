---
comments: true
---
# Pagination

**Django Ninja** dilengkapi dengan dukungan pagination. Ini memungkinkan Anda membagi result set yang besar menjadi halaman-halaman terpisah.


Untuk menerapkan pagination ke sebuah fungsi — cukup terapkan decorator `paginate`:

```python hl_lines="1 4"
from ninja.pagination import paginate

@api.get('/users', response=List[UserSchema])
@paginate
def list_users(request):
    return User.objects.all()
```


Selesai!

Sekarang Anda dapat mem-query users menggunakan parameter GET `limit` dan `offset`

```
/api/users?limit=10&offset=0
```

Secara default, limit disetel ke `100` (Anda dapat mengubahnya di settings.py Anda menggunakan `NINJA_PAGINATION_PER_PAGE`)


## Class Pagination Bawaan

### LimitOffsetPagination (default)

Ini adalah class pagination default (Anda dapat mengubahnya di settings.py Anda dengan mengarahkan `NINJA_PAGINATION_CLASS` ke path sebuah class)

```python hl_lines="1 4"
from ninja.pagination import paginate, LimitOffsetPagination

@api.get('/users', response=List[UserSchema])
@paginate(LimitOffsetPagination)
def list_users(request):
    return User.objects.all()
```

Contoh query:
```
/api/users?limit=10&offset=0
```

Class ini memiliki dua parameter input:

 - `limit` - menentukan jumlah querysets dalam satu halaman (default = 100, dapat diubah melalui NINJA_PAGINATION_PER_PAGE)
 - `offset` - menyetel offset jendela halaman (default: 0, pengindeksan dimulai dari 0)


### PageNumberPagination
```python hl_lines="1 4"
from ninja.pagination import paginate, PageNumberPagination

@api.get('/users', response=List[UserSchema])
@paginate(PageNumberPagination)
def list_users(request):
    return User.objects.all()
```

Contoh query:
```
/api/users?page=2
```

Class ini memiliki satu parameter `page` dan secara default mengeluarkan 100 querysets per halaman (dapat diubah melalui settings.py)

Penomoran halaman dimulai dari 1.

Anda juga dapat menyetel nilai page size kustom untuk setiap view secara terpisah:

```python hl_lines="2"
@api.get("/users")
@paginate(PageNumberPagination, page_size=50)
def list_users(...
```



## Mengakses Parameter Pagination di View Function

Jika Anda perlu mengakses parameter `Input` yang digunakan untuk pagination di view function Anda — gunakan argumen `pass_parameter`

Dalam kasus tersebut, data input akan tersedia di `**kwargs`:

```python hl_lines="2 4"
@api.get("/someview")
@paginate(pass_parameter="pagination_info")
def someview(request, **kwargs):
    page = kwargs["pagination_info"].page
    return ...
```


## Membuat Class Pagination Kustom

Untuk membuat class pagination kustom, Anda harus mewarisi dari `ninja.pagination.PaginationBase` dan meng-override class schema `Input` dan `Output` serta method `paginate_queryset(self, queryset, request, **params)`:

 - Schema `Input` adalah class schema yang mendeskripsikan parameter yang harus diteruskan ke paginator (seperti nomor halaman atau nilai limit/offset).
 - Schema `Output` mendeskripsikan skema output halaman (seperti count/next/items, dll.).
 - Method `paginate_queryset` menerima queryset awal dan harus mengembalikan iterable yang hanya berisi data pada halaman yang diminta. Method ini menerima parameter berikut:
    - `queryset`: queryset (atau iterable) yang dikembalikan oleh fungsi API.
    - `pagination` - parameter paginator.Input (yang telah di-parsing dan divalidasi)
    - `**params`: keyword arguments yang akan berisi semua argumen yang diterima fungsi yang didekorasi.


Contoh:

```python hl_lines="7 11 16 26"
from ninja.pagination import paginate, PaginationBase
from ninja import Schema


class CustomPagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        skip: int
        

    class Output(Schema):
        items: List[Any] # `items` is a default attribute
        total: int
        per_page: int

    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        return {
            'items': queryset[skip : skip + 5],
            'total': queryset.count(),
            'per_page': 5,
        }


@api.get('/users', response=List[UserSchema])
@paginate(CustomPagination)
def list_users(request):
    return User.objects.all()
```

Tips: Anda bisa mendapatkan objek request dari parameters:

```python
def paginate_queryset(self, queryset, pagination: Input, **params):
    request = params["request"]
```

#### Async Pagination

Class pagination standar **Django Ninja** mendukung async. Jika Anda ingin menangani request async dengan class pagination kustom, Anda harus mewarisi dari `ninja.pagination.AsyncPaginationBase` dan meng-override method `apaginate_queryset(self, queryset, request, **params)`.

### Output Attributes

Secara default, item halaman ditempatkan pada atribut `'items'`. Untuk mengubah perilaku ini, Anda dapat menggunakan `items_attribute`:

```python hl_lines="4 8"
class CustomPagination(PaginationBase):
    ...
    class Output(Schema):
        results: List[Any]
        total: int
        per_page: int
    
    items_attribute: str = "results"

```


## Menerapkan Pagination ke Beberapa Operation Sekaligus

Sering ada kasus di mana Anda perlu menambahkan pagination ke semua view yang mengembalikan querysets atau lists

Anda dapat menggunakan class router bawaan (`RouterPaginated`) yang akan otomatis menyuntikkan pagination ke semua operation yang didefinisikan dengan `response=List[SomeSchema]`:

```python hl_lines="1 3 6 10"
from ninja.pagination import RouterPaginated

router = RouterPaginated()


@router.get("/items", response=List[MySchema])
def items(request):
    return MyModel.objects.all()

@router.get("/other-items", response=List[OtherSchema])
def ohter_items(request):
    return OtherModel.objects.all()

```

Dalam contoh ini, kedua operation akan memiliki pagination yang aktif.

Untuk menerapkan pagination ke instance `api` utama, Anda dapat menggunakan argumen `default_router`:


```python
api = NinjaAPI(default_router=RouterPaginated())

@api.get(...
```

!!! done

    Lanjutkan ke bab berikutnya! **[Response Renderers](response-renderers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
