---
comments: true
---
# Meng-override Konfigurasi Pydantic

Untuk sebuah **`Schema` Django Ninja**, terdapat banyak pengaturan kustomisasi yang tersedia melalui [class `Config` Pydantic](https://pydantic.com.cn/usage/model_config/) milik schema tersebut. 

!!! note
    Di balik layar, **Django Ninja** menggunakan [Pydantic Models](https://pydantic.com.cn/usage/models/)
    beserta seluruh fitur dan keunggulannya. Alias `Schema` dipilih untuk menghindari kebingungan saat bekerja dengan Django models dalam kode,
    karena class model milik Pydantic secara default bernama "Model", yang bentrok dengan class "Model" milik Django.

## Contoh CamelCase Schema

Salah satu atribut `Config` yang menarik adalah [`alias_generator`](https://pydantic.com.cn/usage/model_config/#alias-generator).
Contoh penggunaan Pydantic di **Django Ninja** mungkin terlihat seperti ini:

```python hl_lines="12 13"
from ninja import Schema


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))


class CamelModelSchema(Schema):
    str_field_name: str
    float_field_name: float

    class Config(Schema.Config):
        alias_generator = to_camel
```

!!! note
    Saat meng-override `Config` milik schema, Anda perlu mewarisi dari class `Config` dasarnya.

Perlu diingat bahwa ketika Anda ingin mengubah output nama field (misalnya menjadi camelCase) — Anda juga perlu menyetel `populate_by_name` dan `by_alias`

```python hl_lines="6 9"
class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ["id", "email"]
        alias_generator = to_camel
        populate_by_name = True  # !!!!!! <--------


@api.get("/users", response=list[UserSchema], by_alias=True) # !!!!!! <-------- by_alias
def get_users(request):
    return User.objects.all()

```

Hasilnya:

```JSON
[
  {
    "Id": 1,
    "Email": "tim@apple.com"
  },
  {
    "Id": 2,
    "Email": "sarah@smith.com"
  }
  ...
]

```

## Konfigurasi Kustom dari Django Models

Saat menggunakan [`create_schema`](django-pydantic-create-schema.md#create_schema), schema yang dihasilkan
dapat digunakan untuk membangun class lain dengan konfigurasi kustom, misalnya:

```python hl_lines="10"
from django.contrib.auth.models import User
from ninja.orm import create_schema


BaseUserSchema = create_schema(User)


class UserSchema(BaseUserSchema):

    class Config(BaseUserSchema.Config):
        ...
```

!!! done

    Lanjutkan ke bab berikutnya! **[Pagination](pagination.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
