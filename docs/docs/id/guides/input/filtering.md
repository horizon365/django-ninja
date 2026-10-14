---
comments: true
---
# Filtering

Jika Anda ingin mengizinkan pengguna memfilter querysets Anda berdasarkan beberapa atribut yang berbeda, ada baiknya Anda mengenkapsulasi filter Anda ke dalam sebuah class `FilterSchema`.
`FilterSchema` adalah `Schema` biasa, jadi ia menggunakan semua fitur Pydantic yang diperlukan, tetapi juga menambahkan beberapa kemudahan
untuk mengonversi parameter filtering yang dihadapi pengguna menjadi query database dengan mudah.

Pertama, definisikan subclass dari `FilterSchema`:

```python hl_lines="6 7 8"
from ninja import FilterSchema, Field
from typing import Optional


class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    author: Optional[str] = None
    created_after: Optional[datetime] = None
```


Selanjutnya, gunakan schema ini bersama dengan `Query` di API handler Anda:
```python hl_lines="2"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

Sama seperti yang dijelaskan di [Menggunakan Schema untuk Mendefinisikan Query Parameters](./query-params.md#using-schema), Django Ninja mengubah field yang didefinisikan dalam `BookFilterSchema` menjadi query parameters.
Anda dapat menggunakan shorthand satu baris `.filter()` untuk menerapkan filter-filter tersebut ke queryset Anda:
```python hl_lines="4"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

Di balik layar, `FilterSchema` mengonversi field-fieldnya menjadi [ekspresi Q](https://docs.djangoproject.com/en/3.1/topics/db/queries/#complex-lookups-with-q-objects), lalu menggabungkannya dan menggunakannya untuk memfilter queryset Anda.


Sebagai alternatif, alih-alih menggunakan method `.filter`, Anda bisa mengambil ekspresi `Q` yang sudah disiapkan dan melakukan filtering sendiri.
Ini dapat berguna ketika Anda memiliki filtering queryset tambahan di luar yang Anda ekspos ke pengguna melalui API:
```python hl_lines="5 8"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):

    # Never serve books from inactive publishers and authors
    q = Q(author__is_active=True) | Q(publisher__is_active=True)
    
    # But allow filtering the rest of the books
    q &= filters.get_filter_expression()
    return Book.objects.filter(q)
```

Secara default, filter akan berperilaku sebagai berikut:

* Nilai `None` akan diabaikan dan tidak ada filtering yang diterapkan;
* Setiap field yang tidak bernilai `None` akan dikonversi menjadi ekspresi `Q` sesuai dengan definisi `Field` masing-masing field;
* Semua ekspresi `Q` akan digabungkan menjadi satu menggunakan operator logika `AND`;
* Ekspresi `Q` yang dihasilkan digunakan untuk memfilter queryset, dan queryset dengan klausa `.filter` yang diterapkan dikembalikan kepada Anda.

## Custom Fields
Secara default, `FilterSet` menggunakan nama field untuk menghasilkan ekspresi Q:
```python
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
```
Field `name` akan dikonversi menjadi ekspresi `Q(name=...)`.

Ketika lookup database Anda lebih kompleks dari itu, Anda dapat menentukannya secara eksplisit menggunakan keyword argument `"q"` pada definisi field:
```python hl_lines="2"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains') 
```
Anda bahkan dapat menentukan beberapa nama keyword argument lookup sebagai list:
```python hl_lines="2 3 4"
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains',
                                     'author__name__icontains',
                                     'publisher__name__icontains']) 
```
Secara default, ekspresi pada level field digabungkan menggunakan konektor `"OR"`, jadi dengan pengaturan di atas, query parameter `?search=foobar` akan mencari buku yang mengandung "foobar" pada name, author, atau publisher-nya.


## Menggabungkan Ekspresi
Secara default,

* ekspresi pada level field digabungkan menggunakan operator `OR`.
* field-field itu sendiri digabungkan menggunakan operator `AND`.

Jadi, untuk `FilterSchema` berikut...
```python
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains', 'author__name__icontains'])
    popular: Optional[bool] = None
```
...dan query parameters berikut dari seorang pengguna
```
http://localhost:8000/api/books?search=harry&popular=true
```
Instance `FilterSchema` akan mencari buku-buku populer yang mengandung `harry` pada nama buku _atau_ nama author-nya.


Anda dapat mengkustomisasi perilaku ini menggunakan parameter `expression_connector` baik pada definisi level field maupun level class:
```python hl_lines="3 7"
class BookFilterSchema(FilterSchema):
    active: Optional[bool] = Field(None, q=['is_active', 'publisher__is_active'],
                                   expression_connector='AND')
    name: Optional[str] = Field(None, q='name__icontains')
    
    class Config:
        expression_connector = 'OR'
```

Expression connector dapat menerima nilai `"OR"`, `"AND"`, dan `"XOR"`, tetapi yang terakhir hanya [didukung](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#xor) di Django 4.1.

Sekarang, sebuah request dengan query parameters berikut
```
http://localhost:8000/api/books?name=harry&active=true
```
...akan mencari buku yang memiliki `harry` pada namanya _atau_ buku yang aktif itu sendiri dan diterbitkan oleh publisher yang aktif.


## Filtering dengan Nilai None
Anda dapat membuat `FilterSchema` memperlakukan `None` sebagai nilai valid yang tetap difilter.

Ini dapat dilakukan pada level field melalui keyword argument `ignore_none`:
```python hl_lines="3"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
```

Dengan begitu, ketika pengguna tidak memberikan nilai lain untuk `"tag"`, filter akan selalu menyertakan kondisi `tag=None`.

Anda juga dapat menentukan ini untuk semua field sekaligus di konfigurasi:
```python hl_lines="6"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
    
    class Config:
        ignore_none = False
```


## Ekspresi Kustom
Terkadang Anda mungkin memiliki skenario filtering yang kompleks yang tidak dapat ditangani oleh anotasi field tunggal.
Untuk kasus tersebut, Anda dapat mengimplementasikan logika filtering field Anda sebagai method kustom. Cukup definisikan sebuah method bernama `filter_<fieldname>` yang menerima nilai filter dan mengembalikan ekspresi Q:

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    tag: Optional[str] = None
    popular: Optional[bool] = None
    
    def filter_popular(self, value: bool) -> Q:
        return Q(view_count__gt=1000) | Q(download_count__gt=100) if value else Q()
```
Method field semacam ini lebih diutamakan daripada yang ditentukan pada definisi `Field()` field terkait.
Jika itu masih belum cukup, Anda dapat mengimplementasikan logika filtering kustom Anda sendiri untuk seluruh class `FilterSet` di method `custom_expression`:

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    popular: Optional[bool] = None

    def custom_expression(self) -> Q:
        q = Q()
        if self.name:
            q &= Q(name__icontains=self.name)
        if self.popular:
            q &= (
                Q(view_count__gt=1000) |
                Q(downloads__gt=100) |
                Q(tag='popular')
            )
        return q
```
Method `custom_expression` lebih diutamakan daripada definisi lain apa pun yang dijelaskan di atas, termasuk method `filter_<fieldname>`.

!!! done

    Seri parameter input telah selesai! Lanjutkan ke bagian berikutnya **[Menangani Response](../response/index.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
