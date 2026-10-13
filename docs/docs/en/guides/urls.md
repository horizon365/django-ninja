---
comments: true
---
# Reversing URLs

Each method in a Django Ninja schema (or `Router`) generates a reverse URL name.

## How URLs are generated

These URLs are all contained within a namespace, which defaults to `"api-1.0.0"`, and each URL name matches the function it decorates.

For example:

```python
api = NinjaAPI()

@api.get("/")
def index(request):
    ...

index_url = reverse_lazy("api-1.0.0:index")
```

This implicit URL name is only set for the first operation on each API path. If you do *not* want any implicit reverse URL name to be generated, simply specify `url_name=""` (an empty string) on the method decorator.

### Change the URL name

Instead of using the default URL name, you can explicitly specify it as a property on the method decorator.
```python
@api.get("/users", url_name="user_list")
def users(request):
    ...

users_url = reverse_lazy("api-1.0.0:user_list")
```

This will override any implicit URL name for this API path.


#### Override the default URL name

You can also override the implicit URL naming by overriding the `get_operation_url_name` method:

```python
class MyAPI(NinjaAPI):
    def get_operation_url_name(self, operation, router):
        return operation.view_func.__name__ + '_my_extra_suffix'

api = MyAPI()
```

### Custom namespace

The default URL namespace is built by prefixing `"api-"` to the schema's version, however you can explicitly specify the namespace by overriding the `urls_namespace` attribute of the NinjaAPI schema class.
```python

api = NinjaAPI(auth=token_auth, version='2')
api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')

api_users_url = reverse_lazy("api-2:users")
private_api_admins_url = reverse_lazy("private_api:admins")
```

!!! success

    Continue to the next section **[Async support](async-support.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
