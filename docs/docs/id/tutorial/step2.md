---
comments: true
---
# Tutorial - Menangani parameter input

## Meneruskan parameter dari query string

Mari kita ubah operasinya agar menerima sebuah name dari query string URL. Untuk melakukannya, cukup tambahkan argumen `name` ke fungsi kita.

```python
@api.get("/hello")
def hello(request, name):
    return f"Hello {name}"
```

Ketika kita menyediakan argumen bernama tersebut, kita mendapatkan response yang diharapkan (HTTP 200).

<a href="http://localhost:8000/api/hello?name=you"
target="_blank">localhost:8000/api/hello?name=you</a>:

```json
"Hello you"
```

### Nilai default

Jika Anda tidak menyediakan parameter tersebut, sebuah response error HTTP 422 akan dikembalikan.

*[HTTP 422]: Unprocessable Entity

<a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a>:

```json
{
  "detail": [
    {
      "loc": ["query", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

Kita dapat menentukan nilai default untuk argumen `name` jika parameter tersebut tidak disediakan:

```python hl_lines="2"
@api.get("/hello")
def hello(request, name="world"):
    return f"Hello {name}"
```

## Tipe input

**Django Ninja** menggunakan [Python type hints](https://docs.python.org/3/library/typing.html) standar untuk memformat tipe input. Jika tidak ada tipe yang disediakan, string diasumsikan (tetapi menyediakan type hints untuk semua argumen adalah praktik terbaik).

Mari kita tambahkan operasi kedua yang melakukan operasi matematika dasar dengan bilangan bulat.

```python hl_lines="5-7"
@api.get("/hello")
def hello(request, name: str = "world"):
    return f"Hello {name}"

@api.get("/math")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

<a href="http://localhost:8000/api/math?a=2&b=3"
target="_blank">localhost:8000/api/math?a=2&b=3</a>:

```json
{
  "add": 5,
  "multiply": 6
}
```

## Meneruskan parameter melalui path string

Anda dapat mendeklarasikan "parameter" path menggunakan sintaks yang sama dengan Python format strings.

Parameter apa pun yang ditemukan di path string akan diteruskan ke fungsi Anda sebagai argumen, alih-alih diambil dari query string.

```python hl_lines="1"
@api.get("/math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

Sekarang kita mengakses operasi math melalui <a href="http://localhost:8000/api/math/2and3"
target="_blank">localhost:8000/api/math/2and3</a>.


## Meneruskan parameter melalui request body

Kita akan mengubah operasi `hello` untuk menggunakan HTTP `POST` request, dan mengambil parameter dari request body.

Untuk menentukan bahwa parameter berasal dari request body, kita perlu mendeklarasikan sebuah schema.

*[Schema]: Perluasan dari "Model" milik Pydantic

```python hl_lines="1 5-6 8-10"
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class HelloSchema(Schema):
    name: str = "world"

@api.post("/hello")
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"
```

### API yang mendokumentasikan dirinya sendiri

Sekarang mengakses <a href="http://localhost:8000/api/hello" target="_blank">localhost:8000/api/hello</a> akan menghasilkan response error HTTP 405, karena kita perlu mengubah request yang dikirim ke URL ini menjadi tipe POST.

*[HTTP 405]: Method Not Allowed

Cara mudah untuk melakukannya adalah dengan menggunakan dokumentasi Swagger yang secara otomatis dibuatkan untuk kita, pada URL "/docs" default (ditambahkan ke root URL API kita).

1. Kunjungi <a href="http://localhost:8000/api/docs" target="_blank">localhost:8000/api/docs</a> untuk melihat operasi yang telah kita buat
1. Buka operasi `/api/hello`
2. Klik "Try it out"
3. Ubah request body
4. Klik "Execute"

!!! success

    Lanjutkan ke bab berikutnya **[Menangani response](step3.md)**
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
