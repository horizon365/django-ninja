---
comments: true
---
# Pagination

**Django Ninja** comes with pagination support. This allows you to split large result sets into separate pages.


To apply pagination to a function — simply apply the `paginate` decorator:

```python hl_lines="1 4"
from ninja.pagination import paginate

@api.get('/users', response=List[UserSchema])
@paginate
def list_users(request):
    return User.objects.all()
```


That's it!

Now you can query users using the `limit` and `offset` GET parameters

```
/api/users?limit=10&offset=0
```

By default, the limit is set to `100` (you can change it in your settings.py using `NINJA_PAGINATION_PER_PAGE`)


## Built-in Pagination Classes

### LimitOffsetPagination (default)

This is the default pagination class (you can change it in your settings.py by pointing `NINJA_PAGINATION_CLASS` to the path of a class)

```python hl_lines="1 4"
from ninja.pagination import paginate, LimitOffsetPagination

@api.get('/users', response=List[UserSchema])
@paginate(LimitOffsetPagination)
def list_users(request):
    return User.objects.all()
```

Example query:
```
/api/users?limit=10&offset=0
```

This class has two input parameters:

 - `limit` - defines the number of querysets on a page (default = 100, can be changed via NINJA_PAGINATION_PER_PAGE)
 - `offset` - sets the page window offset (default: 0, indexing starts from 0)


### PageNumberPagination
```python hl_lines="1 4"
from ninja.pagination import paginate, PageNumberPagination

@api.get('/users', response=List[UserSchema])
@paginate(PageNumberPagination)
def list_users(request):
    return User.objects.all()
```

Example query:
```
/api/users?page=2
```

This class has one parameter `page` and by default outputs 100 querysets per page (can be changed via settings.py)

Page numbering starts from 1.

You can also set a custom page size value for each view individually:

```python hl_lines="2"
@api.get("/users")
@paginate(PageNumberPagination, page_size=50)
def list_users(...
```



## Accessing Pagination Parameters in a View Function

If you need to access the `Input` parameters used for pagination in your view function — use the `pass_parameter` argument

In that case, the input data will be available in `**kwargs`:

```python hl_lines="2 4"
@api.get("/someview")
@paginate(pass_parameter="pagination_info")
def someview(request, **kwargs):
    page = kwargs["pagination_info"].page
    return ...
```


## Creating a Custom Pagination Class

To create a custom pagination class, you should inherit from `ninja.pagination.PaginationBase` and override the `Input` and `Output` schema classes as well as the `paginate_queryset(self, queryset, request, **params)` method:

 - The `Input` schema is a schema class that describes the parameters that should be passed to the paginator (such as page number or limit/offset values).
 - The `Output` schema describes the schema of the page output (such as count/next/items, etc.).
 - The `paginate_queryset` method receives the initial queryset and should return an iterable containing only the data in the requested page. The method accepts the following parameters:
    - `queryset`: the queryset (or iterable) returned by the API function.
    - `pagination` - the paginator.Input parameters (parsed and validated)
    - `**params`: keyword arguments that will contain all the arguments the decorated function receives.


Example:

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

Tip: you can get the request object from the parameters:

```python
def paginate_queryset(self, queryset, pagination: Input, **params):
    request = params["request"]
```

#### Async Pagination

The standard **Django Ninja** pagination classes support async. If you want to handle async requests with a custom pagination class, you should inherit from `ninja.pagination.AsyncPaginationBase` and override the `apaginate_queryset(self, queryset, request, **params)` method.

### Output Attributes

By default, page items are placed in the `'items'` attribute. To override this behavior, you can use `items_attribute`:

```python hl_lines="4 8"
class CustomPagination(PaginationBase):
    ...
    class Output(Schema):
        results: List[Any]
        total: int
        per_page: int
    
    items_attribute: str = "results"

```


## Applying Pagination to Multiple Operations at Once

There is often a case where you need to add pagination to all views that return querysets or lists

You can use the built-in router class (`RouterPaginated`) which will automatically inject pagination into all operations defined with `response=List[SomeSchema]`:

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

In this example, both operations will have pagination enabled.

To apply pagination to the main `api` instance, you can use the `default_router` argument:


```python
api = NinjaAPI(default_router=RouterPaginated())

@api.get(...
```

!!! done

    Continue to the next chapter! **[Response Renderers](response-renderers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
