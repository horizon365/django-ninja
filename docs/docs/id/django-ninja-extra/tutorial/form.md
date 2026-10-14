---
comments: true
---
Jika Anda belum tahu cara menangani request POST dengan content type seperti `application/x-www-form-urlencoded` atau `multipart/form-data` di django-ninja-extra, maka panduan ini akan berguna bagi Anda.
Django-Ninja sudah membahas sebagian besar use case [di sini](https://django-ninja.cn/tutorial/form-params/), tetapi saya akan memberikan ringkasan singkat di sini.

### Form Data sebagai Parameter

```python hl_lines="7 8"
from ninja import Form, constants
from ninja_extra import api_controller, http_post


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @http_post("/login")
    def login(self, username: str = Form(...), password: str = Form(...)):
        return {'username': username, 'password': '*****'}
```
Ada dua hal yang perlu diperhatikan di sini:

- Anda perlu mengimpor `Form` dari module `ninja`
- Gunakan `Form` sebagai nilai default untuk parameter Anda


!!! info
    Untuk informasi lebih lanjut tentang hal ini, kunjungi [Tutorial Form Django-Ninja](https://django-ninja.cn/guides/input/form-params/)
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
