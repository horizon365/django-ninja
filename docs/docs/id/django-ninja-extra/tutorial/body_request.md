---
comments: true
---
# **Request Body**

Request body biasanya digunakan untuk operasi "create" dan "update" (POST, PUT, PATCH).
Sebagai contoh, saat menggunakan POST atau PUT untuk membuat sebuah resource, request body biasanya berisi representasi dari resource yang akan dibuat.

Untuk membuat **request body**, Anda perlu menggunakan **Django Ninja `Schema`** atau skema Pydantic apa pun yang sesuai dengan kebutuhan Anda.

Saya merekomendasikan [Ninja-Schema](https://pypi.org/project/ninja-schema/)

## **Membuat Data Model Anda**

Kemudian Anda mendeklarasikan data model Anda sebagai kelas yang mewarisi dari `Schema`.

Gunakan tipe Python standar untuk semua atribut:

```Python
from ninja import Schema, constants
from ninja_extra import api_controller, route


class Item(Schema):
    name: str
    description: str = None
    price: float
    quantity: int

    
@api_controller(tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @route.post("/items")
    def create(self, item: Item):
        return item

```

Catatan: Jika Anda menggunakan **`None`** sebagai nilai default untuk sebuah atribut, atribut tersebut menjadi opsional di request body.
Sebagai contoh, model di atas mendeklarasikan JSON "`object`" (atau `dict` Python) seperti berikut:

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...karena `description` bersifat opsional (nilai defaultnya adalah `None`), JSON "`object`" berikut ini juga akan valid:

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
