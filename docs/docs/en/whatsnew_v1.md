---
comments: true
---
# Welcome to Django Ninja 1.0


To get started, install the latest version using the following command:
```
pip install -U django-ninja
```

django-ninja v1 is compatible with Python 3.7 and above.


The Django Ninja 0.x series is still supported, but will only receive security updates and critical bug fixes.


✨ What's new in Django Ninja 1.0

## Pydantic2 support

Pydantic version 2 is rewritten in Rust and includes many improvements and features, such as:

 - Safer types.
 - Better extensibility.
 - Better performance.

According to our tests, an average project can gain about a 10% performance improvement on average, while in some edge parsing/serialization scenarios you can get a 4x boost.
On the other hand, it introduces breaking changes — pydantic 1 and 2 are not fully compatible — but we have tried to make this transition as easy as possible.
So if you used the 'Schema' class, migrating to ninja v1 should be straightforward. Otherwise, please follow the [pydantic migration guide](https://pydantic.com.cn/migration/)


Some new features provided by pydantic2

### pydantic context

Pydantic now supports context during validation and serialization, and Django Ninja passes the "request" object through during request and response handling.
```Python hl_lines="6 7"
class Payload(Schema):
    id: int
    name: str
    request_path: str

    @staticmethod
    def resolve_request_path(data, context):
        request = context["request"]
        return request.get_full_path()

```

During the response phase, "response_code" is also passed to the context.

## Schema.Meta

Pydantic has now deprecated the BaseModel.Config class. However, to stay consistent with all other Django parts, we introduced a "Meta" class for ModelSchema — it works similarly to Django's ModelForms:
```Python hl_lines="2 4"
class TxItem(ModelSchema):
    class Meta:
        model = Transaction
        fields = ["id", "account", "amount", "timestamp"]

```

(The "Config" class is still supported, but is now deprecated)


## Shorter/cleaner parameter syntax

```python
@api.post('/some')
def some_form(request, username: Form[str], password: Form[str]):
    return True
```

instead of

```python
@api.post('/some')
def some_form(request, username: str = Form(...), password: str = Form(...)):
    return True
```

or

```python
@api.post('/some')
def some_form(request, data: Form[AuthSchema]):
    return True
```


instead of

```python
@api.post('/some')
def some_form(request, data: AuthSchema = Form(...)):
    return True
```



as well as all the autocompletion features in your editor.


On the other hand, **the old syntax is still supported**, so you can effortlessly port your project to the latest django-ninja version.


#### + Annotated

typing.Annotated is also now supported:

```Python
@api.get("/annotated")
def annotated(request, data: Annotated[SomeData, Form()]):
    return {"data": data.dict()}

```


## Async auth support

Async authenticators are finally supported. All you have to do is add `async` to your `authenticate` method:

```Python
class Auth(HttpBearer):
    async def authenticate(self, request, token):
        await asyncio.sleep(1)
        if token == "secret":
            return token

```


## Changed CSRF behavior


`csrf=True` is no longer required if you use cookie-based authentication. Instead, CSRF protection is enabled automatically. This also lets you mix CSRF-protected authenticators with other methods that don't require cookies:

```Python
api = NinjaAPI(auth=[django_auth, Auth()])
```


## Documentation

The documentation viewer is now configurable and pluggable. By default, django-ninja ships with Swagger and Redoc:
```Python
from ninja import NinjaAPI, Redoc, Swagger


# use redoc
api = NinjaAPI(docs=Redoc()))

# use swagger:
api = NinjaAPI(docs=Swagger())

# set configuration for swagger:
api = NinjaAPI(docs=Swagger({"persistAuthorization": True}))
```

Users can now create custom documentation viewers by subclassing the `DocsBase` class.

## Router

add_router supports string paths:

```Python
api = NinjaAPI()


api.add_router('/app1', 'myproject.app1.router')
api.add_router('/app2', 'myproject.app2.router')
api.add_router('/app3', 'myproject.app3.router')
api.add_router('/app4', 'myproject.app4.router')
api.add_router('/app5', 'myproject.app5.router')
```


## Decorators

When django-ninja decorates a view with .get/.post etc., it wraps the result of the function (in most cases not an HttpResponse - but some serializable object), so it is unlikely to work with some built-in or third-party decorators, such as:
```python hl_lines="4"
from django.views.decorators.cache import cache_page

@api.get("/test")
@cache_page(5) # <----- will not work!
def test_view(request):
    return {"some": "Complex data"}
```
This example will not work.

Now django-ninja introduces a decorate_view decorator that allows injecting decorators that work with http responses:
```python hl_lines="1 4"
from ninja.decorators import decorate_view

@api.get("/test")
@decorate_view(cache_page(5))
def test_view(request):
    return str(datetime.now())
```


## Pagination

The `paginate_queryset` method now accepts the `request` object


#### Backward-incompatible items
 - resolve_xxx(self, ...) - support for (self) resolution is deprecated in favor of pydantic's built-in functionality.
 - pydantic v1 is no longer supported
 - python 3.6 is no longer supported

By the way - if you like this project and haven't given it a GitHub star yet - please do so! [github star](img/github-star.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
