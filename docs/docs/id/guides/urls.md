---
comments: true
---
# Reversing URLs

Setiap method dalam sebuah Django Ninja schema (atau `Router`) menghasilkan sebuah nama reverse URL.

## Bagaimana URL dihasilkan

URL-URL ini semuanya berada dalam sebuah namespace, yang secara default bernama `"api-1.0.0"`, dan setiap nama URL sesuai dengan fungsi yang didekorasinya.

Sebagai contoh:

```python
api = NinjaAPI()

@api.get("/")
def index(request):
    ...

index_url = reverse_lazy("api-1.0.0:index")
```

Nama URL implisit ini hanya ditetapkan untuk operation pertama pada setiap path API. Jika Anda *tidak* ingin nama reverse URL implisit dibuat, cukup tentukan `url_name=""` (string kosong) pada decorator method-nya.

### Mengubah nama URL

Alih-alih menggunakan nama URL default, Anda dapat menentukannya secara eksplisit sebagai properti pada decorator method-nya.
```python
@api.get("/users", url_name="user_list")
def users(request):
    ...

users_url = reverse_lazy("api-1.0.0:user_list")
```

Ini akan meng-override nama URL implisit apa pun untuk path API tersebut.


#### Meng-override nama URL default

Anda juga dapat meng-override penamaan URL implisit dengan meng-override method `get_operation_url_name`:

```python
class MyAPI(NinjaAPI):
    def get_operation_url_name(self, operation, router):
        return operation.view_func.__name__ + '_my_extra_suffix'

api = MyAPI()
```

### Namespace kustom

Namespace URL default dibentuk dengan mengawali `"api-"` pada version milik schema, namun Anda dapat menentukan namespace secara eksplisit dengan meng-override atribut `urls_namespace` dari class schema NinjaAPI.
```python

api = NinjaAPI(auth=token_auth, version='2')
api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')

api_users_url = reverse_lazy("api-2:users")
private_api_admins_url = reverse_lazy("private_api:admins")
```

!!! success

    Lanjutkan ke bagian berikutnya **[Async Support](async-support.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
