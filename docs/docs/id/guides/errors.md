---
comments: true
---
# Penanganan error

**Django Ninja** memungkinkan Anda memasang custom exception handlers untuk mengendalikan bagaimana response dikembalikan ketika terjadi error atau exception yang tertangani.

## Custom exception handlers

Misalkan Anda membangun sebuah API yang bergantung pada service eksternal tertentu yang memang dirancang untuk tidak tersedia pada momen-momen tertentu. Anda dapat menangani error tersebut dan mengembalikan response yang ramah kepada client (memberi tahu mereka untuk kembali lagi nanti) alih-alih melemparkan error 500 default ketika exception terjadi.
Untuk mencapainya, Anda perlu:

 - 1) Membuat sebuah exception (atau menggunakan yang sudah ada)
 - 2) Menggunakan decorator api.exception_handler


Contoh:


```python hl_lines="9 10"
api = NinjaAPI()

class ServiceUnavailableError(Exception):
    pass


# inisialisasi handler

@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=503,
    )


# beberapa logika yang melempar exception

@api.get("/service")
def some_operation(request):
    if random.choice([True, False]):
        raise ServiceUnavailableError()
    return {"message": "Hello"}

```

Fungsi exception handler menerima 2 argumen:

 - **request** - HTTP request milik Django
 - **exc** - exception yang sebenarnya terjadi

Fungsi tersebut harus mengembalikan sebuah HTTP response

## Meng-override exception handler default

Secara default, **Django Ninja** menginisialisasi exception handler berikut:


#### `ninja.errors.AuthenticationError`

Dilemparkan ketika data autentikasi tidak valid

#### `ninja.errors.ValidationError`

Dilemparkan ketika data request gagal validasi

#### `ninja.errors.HttpError`

Digunakan untuk melemparkan HTTP error dengan status code dari bagian mana pun dalam kode
#### `django.http.Http404`
 
Exception 404 default Django (dapat dikembalikan, misalnya, menggunakan get_object_or_404)
#### `Exception`
 
Exception lain apa pun yang tidak ditangani oleh aplikasi.
Perilaku default
 
  - **Jika `settings.DEBUG` bernilai `True`** - mengembalikan traceback dalam bentuk teks biasa (berguna saat debugging di console atau Swagger UI)
  - **else** - menggunakan mekanisme penanganan exception default Django (logging error, mengirim email ke ADMINS)


### Meng-override handler default

Jika Anda perlu mengubah output default dari validation errors - override exception handler ValidationError:

```python hl_lines="1 4"
from ninja.errors import ValidationError
...

@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return HttpResponse("Invalid input", status=422)
```


## Melempar HTTP response melalui exception

Sebagai alternatif dari membuat custom exception dan menulis handler untuknya - Anda juga dapat melemparkan HTTP exception, yang akan menghasilkan HTTP response dengan code yang diinginkan dikembalikan

```python
from ninja.errors import HttpError

@api.get("/some/resource")
def some_operation(request):
    if True:
        raise HttpError(503, "Service Unavailable. Please retry later.")

```
!!! success

    Lanjutkan ke bagian berikutnya **[Reversing URLs](urls.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
