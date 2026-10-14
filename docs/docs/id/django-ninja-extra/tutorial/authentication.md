---
comments: true
---
# **Autentikasi**

**Django Ninja Extra** menyediakan API yang sama dengan **Django Ninja** dalam hal otorisasi dan autentikasi, sehingga menjamin konsistensi dan kemudahan penggunaan di antara kedua package tersebut.

## **OpenAPI Schema Otomatis**

Berikut adalah contoh di mana client perlu menyertakan header untuk autentikasi:

`Authorization: Bearer supersecret`

```Python
from ninja.security import HttpBearer
from ninja_extra import api_controller, route
from ninja.constants import NOT_SET


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token

@api_controller(tags=['My Operations'], auth=NOT_SET, permissions=[])
class MyController:
    @route.get("/bearer", auth=AuthBearer())
    def bearer(self):
        return {"token": self.context.request.auth}

```

## **Autentikasi Global** 

Jika Anda perlu melindungi **semua** method route yang didefinisikan di `api` dan APIController, Anda dapat meneruskan parameter `auth` ke konstruktor `NinjaExtraAPI`:


```Python
from ninja_extra import NinjaExtraAPI
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaExtraAPI(auth=GlobalAuth())

```
Baca selengkapnya tentang [autentikasi](https://django-ninja.cn/guides/authentication/) di django-ninja.

## Kelas Autentikasi Async

Ninja Extra menambahkan dukungan async untuk semua kelas dasar `Auth` yang disediakan oleh Django Ninja dalam package `ninja_extra.security`,
dan mempertahankan antarmuka yang serupa. Perlu diperhatikan bahwa saat menggunakan kelas autentikasi async ini, handler endpoint **harus** berupa fungsi async.

Sebagai contoh, mari kita tulis ulang contoh autentikasi pertama dengan kelas `AsyncHttpBearer`.

```Python
from ninja_extra import api_controller, route
from ninja_extra.security import AsyncHttpBearer
from ninja.constants import NOT_SET


class AuthBearer(AsyncHttpBearer):
    async def authenticate(self, request, token):
        # await some actions
        if token == "supersecret":
            return token


@api_controller(tags=['My Operations'], auth=NOT_SET, permissions=[])
class MyController:
    @route.get("/bearer", auth=AuthBearer())
    async def bearer(self):
        return {"token": self.context.request.auth}

```
Pada contoh di atas, kita mengubah `HttpBearer` menjadi `AsyncHttpBearer` dan mengubah bearer menjadi endpoint `async`. 
Jika `AuthBearer` akan diterapkan pada **autentikasi** `MyController`, maka semua route handler di bawah `MyController` harus berupa route handler async.


## **Autentikasi JWT**
Jika Anda ingin menggunakan autentikasi JWT. Lihat [ninja-jwt](https://pypi.org/project/django-ninja-jwt/)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
