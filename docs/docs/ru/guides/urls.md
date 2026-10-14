---
comments: true
---
# Реверс URL

Каждый метод в схеме Django Ninja (или `Router`) генерирует имя для реверса URL.

## Как генерируются URL

Все эти URL содержатся в пространстве имён, которое по умолчанию равно `"api-1.0.0"`, и каждое имя URL совпадает с функцией, которую оно декорирует.

Например:

```python
api = NinjaAPI()

@api.get("/")
def index(request):
    ...

index_url = reverse_lazy("api-1.0.0:index")
```

Это неявное имя URL устанавливается только для первой операции на каждом пути API. Если вы *не* хотите, чтобы генерировалось неявное имя для реверса URL, просто укажите `url_name=""` (пустую строку) в декораторе метода.

### Изменение имени URL

Вместо использования имени URL по умолчанию вы можете явно указать его как свойство в декораторе метода.
```python
@api.get("/users", url_name="user_list")
def users(request):
    ...

users_url = reverse_lazy("api-1.0.0:user_list")
```

Это переопределит любое неявное имя URL для этого пути API.


#### Переопределение имени URL по умолчанию

Вы также можете переопределить неявное именование URL, переопределив метод `get_operation_url_name`:

```python
class MyAPI(NinjaAPI):
    def get_operation_url_name(self, operation, router):
        return operation.view_func.__name__ + '_my_extra_suffix'

api = MyAPI()
```

### Пользовательское пространство имён

Пространство имён URL по умолчанию строится путём добавления префикса `"api-"` к версии схемы, однако вы можете явно указать пространство имён, переопределив атрибут `urls_namespace` класса схемы NinjaAPI.
```python

api = NinjaAPI(auth=token_auth, version='2')
api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')

api_users_url = reverse_lazy("api-2:users")
private_api_admins_url = reverse_lazy("private_api:admins")
```

!!! success

    Переходите к следующему разделу **[Поддержка асинхронности](async-support.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
