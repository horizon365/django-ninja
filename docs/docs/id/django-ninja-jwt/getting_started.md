
#### Prasyarat
- Python >= 3.6
- Django >= 2.1
- Django-Ninja >= 0.16.1
- Django-Ninja-Extra >= 0.11.0

Berikut adalah versi Python dan package yang didukung secara resmi. Versi lain juga mungkin dapat berfungsi. Anda bebas memodifikasi konfigurasi tox dan melihat apa yang mungkin.

## Instalasi

Ninja JWT dapat diinstal via pip:

    pip install django-ninja-jwt

Selain itu, Anda perlu mendaftarkan controller `NinjaJWTDefaultController` ke API Django-Ninja Anda.

```python
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

```
`NinjaJWTDefaultController` dilengkapi dengan tiga route, yaitu `obtain_token`, `refresh_token`, dan `verify_token`.
Controller ini merupakan kombinasi dari dua subclass, yaitu `TokenVerificationController` dan `TokenObtainPairController`.
Jika Anda ingin mengustomisasi route-route tersebut, Anda dapat mewarisi controller-controller ini dan mengubah implementasinya.

```python
from ninja_extra import api_controller
from ninja_jwt.controller import TokenObtainPairController

@api_controller('token', tags=['Auth'])
class MyCustomController(TokenObtainPairController):
    """Only obtain token and refresh token"""
...
api.register_controllers(MyCustomController)
```

Jika Anda ingin menggunakan localization/translation, cukup tambahkan `ninja_jwt` ke `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    ...
    'ninja_jwt',
    ...
]
```

## Penggunaan

Untuk memastikan bahwa Ninja JWT berfungsi, Anda dapat membuat beberapa request uji dengan curl:

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "davidattenborough", "password": "boatymcboatface"}' \
  http://localhost:8000/api/token/pair

...
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}
```

Anda dapat menggunakan access token yang dikembalikan untuk membuktikan autentikasi pada views yang terlindungi:

``` {.sourceCode .bash}
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
  http://localhost:8000/api/some-protected-view/
```

Ketika access token yang berumur pendek ini kedaluwarsa, Anda dapat menggunakan refresh token yang berumur lebih panjang untuk memperoleh access token lain:

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"}' \
  http://localhost:8000/api/token/refresh/

...
{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXN...", "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVm..."}
```

Dependensi Kriptografi (Opsional)
-------------------------------------

Jika Anda berencana meng-encode atau men-decode token menggunakan algoritma tanda tangan digital tertentu (yaitu, RSA dan ECDSA; lihat PyJWT untuk algoritma lainnya),
Anda perlu menginstal library cryptography_. Library ini dapat diinstal secara eksplisit, atau sebagai item yang dibutuhkan dari requirements `django-ninja-jwt`:

    pip install django-ninja-jwt[crypto]

Saat menggunakan file requirements dari proyek `Ninja JWT`, format `django-ninja-jwt[crypto]` direkomendasikan,
karena baris requirement `cryptography` yang terpisah dapat di kemudian hari disalahartikan sebagai requirement yang tidak terpakai dan dihapus.
[cryptography](https://cryptography.io)

!!! success

    Lanjutkan ke bab berikutnya **[Autentikasi Route](auth_integration.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
