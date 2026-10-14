---
comments: true
---
# CSRF (Cross-Site Request Forgery)

## Apa itu cross-site request forgery?
> [Cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery) terjadi ketika sebuah situs web berbahaya memuat tautan, tombol form, atau beberapa JavaScript yang dimaksudkan untuk menggunakan kredensial user yang sedang login (yang mengunjungi situs web berbahaya tersebut di browsernya) untuk melakukan suatu tindakan di situs web Anda (atau lokasi lain yang tidak tercakup dalam dokumen ini).


## Cara bertahan dari cross-site request forgery dengan Django Ninja
### Gunakan metode authentication yang tidak otomatis disematkan dalam request
Serangan cross-site request forgery mengandalkan metode authentication yang otomatis disertakan dalam request yang berasal dari situs web lain, seperti [cookies](https://en.wikipedia.org/wiki/HTTP_cookie) atau [Basic access authentication](https://en.wikipedia.org/wiki/Basic_access_authentication).
Menggunakan metode authentication yang tidak otomatis disematkan, seperti `Authorization: Bearer`, dapat mengurangi risiko serangan ini.


### Gunakan perlindungan cross-site request forgery bawaan Django
Jika Anda menggunakan authentication default Django yang menggunakan cookies, Anda juga harus menggunakan [perlindungan cross-site request forgery default Django](https://docs.djangoproject.com/en/4.2/ref/csrf/).


Secara default, **Django Ninja** memiliki perlindungan cross-site request forgery yang dinonaktifkan (**OFF**) untuk semua operasi.
Untuk mengaktifkannya, Anda perlu menggunakan argumen `csrf` pada class NinjaAPI:

```python hl_lines="3"
from ninja import NinjaAPI

api = NinjaAPI(csrf=True)
```

<span style="color: red;">Peringatan</span>: Menggunakan authentication berbasis cookie dengan cross-site request forgery yang dimatikan tidak aman! (mis. `CookieKey`, atau `django_auth`).


**Django Ninja** akan mengaktifkan cross-site request forgery secara otomatis untuk authentication berbasis cookie.


```python hl_lines="8"
from ninja import NinjaAPI
from ninja.security import APIKeyCookie

class CookieAuth(APIKeyCookie):
    def authenticate(self, request, key):
        return key == "test"

api = NinjaAPI(auth=CookieAuth())

```


Atau berbasis django-auth (yang mewarisi dari authentication berbasis cookie):

```python hl_lines="4"
from ninja import NinjaAPI
from ninja.security import django_auth

api = NinjaAPI(auth=django_auth)
```


#### Decorator Django `ensure_csrf_cookie`
Anda dapat menggunakan decorator Django [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie) pada route yang tidak terlindungi untuk membuatnya menyertakan header `Set-Cookie` bagi token cross-site request forgery. Perhatikan bahwa:
- Decorator route harus dieksekusi sebelum (yaitu berada di atas) decorator [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie).
- Anda harus menerapkan `csrf_exempt` pada route tersebut.
- Decorator `ensure_csrf_cookie` hanya bekerja pada `HttpResponse` milik Django, bukan pada dictionary seperti yang dilakukan kebanyakan decorator Django Ninja.
```python hl_lines="4"
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

@api.post("/csrf")
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request):
    return HttpResponse()
```
Sebuah request ke route ini akan memicu response dari Django dengan header `Set-Cookie` yang sesuai.


#### Kode front-end
Anda dapat menggunakan bagian [Using CSRF protection with AJAX](https://docs.djangoproject.com/en/4.2/howto/csrf/#using-csrf-protection-with-ajax) dan [Setting the token on the AJAX request](https://docs.djangoproject.com/en/4.2/howto/csrf/#setting-the-token-on-the-ajax-request) dari [How to use Django's CSRF protection](https://docs.djangoproject.com/en/4.2/howto/csrf/) untuk mempelajari cara menangani token perlindungan cross-site request forgery di kode front-end Anda.


## Tentang CORS
Anda mungkin ingin menyiapkan front-end dan API Anda di situs yang berbeda (dalam hal ini Anda dapat melihat [django-cors-headers](https://github.com/adamchainz/django-cors-headers)).
Meskipun tidak terkait langsung dengan cross-site request forgery, CORS (Cross-Origin Resource Sharing) dapat berguna ketika Anda mendefinisikan cookie cross-site request forgery di situs yang berbeda dari yang digunakan oleh front-end, karena hal ini tidak diizinkan oleh [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) secara default.
Kemudian Anda dapat melihat [README django-cors-headers](https://github.com/adamchainz/django-cors-headers#readme).

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
