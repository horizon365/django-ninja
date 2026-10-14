---
comments: true
---
# Parameter operasi

## Berkaitan dengan schema OpenAPI

Parameter-parameter berikut berinteraksi dengan cara schema OpenAPI (dan dokumentasi) dihasilkan.

### Argumen `tags`

Anda dapat menggunakan argumen `tags` (`list[str]`) untuk mengelompokkan operasi API.
```python hl_lines="6"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}


@api.post("/orders/", tags=["orders"])
def create_order(request, order: Order):
    return {"success": True}
```

Operasi yang diberi tag dapat ditangani secara berbeda oleh berbagai tools dan library. Sebagai contoh, Swagger UI menggunakan tags untuk mengelompokkan operasi yang ditampilkan.

![Summary`](../img/operation_tags.png)

#### Tags pada router

Anda dapat menggunakan argumen `tags` untuk menerapkan tags ke semua operasi yang dideklarasikan dalam sebuah router:

```python
api.add_router("/events/", events_router, tags=["events"])

# or using constructor: 

router = Router(tags=["events"])
```


### Argumen `summary`

Nama yang mudah dibaca manusia (human-readable) untuk operasi Anda.

Secara default, nama ini dibuat dengan mengkapitalisasi nama fungsi operasi Anda:

```python hl_lines="2"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}
```

![Summary`](../img/operation_summary_default.png)

Jika Anda ingin menggantinya atau menerjemahkannya ke bahasa lain, Anda dapat menggunakan argumen `summary` pada decorator `api`.

```python hl_lines="1"
@api.get("/hello/", summary="Say Hello")
def hello(request, name: str):
    return {"hello": name}
```

![`Summary`](../img/operation_summary.png)

### Argumen `description`

Untuk memberikan informasi lebih lanjut tentang operasi Anda, Anda dapat menggunakan argumen `description` atau docstring Python biasa:

```python hl_lines="1"
@api.post("/orders/", description="Creates an order and updates stock")
def create_order(request, order: Order):
    return {"success": True}
```

![`Summary`](../img/operation_description.png)

Ketika Anda perlu memberikan deskripsi yang panjang dan multi-baris, Anda dapat menggunakan `docstrings` Python untuk definisi fungsi:

```python hl_lines="4 5 6 7"
@api.post("/orders/")
def create_order(request, order: Order):
    """
    To create an order please provide:
     - **first_name**
     - **last_name**
     - and **list of Items** *(product + amount)*
    """
    return {"success": True}

```

![`Summary`](../img/operation_description_docstring.png)


### Argumen `operation_id`

`operationId` milik OpenAPI adalah string unik opsional yang digunakan untuk mengidentifikasi sebuah operasi. Jika disediakan, ID-ID ini harus unik di seluruh operasi yang dideskripsikan dalam API Anda.

Secara default, **Django Ninja** mengisinya dengan `module name` + `function name`.

Jika Anda ingin mengisinya untuk setiap operasi secara individual, Anda dapat menggunakan argumen `operation_id`:

```python hl_lines="2"
...
@api.post("/tasks", operation_id="create_task")
def new_task(request):
    ...
```

Jika Anda ingin mengganti perilaku globalnya, Anda dapat melakukan subclass pada instance NinjaAPI dan meng-override method `get_openapi_operation_id`.

Method ini akan dipanggil untuk setiap operasi yang Anda definisikan, sehingga Anda dapat mengatur logika penamaan kustom Anda dengan cara ini:
```python hl_lines="5 6 7 9"
from ninja import NinjaAPI

class MySuperApi(NinjaAPI):

    def get_openapi_operation_id(self, operation):
        # here you can access operation ( .path , .view_func, etc) 
        return ...

api = MySuperApi()

@api.get(...)
...
```

### Argumen `deprecated`

Tandai sebuah operasi sebagai deprecated tanpa menghapusnya dengan menggunakan argumen `deprecated`:

```python hl_lines="1"
@api.post("/make-order/", deprecated=True)
def some_old_method(request, order: str):
    return {"success": True}
```

Operasi tersebut akan ditandai sebagai deprecated di schema JSON maupun di dokumentasi OpenAPI interaktif:

![Deprecated](../img/deprecated.png)

### Argumen `include_in_schema`

Jika Anda perlu menyertakan/mengecualikan operasi tertentu dari schema OpenAPI, Anda dapat menggunakan argumen `include_in_schema`:

```python hl_lines="1"
@api.post("/hidden", include_in_schema=False)
def some_hidden_operation(request):
    pass
```

## Argumen `openapi_extra`
Anda dapat mengkustomisasi schema OpenAPI Anda untuk endpoint tertentu (lihat [opsi kustomisasi OpenAPI](https://swagger.io/docs/specification/about/) untuk detailnya)
```python hl_lines="1 26"
# You can set requestBody from openapi_extra
@api.get(
    "/tasks",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "required": ["email"],
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "phone": {"type": "number"},
                            "email": {"type": "string"},
                        },
                    }
                }
            },
            "required": True,
        }
    },
)
def some_operation(request):
    pass
    
# You can add additional responses to the automatically generated schema
@api.post(
    "/tasks",
    openapi_extra={
        "responses": {
            400: {
                "description": "Error Response",
            },
            404: {
                "description": "Not Found Response",
            },
        },
    },
)
def some_operation_2(request):
    pass

```


## Opsi output response

Ada beberapa argumen yang memungkinkan Anda menyesuaikan output dari response:
### `by_alias`

Apakah alias field harus digunakan sebagai keys dalam response (default adalah `False`).

### `exclude_unset`

Apakah field yang tidak di-set saat pembuatan schema dan memiliki nilai default harus dikecualikan dari response (default adalah `False`).
### `exclude_defaults`

Apakah field yang nilainya sama dengan nilai default-nya (terlepas dari apakah field tersebut di-set) harus dikecualikan dari response (default adalah `False`).
### `exclude_none`

Apakah field yang nilainya sama dengan `None` harus dikecualikan dari response (default adalah `False`).

## url_name
Memungkinkan Anda mengatur nama URL endpoint API (menggunakan [URL name reversing milik Django](https://docs.djangoproject.com/en/stable/topics/http/urls/#reversing-namespaced-urls))
```python hl_lines="1 7"
@api.post("/tasks", url_name='tasks')
def some_operation(request):
    pass

# then you can get the url with

reverse('api-1.0.0:tasks')
```

Untuk detail lebih lanjut, lihat panduan [Reversing URLs](../guides/urls.md).


## Menentukan servers
Jika Anda ingin menentukan satu atau beberapa servers untuk spesifikasi OpenAPI, Anda dapat menggunakan `servers` saat menginisialisasi instance NinjaAPI:
```python hl_lines="4 5 6 7"
from ninja import NinjaAPI

api = NinjaAPI(
        servers=[
            {"url": "https://stag.example.com", "description": "Staging env"},
            {"url": "https://prod.example.com", "description": "Production env"},
        ]
)
```
Ini memungkinkan pergantian antar environment saat menggunakan dokumentasi OpenAPI interaktif:
![Servers](../img/servers.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
