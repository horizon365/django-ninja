
Ninja JWT menggunakan `HttpBearer` milik Django Ninja sebagai cara untuk mengautentikasi user yang mengakses endpoint API Anda.
User yang terautentikasi dapat ditemukan di `request.user` atau `request.auth`.

### Autentikasi Route - Berbasis Kelas

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=JWTAuth())
    def some_endpoint(self):
        ...
```

### Autentikasi Route - Berbasis Fungsi

```python
from ninja import router
from ninja_jwt.authentication import JWTAuth

router = router('')

@router.get('/some-endpoint', auth=JWTAuth())
def some_endpoint(request):
    ...
```

Implementasi Autentikasi Kustom
-------
Jika Anda ingin menggunakan implementasi `JWTAuth` yang berbeda, Anda perlu membuat subclass dari `JWTBaseAuthentication`.
Jika Anda ingin menggunakan sesuatu selain `bearer`, baca selengkapnya tentang [Django Ninja - Authentication](https://django-ninja.rest-framework.com/tutorial/authentication/).

Contoh:
```python
from ninja.security import APIKeyHeader
from ninja_jwt.authentication import JWTBaseAuthentication
from ninja import router

class ApiKey(APIKeyHeader, JWTBaseAuthentication):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        return self.jwt_authenticate(request, token=key)


header_key = ApiKey()
router = router('')

@router.get("/headerkey", auth=header_key)
def apikey(request):
    return f"Token = {request.auth}"

```

### Autentikasi Route Asynchronous
Jika Anda tertarik dengan autentikasi route asynchronous, tersedia kelas `AsyncJWTAuth`

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import AsyncJWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=AsyncJWTAuth())
    async def some_endpoint(self):
        ...
```
Catatan: `some_endpoint` harus asynchronous. Setiap fungsi endpoint yang ditandai dengan `AsyncJWTAuth` harus asynchronous.

!!! warning
    Fungsionalitas asynchronous hanya tersedia untuk versi Django > 3.0.

!!! success

    Lanjutkan ke bab berikutnya **[Pengaturan](settings.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
