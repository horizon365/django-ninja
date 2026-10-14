---
comments: true
---
# Tweaking the Response

Terkadang Anda ingin mengubah sebuah response tepat sebelum dikirimkan, misalnya untuk menambahkan header atau memodifikasi cookie.

Untuk melakukannya, cukup deklarasikan argumen fungsi bertipe `HttpResponse`:

```python
from django.http import HttpRequest, HttpResponse

@api.get("/cookie/")
def feed_cookiemonster(request: HttpRequest, response: HttpResponse):
    # Set a cookie.
    response.set_cookie("cookie", "delicious")
    # Set a header.
    response["X-Cookiemonster"] = "blue"
    return {"cookiemonster_happy": True}
```


## Temporal Response Object

Objek response ini digunakan sebagai dasar untuk semua response yang dibangun oleh Django Ninja, termasuk error responses.
Jika sebuah objek `HttpResponse` Django dikembalikan langsung oleh sebuah operation, maka objek ini *tidak* digunakan.

Jelas objek response ini belum akan berisi content, tetapi ia sudah menyetel `content_type` (meskipun mungkin Anda tidak ingin mengubahnya).

`status_code` akan di-override berdasarkan nilai yang dikembalikan (defaultnya 200, atau status code jika yang dikembalikan adalah tuple dua elemen).


## Mengubah Base Response Object

Anda dapat mengubah objek temporal response ini dengan meng-override method `NinjaAPI.create_temporal_response`.

```python
    def create_temporal_response(self, request: HttpRequest) -> HttpResponse:
        response = super().create_temporal_response(request)
        # Do your magic here...
        return response
```

!!! done

    Lanjutkan ke bab berikutnya! **[Menghasilkan Schema dari Django Models](django-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
