
Ninja JWT menyediakan dua jenis token yang berbeda yang dapat digunakan untuk membuktikan autentikasi.
Dalam payload sebuah token, jenisnya dapat diidentifikasi dari nilai claim jenis token, yang secara default adalah `token_type`.
Namun, nilainya dapat berupa `access`, `sliding`, atau `refresh`,
tetapi saat ini refresh token belum dianggap sebagai token autentikasi yang valid. Nama claim yang digunakan untuk menyimpan jenis token dapat dikustomisasi dengan mengubah pengaturan `TOKEN_TYPE_CLAIM`.

Secara default, Ninja JWT mengharapkan token `access` untuk membuktikan autentikasi.
Jenis token autentikasi yang diizinkan ditentukan oleh nilai pengaturan `AUTH_TOKEN_CLASSES`.
Pengaturan ini berisi daftar dotted path yang menunjuk ke kelas-kelas token. Nilai defaultnya adalah dotted path `'ninja_jwt.tokens.AccessToken'`,
tetapi juga dapat mencakup dotted path `'ninja_jwt.tokens.SlidingToken'`.
Salah satu atau kedua dotted path tersebut dapat muncul dalam daftar kelas token autentikasi.
Jika keduanya ada, maka kedua jenis token dapat digunakan untuk membuktikan autentikasi.

Sliding Tokens
==============

Sliding tokens memberikan pengalaman yang lebih nyaman bagi pengguna token, tetapi mengorbankan tingkat keamanan yang lebih rendah dan, saat blacklist app digunakan, kinerja yang lebih rendah.
Sliding token adalah token yang berisi claim kedaluwarsa (expiration) sekaligus claim kedaluwarsa refresh (refresh expiration). Selama timestamp pada claim kedaluwarsa sliding token belum terlewati,
token tersebut dapat digunakan untuk membuktikan autentikasi. Selain itu, selama timestamp pada claim kedaluwarsa refresh belum terlewati,
token juga dapat dikirimkan ke refresh view untuk mendapatkan salinannya dengan claim kedaluwarsa yang telah diperbarui.

Jika Anda ingin menggunakan sliding tokens, ubah pengaturan `AUTH_TOKEN_CLASSES` menjadi `('ninja_jwt.tokens.SlidingToken',)`.
(Sebagai alternatif, jika Anda ingin mengizinkan kedua jenis token untuk autentikasi, pengaturan `AUTH_TOKEN_CLASSES` dapat memuat dotted path yang menunjuk ke kelas token `AccessToken` dan `SlidingToken`
di modul `ninja_jwt.tokens`)

Selain itu, daftarkan `NinjaJWTSlidingController` ke `api`:
```python
from ninja_jwt.controller import NinjaJWTSlidingController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTSlidingController)

```

Perhatikan bahwa jika Anda menggunakan blacklist app, Ninja JWT akan memvalidasi semua sliding tokens terhadap blacklist untuk setiap request yang terautentikasi.
Hal ini akan menurunkan kinerja API views yang terautentikasi.

!!! success

    Lanjutkan ke bab berikutnya **[Blacklist App](blacklist_app.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
