Jika Anda ingin mengustomisasi claim yang disertakan dalam web token yang dihasilkan oleh views `NinjaJWTDefaultController` dan `NinjaJWTSlidingController`,
buat subclass untuk controller yang diinginkan beserta serializer-nya. Berikut adalah contohnya:

!!! info
Jika Anda tertarik dengan versi asynchronous dari kelas tersebut, gunakan `AsyncNinjaJWTDefaultController` dan `AsyncNinjaJWTSlidingController`.
Perlu diperhatikan juga bahwa ini hanya berfungsi pada versi Django yang mendukung operasi asynchronous.

```python
from ninja_jwt.schema import TokenObtainPairInputSchema
from ninja_jwt.controller import TokenObtainPairController
from ninja_extra import api_controller, route
from ninja import Schema


class UserSchema(Schema):
    first_name: str
    email: str


class MyTokenObtainPairOutSchema(Schema):
    refresh: str
    access: str
    user: UserSchema


class MyTokenObtainPairSchema(TokenObtainPairInputSchema):
    def output_schema(self):
        out_dict = self.get_response_schema_init_kwargs()
        out_dict.update(user=UserSchema.from_orm(self._user))
        return MyTokenObtainPairOutSchema(**out_dict)


@api_controller('/token', tags=['Auth'])
class MyTokenObtainPairController(TokenObtainPairController):
    @route.post(
        "/pair", response=MyTokenObtainPairOutSchema, url_name="token_obtain_pair"
    )
    def obtain_token(self, user_token: MyTokenObtainPairSchema):
        return user_token.output_schema()

```

Sama seperti controller standar, Anda juga perlu mendaftarkan controller tersebut seperti yang ditunjukkan di [Memulai](getting_started.md)

#### Menggunakan Django Ninja Router

Jika Anda tertarik menggunakan fungsi alih-alih kelas, hal itu juga dimungkinkan. Berikut adalah contohnya

```python
from ninja_jwt.routers.blacklist import blacklist_router
from ninja_jwt.routers.obtain import obtain_pair_router, sliding_router
from ninja_jwt.routers.verify import verify_router
```

Daftarkan `router` ke `api` milik django-ninja seperti ini:

```python
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router('/token', tags=['Auth'], router=obtain_pair_router)
...
```

Jika Anda tertarik mengustomisasi token claim, Anda dapat melakukannya dengan membuat subclass dari `TokenObtainPairInputSchema` dan `TokenObtainPairController`. Lihat [Controller Schema Swapping](#controller-schema-swapping)

Selain itu, penting untuk diperhatikan bahwa `NinjaExtra` mendaftarkan handler untuk kelas `APIException` yang tidak tersedia pada instance `NinjaAPI`.
Untuk mengatasi hal ini, Anda memerlukan kode tambahan berikut:

```python
from ninja import NinjaAPI
from ninja_extra import exceptions

api = NinjaAPI()
api.add_router('', tags=['Auth'], router=router)

def api_exception_handler(request, exc):
    headers = {}

    if isinstance(exc.detail, (list, dict)):
        data = exc.detail
    else:
        data = {"detail": exc.detail}

    response = api.create_response(request, data, status=exc.status_code)
    for k, v in headers.items():
        response.setdefault(k, v)

    return response

api.exception_handler(exceptions.APIException)(api_exception_handler)
```

### Controller Schema Swapping

Anda sekarang dapat menukar (swap) schema controller di pengaturan `NINJA_JWT` tanpa mewarisi atau meng-override fungsionalitas controller Ninja JWT.

Semua input schema controller harus mewarisi dari `ninja_jwt.schema.InputSchemaMixin`, dan schema yang menghasilkan token harus mewarisi dari
 `ninja_jwt.schema.TokenObtainInputSchemaBase` atau `ninja_jwt.schema.TokenInputSchemaMixin` jika Anda menginginkan kontrol lebih.

Menggunakan contoh di atas:

```python
# project/schema.py
from typing import Type, Dict
from ninja_jwt.schema import TokenObtainInputSchemaBase
from ninja import Schema
from ninja_jwt.tokens import RefreshToken

class UserSchema(Schema):
    first_name: str
    email: str


class MyTokenObtainPairOutSchema(Schema):
    refresh: str
    access: str
    user: UserSchema


class MyTokenObtainPairInputSchema(TokenObtainInputSchemaBase):
    @classmethod
    def get_response_schema(cls) -> Type[Schema]:
        return MyTokenObtainPairOutSchema

    @classmethod
    def get_token(cls, user) -> Dict:
        values = {}
        refresh = RefreshToken.for_user(user)
        values["refresh"] = str(refresh)
        values["access"] = str(refresh.access_token)
        values.update(user=UserSchema.from_orm(user)) # this will be needed when creating output schema
        return values
```

Di `MyTokenObtainPairInputSchema` kita meng-override method `get_token` untuk mendefinisikan token kita serta beberapa data yang dibutuhkan oleh output schema.
Kita juga meng-override method `get_response_schema` untuk mendefinisikan output schema kita, yaitu `MyTokenObtainPairOutSchema`.

Selanjutnya, kita menerapkan schema `MyTokenObtainPairInputSchema` ke controller. Ini dapat dilakukan dengan mudah di pengaturan `NINJA_JWT`.

```python
# project/settings.py

NINJA_JWT = {
    'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA': 'project.schema.MyTokenObtainPairInputSchema',
}
```
Schema lain yang dapat ditukar (swappable) dapat diatur sebagai berikut
```python
# project/settings.py

NINJA_JWT = {
    # FOR OBTAIN PAIR
    'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA': "project.schema.MyTokenObtainPairInputSchema",
    'TOKEN_OBTAIN_PAIR_REFRESH_INPUT_SCHEMA': "for.obtain_pair.refresh_input.schema",
    # FOR SLIDING TOKEN
    'TOKEN_OBTAIN_SLIDING_INPUT_SCHEMA':  "for.obtain_sliding.input.schema",
    'TOKEN_OBTAIN_SLIDING_REFRESH_INPUT_SCHEMA': "for.obtain_pair.refresh_input.schema",

    'TOKEN_BLACKLIST_INPUT_SCHEMA':  "for.blacklist_input.schema",
    'TOKEN_VERIFY_INPUT_SCHEMA':  "for.verify_input.schema",
}
```

![token_customization_git](./img/token_customize.gif)

!!! note
   `Controller Schema Swapping` hanya tersedia di **v5.2.4** ke atas

!!! success

    Lanjutkan ke bab berikutnya **[Membuat Token Secara Manual](creating_tokens_manually.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
