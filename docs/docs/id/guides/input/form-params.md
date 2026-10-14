---
comments: true
---
# Form Data

**Django Ninja** juga memungkinkan Anda mem-parsing dan memvalidasi data `request.POST`
(yaitu `application/x-www-form-urlencoded` atau `multipart/form-data`).

## Form Data sebagai Parameter

```python hl_lines="1 4"
from ninja import NinjaAPI, Form

@api.post("/login")
def login(request, username: Form[str], password: Form[str]):
    return {'username': username, 'password': '*****'}
```

Perhatikan hal-hal berikut:

1) Anda perlu mengimpor class `Form` dari `ninja`
```python
from ninja import Form
```

2) Gunakan `Form` sebagai nilai default untuk parameter:
```python
username: Form[str]
```

## Menggunakan Schema

Mirip dengan [Request Body](body.md#declare-it-as-a-parameter), Anda dapat menggunakan schema untuk mengorganisasi parameter Anda.

```python hl_lines="12"
{!./src/tutorial/form/code01.py!}
```

## Request Form + Path + Query Parameters

Mirip dengan [Request Body](body.md#request-body-path-query-parameters), Anda dapat mengombinasikan form data dengan sumber parameter lainnya.

Anda dapat mendeklarasikan query parameters **dan** path parameters **dan** form fields, **dll.** sekaligus.

**Django Ninja** akan mengenali bahwa function parameters yang cocok dengan path parameters harus **diambil dari path**,
sedangkan function parameters yang dideklarasikan dengan `Form(...)` harus **diambil dari form fields pada request**, dan seterusnya.

```python hl_lines="12"
{!./src/tutorial/form/code02.py!}
```
## Memetakan Form Field Kosong ke Nilai Default

Form field opsional sering dikirim dengan nilai kosong. Nilai ini ditafsirkan sebagai string kosong, sehingga untuk field seperti `int` atau `bool`, validasi bisa gagal.

Seperti dijelaskan dalam dokumentasi Pydantic, ini dapat diselesaikan dengan menggunakan [generic classes sebagai tipe](https://pydantic.com.cn/usage/types/#generic-classes-as-types).

```python hl_lines="15 16 23-25"
{!./src/tutorial/form/code03.py!}
```

!!! done

    Lanjutkan ke bab berikutnya! **[Upload File](file-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
