
Ninja JWT dilengkapi dengan sebuah application yang menyediakan fungsionalitas blacklist token.
Untuk menggunakan application ini, sertakan application tersebut dalam daftar aplikasi yang terinstal di `settings.py`:

```python
# Django project settings.py

...

INSTALLED_APPS = (
    ...
    'ninja_jwt.token_blacklist',
    ...
)
```

Selain itu, pastikan untuk menjalankan `python manage.py migrate` untuk menjalankan migrasi application tersebut.

Jika application blacklist terdeteksi di `INSTALLED_APPS`, Ninja JWT akan menambahkan setiap refresh token atau sliding token yang dihasilkan ke daftar outstanding token.
Ninja JWT juga akan memeriksa, sebelum menganggap suatu refresh token atau sliding token valid, bahwa token tersebut tidak muncul di blacklist token.

Application blacklist Ninja JWT menggunakan dua model, yaitu `OutstandingToken` dan `BlacklistedToken`, untuk mengimplementasikan daftar outstanding token dan blacklist token-nya.
Model admin didefinisikan untuk kedua model tersebut. Untuk menambahkan token ke blacklist, cari record `OutstandingToken` yang sesuai di admin,
lalu gunakan admin sekali lagi untuk membuat record `BlacklistedToken` yang menunjuk ke record `OutstandingToken` tersebut.

Sebagai alternatif, Anda dapat mem-blacklist sebuah token dengan membuat instance dari subclass `BlacklistMixin` dan memanggil method `blacklist` pada instance tersebut:

```python
from ninja_jwt.tokens import RefreshToken

token = RefreshToken(base64_encoded_token_string)
token.blacklist()
```

Ini akan membuat outstanding token dan record blacklist yang unik untuk claim `jti` milik token tersebut, atau untuk claim apa pun yang ditentukan oleh setting `JTI_CLAIM`.

Application blacklist juga menyediakan management command `flushexpiredtokens`, yang akan menghapus semua token yang telah kedaluwarsa dari outstanding list maupun blacklist.
Anda sebaiknya menyiapkan cron job di server atau platform hosting Anda yang menjalankan command ini setiap hari.

!!! success

    Lanjutkan ke bab berikutnya **[Development dan Contributing](development_and_contributing.md)**.


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
