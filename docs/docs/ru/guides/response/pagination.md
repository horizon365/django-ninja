---
comments: true
---
# Пагинация

**Django Ninja** поставляется с поддержкой пагинации. Это позволяет разбивать большие наборы результатов на отдельные страницы.


Чтобы применить пагинацию к функции — просто примените декоратор `paginate`:

```python hl_lines="1 4"
from ninja.pagination import paginate

@api.get('/users', response=List[UserSchema])
@paginate
def list_users(request):
    return User.objects.all()
```


Вот и всё!

Теперь вы можете запрашивать пользователей с помощью GET-параметров `limit` и `offset`

```
/api/users?limit=10&offset=0
```

По умолчанию limit установлен в `100` (вы можете изменить это в вашем settings.py с помощью `NINJA_PAGINATION_PER_PAGE`)


## Встроенные классы пагинации

### LimitOffsetPagination (по умолчанию)

Это класс пагинации по умолчанию (вы можете изменить его в вашем settings.py, указав в `NINJA_PAGINATION_CLASS` путь к классу)

```python hl_lines="1 4"
from ninja.pagination import paginate, LimitOffsetPagination

@api.get('/users', response=List[UserSchema])
@paginate(LimitOffsetPagination)
def list_users(request):
    return User.objects.all()
```

Пример запроса:
```
/api/users?limit=10&offset=0
```

Этот класс имеет два входных параметра:

 - `limit` — определяет количество queryset'ов на странице (по умолчанию = 100, можно изменить через NINJA_PAGINATION_PER_PAGE)
 - `offset` — задаёт смещение окна страницы (по умолчанию: 0, индексация начинается с 0)


### PageNumberPagination
```python hl_lines="1 4"
from ninja.pagination import paginate, PageNumberPagination

@api.get('/users', response=List[UserSchema])
@paginate(PageNumberPagination)
def list_users(request):
    return User.objects.all()
```

Пример запроса:
```
/api/users?page=2
```

Этот класс имеет один параметр `page` и по умолчанию выводит 100 queryset'ов на страницу (можно изменить через settings.py)

Нумерация страниц начинается с 1.

Вы также можете задать пользовательский размер страницы для каждого представления отдельно:

```python hl_lines="2"
@api.get("/users")
@paginate(PageNumberPagination, page_size=50)
def list_users(...
```



## Доступ к параметрам пагинации в функции представления

Если вам нужен доступ к параметрам `Input`, используемым для пагинации, в вашей функции представления — используйте аргумент `pass_parameter`

В этом случае входные данные будут доступны в `**kwargs`:

```python hl_lines="2 4"
@api.get("/someview")
@paginate(pass_parameter="pagination_info")
def someview(request, **kwargs):
    page = kwargs["pagination_info"].page
    return ...
```


## Создание пользовательского класса пагинации

Чтобы создать пользовательский класс пагинации, вы должны унаследоваться от `ninja.pagination.PaginationBase` и переопределить классы схем `Input` и `Output`, а также метод `paginate_queryset(self, queryset, request, **params)`:

 - Схема `Input` — это класс схемы, описывающий параметры, которые должны передаваться пагинатору (например, номер страницы или значения limit/offset).
 - Схема `Output` описывает схему вывода страницы (например, count/next/items и т. д.).
 - Метод `paginate_queryset` получает исходный queryset и должен вернуть итерируемый объект, содержащий только данные запрошенной страницы. Метод принимает следующие параметры:
    - `queryset`: queryset (или итерируемый объект), возвращённый API-функцией.
    - `pagination` — параметры paginator.Input (разобранные и проверенные)
    - `**params`: именованные аргументы, которые будут содержать все аргументы, получаемые декорируемой функцией.


Пример:

```python hl_lines="7 11 16 26"
from ninja.pagination import paginate, PaginationBase
from ninja import Schema


class CustomPagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        skip: int
        

    class Output(Schema):
        items: List[Any] # `items` is a default attribute
        total: int
        per_page: int

    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        return {
            'items': queryset[skip : skip + 5],
            'total': queryset.count(),
            'per_page': 5,
        }


@api.get('/users', response=List[UserSchema])
@paginate(CustomPagination)
def list_users(request):
    return User.objects.all()
```

Совет: вы можете получить объект запроса из параметров:

```python
def paginate_queryset(self, queryset, pagination: Input, **params):
    request = params["request"]
```

#### Асинхронная пагинация

Стандартные классы пагинации **Django Ninja** поддерживают async. Если вы хотите обрабатывать асинхронные запросы с пользовательским классом пагинации, вы должны унаследоваться от `ninja.pagination.AsyncPaginationBase` и переопределить метод `apaginate_queryset(self, queryset, request, **params)`.

### Атрибуты вывода

По умолчанию элементы страницы помещаются в атрибут `'items'`. Чтобы переопределить это поведение, вы можете использовать `items_attribute`:

```python hl_lines="4 8"
class CustomPagination(PaginationBase):
    ...
    class Output(Schema):
        results: List[Any]
        total: int
        per_page: int
    
    items_attribute: str = "results"

```


## Применение пагинации к нескольким операциям сразу

Часто бывает случай, когда нужно добавить пагинацию ко всем представлениям, возвращающим queryset'ы или списки

Вы можете использовать встроенный класс роутера (`RouterPaginated`), который автоматически внедрит пагинацию во все операции, определённые с `response=List[SomeSchema]`:

```python hl_lines="1 3 6 10"
from ninja.pagination import RouterPaginated

router = RouterPaginated()


@router.get("/items", response=List[MySchema])
def items(request):
    return MyModel.objects.all()

@router.get("/other-items", response=List[OtherSchema])
def ohter_items(request):
    return OtherModel.objects.all()

```

В этом примере обе операции будут иметь включённую пагинацию.

Чтобы применить пагинацию к основному экземпляру `api`, вы можете использовать аргумент `default_router`:


```python
api = NinjaAPI(default_router=RouterPaginated())

@api.get(...
```

!!! done

    Переходите к следующей главе! **[Рендереры ответов](response-renderers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
