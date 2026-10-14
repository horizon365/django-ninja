---
comments: true
---
# Path Parameters

Anda dapat mendeklarasikan "parameters" path menggunakan sintaks yang sama dengan Python formatted strings (yang, untungnya, juga cocok dengan <a href="https://swagger.io/docs/specification/describing-parameters/#path-parameters" target="_blank">path parameters OpenAPI</a>):

```python hl_lines="1 2"
{!./src/tutorial/path/code01.py!}
```

Nilai dari path parameter `item_id` akan diteruskan ke fungsi Anda sebagai argumen `item_id`.

Jadi, jika Anda menjalankan contoh ini dan membuka <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a>, Anda akan melihat response berikut:

```JSON
{"item_id":"foo"}
```


### Path Parameters dengan Tipe

Anda dapat mendeklarasikan tipe dari sebuah path parameter menggunakan anotasi tipe Python standar di fungsi Anda:

```python hl_lines="2"
{!./src/tutorial/path/code02.py!}
```

Dalam kasus ini, `item_id` dideklarasikan sebagai **`int`**. Ini memberi Anda dukungan editor dan linter untuk pemeriksaan error, code completion, dll.

Jika Anda menjalankan kode ini di browser melalui <a href="http://localhost:8000/api/items/3" target="_blank">http://localhost:8000/api/items/3</a>, Anda akan melihat response berikut:
```JSON
{"item_id":3}
```

!!! tip
    Perhatikan bahwa nilai yang diterima (dan dikembalikan) fungsi Anda adalah **3**, sebagai `int` Python — bukan string `"3"`.
    Jadi, hanya dengan deklarasi tipe tersebut, **Django Ninja** memberi Anda "parsing" dan validasi request secara otomatis.



### Validasi Data

Di sisi lain, jika Anda mengunjungi <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a> <small>*(`"foo"` bukanlah int)*</small> di browser Anda, Anda akan melihat HTTP error seperti ini:

```JSON hl_lines="8"
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```


### Django Path Converters

Anda dapat menggunakan [Django path converters](https://docs.djangoproject.com/en/stable/topics/http/urls/#path-converters)
untuk membantu mem-parsing path:

```python hl_lines="1"
@api.get("/items/{int:item_id}")
def read_item(request, item_id):
    return {"item_id": item_id}
```

Dalam kasus ini, `item_id` akan di-parsing sebagai **`int`**. Jika `item_id` bukan `int` yang valid, URL tersebut tidak akan cocok.
(Misalnya, jika tidak ada route lain yang cocok, akan dikembalikan 404 Not Found.)

!!! tip
    Perhatikan bahwa karena **Django Ninja** menggunakan tipe `str` default untuk parameter yang tidak dianotasi, nilai yang diterima (dan dikembalikan) fungsi di atas adalah `"3"`,
    sebagai `str` Python — bukan integer **3**. Untuk menerima `int`, cukup deklarasikan `item_id` dengan anotasi tipe `int` pada definisi fungsi seperti biasa:

    ```python hl_lines="2"
    @api.get("/items/{int:item_id}")
    def read_item(request, item_id:int):
        return {"item_id": item_id}
    ```
 
#### Path Parameters dengan Slash

Converter `path` milik Django memungkinkan Anda menangani parameter yang menyerupai path:

```python hl_lines="1"
@api.get('/dir/{path:value}')
def someview(request, value: str):
    return value
```
Anda dapat mem-query operation ini dengan `/dir/some/path/with-slashes`, dan `value` Anda akan bernilai `some/path/with-slashes`

### Beberapa Parameter Sekaligus

Anda dapat meneruskan sebanyak mungkin variabel ke `path` — cukup ingat untuk menggunakan nama yang unik, dan jangan lupa menggunakan nama yang sama pada argumen fungsi Anda.

```python
@api.get("/events/{year}/{month}/{day}")
def events(request, year: int, month: int, day: int):
    return {"date": [year, month, day]}
```


### Menggunakan Schema

Anda juga dapat menggunakan schema untuk mengenkapsulasi path parameters yang saling bergantung (dan memvalidasinya sebagai satu grup):


```python hl_lines="1 2  5 6 7 8 9 10 11 15"
{!./src/tutorial/path/code010.py!}
```

!!! note
    Perhatikan bahwa di sini kita menggunakan source hint `Path` agar **Django Ninja** mengetahui bahwa schema ini akan diterapkan pada path parameters.

### Dokumentasi

Sekarang, ketika Anda membuka <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a> di browser, Anda akan melihat dokumentasi API otomatis yang interaktif.
![Django Ninja Swagger](../../img/tutorial-path-swagger.png)

!!! done

    Lanjutkan ke bab berikutnya! **[Query Parameters](query-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
