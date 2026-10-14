---
comments: true
---
# HTTP Methods

## Mendefinisikan Operations

Sebuah `operation` dapat berupa salah satu dari [HTTP methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods):

- GET (mengambil)
- POST (mengirim)
- PUT (memperbarui)
- DELETE (menghapus)
- PATCH (pembaruan sebagian)

**Django Ninja** memiliki satu decorator untuk setiap operation:

```python hl_lines="1 5 9 13 17"
@api.get("/path")
def get_operation(request):
    ...

@api.post("/path")
def post_operation(request):
    ...

@api.put("/path")
def put_operation(request):
    ...

@api.delete("/path")
def delete_operation(request):
    ...

@api.patch("/path")
def patch_operation(request):
    ...
```

Untuk informasi tentang apa saja yang dapat diteruskan ke salah satu decorator ini, lihat dokumentasi referensi [Operation Parameters](../../reference/operations-parameters.md).

## Menangani Beberapa Method Sekaligus

Jika Anda perlu menangani beberapa method untuk sebuah path tertentu dengan satu fungsi, Anda dapat menggunakan decorator `api_operation`:

```python hl_lines="1"
@api.api_operation(["POST", "PATCH"], "/path")
def mixed_operation(request):
    ...
```

Fitur ini juga dapat digunakan untuk mengimplementasikan HTTP methods lain yang tidak memiliki method khusus di **Django Ninja**, seperti `HEAD` atau `OPTIONS`.

```python hl_lines="1"
@api.api_operation(["HEAD", "OPTIONS"], "/path")
def mixed_operation(request):
    ...
```

!!! done

    Lanjutkan ke bab berikutnya! **[Path Parameters](path-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
