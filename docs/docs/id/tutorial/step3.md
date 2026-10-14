---
comments: true
---
# Tutorial - Menangani response

## Mendefinisikan schema response

**Django Ninja** memungkinkan Anda mendefinisikan schema response untuk keperluan validasi dan dokumentasi.

Kita akan membuat operasi ketiga yang mengembalikan informasi tentang user Django saat ini.

```python
from ninja import Schema

class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # Unauthenticated users do not have the following fields, so provide default values.
    email: str = None
    first_name: str = None
    last_name: str = None

@api.get("/me", response=UserSchema)
def me(request):
    return request.user
```

Ini akan mengonversi objek `User` milik Django menjadi dictionary yang hanya berisi field-field yang didefinisikan.

### Beberapa tipe response

Mari kita kembalikan response yang berbeda jika user saat ini tidak terautentikasi.

```python hl_lines="2-5 7-8 10 12-13"
class UserSchema(Schema):
    username: str
    email: str
    first_name: str
    last_name: str

class Error(Schema):
    message: str

@api.get("/me", response={200: UserSchema, 403: Error})
def me(request):
    if not request.user.is_authenticated:
        return 403, {"message": "Please sign in first"}
    return request.user 
```

Seperti yang Anda lihat, Anda dapat mengembalikan tuple dua bagian yang akan ditafsirkan sebagai kode response HTTP dan datanya.

!!! success

    Ini adalah akhir dari tutorial! Lihat **[tutorial lainnya](other/crud.md)** atau **[Panduan how-to](../guides/input/operations.md)** untuk informasi lebih lanjut.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
