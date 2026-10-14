---
comments: true
---
## Pendahuluan
Saya sudah lama mendengar tentang JWT tetapi belum pernah benar-benar menggunakannya. Baru-baru ini, saat meneliti protokol resumable upload tus, saya sampai ke level hooks-http, dengan tujuan melakukan autentikasi saat upload file. Wajar jika saya teringat package `django-ninja-jwt`. Saya mengira ini harusnya sederhana, tetapi setelah membaca [dokumentasinya](https://django-ninja.cn/django-ninja-jwt/), saya menyadari bahwa ini bukan hanya sederhana — ini sangat polos sampai mengejutkan.

## Memulai

Sesuai panduan, Anda hanya perlu menginstall `dango-ninja-jwt` dan `django-ninja-extra`, lalu mengganti `NinjaAPI` dengan `njaExtraAPI`, dan cukup satu baris saja.

```python
api.register_controllers(NinjaJWTDefaultController)
```

Jujur saja, ini membingungkan.

Tunggu — mari kita lihat docs-nya dulu. Tiga endpoint baru muncul: `pair`, `refresh`, dan `verify`.
![JWT swagger UI token](../img/jwt-token.png)
Perhatikan ikon gembok di pojok kanan atas — ini akan berguna nanti. Ikon ini hanya muncul ketika Anda menggunakan fungsi `JWTAuth`.

### pair
Yang pertama adalah endpoint `pair`. Artinya, setelah Anda memberikan username dan password, endpoint ini mengembalikan authentication token dan refresh token.
Format request body-nya adalah sebagai berikut:
```json
{
  "password": "string",
  "username": "string"
}
```
Perhatian: Di sini `username` muncul di bawah, yang sedikit berbeda dari yang mungkin Anda asumsikan.
Setelah mengklik Execute, Anda akan mendapatkan hasil seperti ini:
```json
{
  "data": {
    "username": "lyq",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzE0NzU2NCwiaWF0IjoxNzQyNTQyNzY0LCJqdGkiOiI4MTZmMzg2YWYwNmY0NmVhOWY1YzlkMDJjYzQxZjFkOCIsInVzZXJfaWQiOjF9.G-mTefGtP-cTXWVrxAsqXGGKnZ1442jw67ilvTY5gcQ",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNjI5MTY0LCJpYXQiOjE3NDI1NDI3NjQsImp0aSI6IjdiMGY1Y2Y5NTVlZDRiMzQ5M2M3MmY4NzJmNDdkMzUxIiwidXNlcl9pZCI6MX0.JO9PxVA-rX6TPo9Db00eOuOorThjgX3nTjBT-CuOh90"
  }
}
```
### refresh
Token `access` di atas dapat digunakan untuk autentikasi, tetapi masa berlakunya terbatas secara default. Token `refresh` memiliki masa berlaku yang lebih lama daripada `access`, dan digunakan untuk mendapatkan token `access` baru setelah token sebelumnya kedaluwarsa.
Setelah di-refresh, token `access` sebelumnya menjadi tidak valid.

Pada titik ini, Anda dapat meng-copy token `access` ke ikon gembok di pojok kanan atas. Dengan begitu, setiap endpoint di halaman saat ini dapat menggunakannya, yang sangat memudahkan debugging.
### verify
Anda dapat menuju endpoint ketiga, `verify`, untuk memeriksa apakah token `access` masih valid.

Jadi secara keseluruhan, `django-ninja-jwt` sederhananya membangun tiga endpoint untuk Anda, sehingga memudahkan untuk mendapatkan, me-refresh, dan menguji token.

## Kustomisasi
Ketiga endpoint ini saja tidak cukup — setidaknya, kita perlu menambahkan autentikasi ke endpoint spesifik milik kita sendiri.
Yang Anda butuhkan di sini adalah `JWTAuth`; hanya setelah menggunakannya ikon gembok akan muncul.
```python
from ninja_jwt.authentication import JWTAuth
@route.get('/some', auth=JWTAuth())
def some_endpoint(request):
    """Convenient for showing the auth button on the docs page"""
    return request.auth.username
```
Dan pada endpoint `some`, juga ada ikon gembok tersendiri.
![JWT swagger UI token custom](../img/jwt-token-custom.png)
Untuk endpoint `some` di atas, jika autentikasi berhasil, ia merespons dengan username dari user yang sedang login. Jika gagal, ia mengembalikan response 401.
Backend developer perlu memberi tahu tim frontend untuk mengirimkan nilai ini — minta mereka menuju ke bagian [pair](#pair) untuk mendapatkannya, dan secara berkala menuju ke [refresh](#refresh) untuk me-refresh-nya.

### Konfigurasi Masa Berlaku Token

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Access token lifetime
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh token lifetime
    'AUTH_HEADER_TYPES': ('Bearer',),
}

```
### Kustomisasi Lanjutan
Jika menggunakan `@route.get('/some', auth=JWTAuth())` di route ninja Anda belum memenuhi kebutuhan, Anda dapat memanggil `authenticate` di dalam fungsi.

```python
@route.get('/some')
def some_endpoint(request):
    auth = JWTAuth()
    # If it fails, a 401 is raised internally
    if auth.authenticate(request, token):
        return request.auth.username

```
`token` di atas perlu Anda ekstrak sendiri dari objek `request`.
