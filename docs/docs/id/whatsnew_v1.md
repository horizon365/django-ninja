---
comments: true
---
# Selamat datang di Django Ninja 1.0


Untuk memulai, instal versi terbaru menggunakan perintah berikut:
```
pip install -U django-ninja
```

django-ninja v1 kompatibel dengan Python 3.7 ke atas.


Serie Django Ninja 0.x masih didukung, tetapi hanya akan menerima pembaruan keamanan dan perbaikan bug kritis.


✨ Apa yang baru di Django Ninja 1.0

## Dukungan Pydantic2

Pydantic versi 2 ditulis ulang dengan Rust dan mencakup banyak peningkatan serta fitur, seperti:

 - Tipe yang lebih aman.
 - Ekstensibilitas yang lebih baik.
 - Kinerja yang lebih baik.

Berdasarkan pengujian kami, proyek rata-rata dapat memperoleh peningkatan kinerja sekitar 10% secara rata-rata, sementara di beberapa skenario parsing/serialization tertentu Anda bisa mendapatkan peningkatan hingga 4x.
Di sisi lain, hal ini menimbulkan perubahan yang bersifat breaking — pydantic 1 dan 2 tidak sepenuhnya kompatibel — tetapi kami telah berusaha membuat transisi ini semudah mungkin.
Jadi jika Anda menggunakan class 'Schema', migrasi ke ninja v1 seharusnya langsung saja. Jika tidak, silakan ikuti [panduan migrasi pydantic](https://pydantic.com.cn/migration/)


Beberapa fitur baru yang disediakan oleh pydantic2

### pydantic context

Pydantic sekarang mendukung context selama validasi dan serialization, dan Django Ninja meneruskan objek "request" selama penanganan request dan response.
```Python hl_lines="6 7"
class Payload(Schema):
    id: int
    name: str
    request_path: str

    @staticmethod
    def resolve_request_path(data, context):
        request = context["request"]
        return request.get_full_path()

```

Pada fase response, "response_code" juga diteruskan ke context.

## Schema.Meta

Pydantic sekarang telah menandai class BaseModel.Config sebagai deprecated. Namun, untuk tetap konsisten dengan semua bagian Django lainnya, kami memperkenalkan class "Meta" untuk ModelSchema — cara kerjanya mirip dengan ModelForms milik Django:
```Python hl_lines="2 4"
class TxItem(ModelSchema):
    class Meta:
        model = Transaction
        fields = ["id", "account", "amount", "timestamp"]

```

(Class "Config" masih didukung, tetapi sekarang sudah deprecated)


## Sintaks parameter yang lebih pendek/lebih bersih

```python
@api.post('/some')
def some_form(request, username: Form[str], password: Form[str]):
    return True
```

alih-alih

```python
@api.post('/some')
def some_form(request, username: str = Form(...), password: str = Form(...)):
    return True
```

atau

```python
@api.post('/some')
def some_form(request, data: Form[AuthSchema]):
    return True
```


alih-alih

```python
@api.post('/some')
def some_form(request, data: AuthSchema = Form(...)):
    return True
```



serta semua fitur autocompletion di editor Anda.


Di sisi lain, **sintaks lama masih didukung**, sehingga Anda dapat memindahkan proyek Anda ke versi django-ninja terbaru tanpa repot.


#### + Annotated

typing.Annotated juga sekarang didukung:

```Python
@api.get("/annotated")
def annotated(request, data: Annotated[SomeData, Form()]):
    return {"data": data.dict()}

```


## Dukungan auth async

Authenticator async akhirnya didukung. Yang perlu Anda lakukan hanyalah menambahkan `async` ke method `authenticate` Anda:

```Python
class Auth(HttpBearer):
    async def authenticate(self, request, token):
        await asyncio.sleep(1)
        if token == "secret":
            return token

```


## Perubahan perilaku CSRF


`csrf=True` tidak lagi diperlukan jika Anda menggunakan authentication berbasis cookie. Sebagai gantinya, perlindungan CSRF diaktifkan secara otomatis. Ini juga memungkinkan Anda mencampur authenticator yang dilindungi CSRF dengan metode lain yang tidak memerlukan cookie:

```Python
api = NinjaAPI(auth=[django_auth, Auth()])
```


## Dokumentasi

Penampil dokumentasi sekarang dapat dikonfigurasi dan di-plug. Secara default, django-ninja dilengkapi dengan Swagger dan Redoc:
```Python
from ninja import NinjaAPI, Redoc, Swagger


# use redoc
api = NinjaAPI(docs=Redoc()))

# use swagger:
api = NinjaAPI(docs=Swagger())

# set configuration for swagger:
api = NinjaAPI(docs=Swagger({"persistAuthorization": True}))
```

Pengguna kini dapat membuat penampil dokumentasi kustom dengan melakukan subclass terhadap class `DocsBase`.

## Router

add_router mendukung path berupa string:

```Python
api = NinjaAPI()


api.add_router('/app1', 'myproject.app1.router')
api.add_router('/app2', 'myproject.app2.router')
api.add_router('/app3', 'myproject.app3.router')
api.add_router('/app4', 'myproject.app4.router')
api.add_router('/app5', 'myproject.app5.router')
```


## Decorators

Ketika django-ninja mendekorasi sebuah view dengan .get/.post dll., ia membungkus hasil dari fungsi tersebut (dalam kebanyakan kasus bukan sebuah HttpResponse - melainkan objek yang dapat diserialisasi), sehingga kemungkinan besar tidak akan bekerja dengan beberapa decorator bawaan atau pihak ketiga, seperti:
```python hl_lines="4"
from django.views.decorators.cache import cache_page

@api.get("/test")
@cache_page(5) # <----- will not work!
def test_view(request):
    return {"some": "Complex data"}
```
Contoh ini tidak akan berfungsi.

Sekarang django-ninja memperkenalkan decorator decorate_view yang memungkinkan penyuntikan decorator yang bekerja dengan http response:
```python hl_lines="1 4"
from ninja.decorators import decorate_view

@api.get("/test")
@decorate_view(cache_page(5))
def test_view(request):
    return str(datetime.now())
```


## Pagination

Method `paginate_queryset` sekarang menerima objek `request`


#### Item yang tidak kompatibel ke belakang
 - resolve_xxx(self, ...) - dukungan untuk resolusi (self) sudah deprecated, digantikan oleh fungsionalitas bawaan pydantic.
 - pydantic v1 tidak lagi didukung
 - python 3.6 tidak lagi didukung

Omong-omong - jika Anda menyukai proyek ini dan belum memberikan bintang GitHub - silakan berikan! [github star](img/github-star.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
