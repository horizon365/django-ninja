---
comments: true
---
# Autentikasi

## Pendahuluan

**Django Ninja** menyediakan beberapa tools untuk membantu Anda menangani autentikasi dan otorisasi dengan mudah, cepat, dan secara standar, tanpa harus mempelajari <a href="https://swagger.io/docs/specification/authentication/" target="_blank">seluruh spesifikasi keamanan</a>.

Ide utamanya adalah ketika Anda mendeskripsikan sebuah operasi API, Anda dapat mendefinisikan objek autentikasi.
```python hl_lines="2 7"
{!./src/tutorial/authentication/code001.py!}
```

Dalam contoh ini, client hanya dapat memanggil method `pets` jika menggunakan autentikasi session Django (yang secara default berbasis cookie), jika tidak maka error HTTP-401 akan dikembalikan.
Jika Anda hanya ingin mengizinkan superusers, Anda dapat menggunakan `from ninja.security import django_auth_superuser` sebagai gantinya.
## Skema OpenAPI otomatis

Berikut adalah contoh di mana client perlu mengirimkan sebuah header untuk autentikasi:

`Authorization: Bearer supersecret`

```python hl_lines="4 5 6 7 10"
{!./src/tutorial/authentication/bearer01.py!}
```

Sekarang buka dokumentasi di <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a>.


![Swagger UI Auth](../img/auth-swagger-ui.png)

Sekarang, ketika Anda mengklik tombol **Authorize**, Anda akan diminta memasukkan token autentikasi Anda.

![Swagger UI Auth](../img/auth-swagger-ui-prompt.png)

Ketika Anda melakukan test call, setiap request akan menyertakan header otorisasi.

## Autentikasi global

Jika Anda perlu melindungi **semua** method API Anda, Anda dapat meneruskan argumen `auth` ke konstruktor `NinjaAPI`:


```python hl_lines="11 19"
from ninja import NinjaAPI, Form
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaAPI(auth=GlobalAuth())

# @api.get(...)
# def ...

# @api.post(...)
# def ...
```

Dan, jika Anda perlu meng-override beberapa method, Anda dapat melakukannya kembali pada level operasi dengan meneruskan argumen `auth`. Dalam contoh ini, autentikasi dinonaktifkan untuk operasi `/token`:
```python hl_lines="19"
{!./src/tutorial/authentication/global01.py!}
```

## Opsi autentikasi yang tersedia

### Fungsi kustom


Argumen "`auth=`" menerima callable apa pun. **NinjaAPI** hanya akan meneruskan autentikasi ketika callable tersebut mengembalikan nilai yang **truthy** (dikonversi menjadi boolean `True`). Nilai kembalian ini akan ditetapkan ke atribut `request.auth`.

```python hl_lines="1 2 3 6"
{!./src/tutorial/authentication/code002.py!}
```


### API keys

Beberapa API menggunakan API keys untuk otorisasi. API key adalah token yang diberikan client saat melakukan panggilan API untuk mengidentifikasi dirinya. Key dapat dikirim di query string:
```
GET /something?api_key=abcdef12345
```

Atau sebagai request header:

```
GET /something HTTP/1.1
X-API-Key: abcdef12345
```

Atau sebagai cookie:

```
GET /something HTTP/1.1
Cookie: X-API-KEY=abcdef12345
```

**Django Ninja** dilengkapi class bawaan untuk membantu Anda menangani situasi-situasi tersebut.


#### Di Query

```python hl_lines="1 2 5 6 7 8 9 10 11 12"
{!./src/tutorial/authentication/apikey01.py!}
```

Dalam contoh ini, kita mengambil token dari `GET['api_key']` dan mencari `Client` yang sesuai di database. Instance Client akan ditetapkan sebagai atribut `request.auth`.

Catatan: **`param_name`** adalah nama parameter GET yang akan diperiksa. Jika tidak diatur, digunakan default `"key"`.


#### Di Header

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey02.py!}
```

#### Di Cookie

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey03.py!}
```



### HTTP Bearer

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/bearer01.py!}
```

### Autentikasi HTTP Basic

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/basic01.py!}
```


## Beberapa authenticator sekaligus

Argumen **`auth`** juga memungkinkan Anda meneruskan beberapa authenticator:

```python hl_lines="18"
{!./src/tutorial/authentication/multiple01.py!}
```

Dalam kasus ini, **Django Ninja** akan memeriksa API key dari `GET` terlebih dahulu, dan jika tidak diatur atau tidak valid, akan memeriksa key di `header`.
Jika keduanya tidak valid, error autentikasi akan dilemparkan ke response.


## Autentikasi pada router

Gunakan argumen `auth` pada router untuk menerapkan authenticator ke semua operasi yang dideklarasikan di dalamnya:

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

Atau melalui konstruktor router
```python
router = Router(auth=BasicAuth())
```


## Exception kustom

Melemparkan exception yang memiliki exception handler akan mengembalikan response dari handler tersebut dengan cara yang sama seperti pada operasi:

```python hl_lines="1 4"
{!./src/tutorial/authentication/bearer02.py!}
```


## Autentikasi async

**Django Ninja** memiliki dukungan dasar untuk autentikasi asinkron. Meskipun class autentikasi default tidak kompatibel dengan async, Anda tetap dapat mendefinisikan callable autentikasi async kustom Anda dan meneruskannya dengan `auth`.

```python
async def async_auth(request):
    ...


@api.get("/pets", auth=async_auth)
def pets(request):
    ...
```


Untuk informasi lebih lanjut, lihat [Penanganan error](errors.md) .

!!! success

    Lanjutkan ke bagian berikutnya **[Testing](testing.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
