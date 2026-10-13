---
comments: true
---
# HTTP Methods

## Defining Operations

An `operation` can be one of the [HTTP methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods):

- GET (retrieve)
- POST (submit)
- PUT (update)
- DELETE (delete)
- PATCH (partial update)

**Django Ninja** has a decorator for each operation:

```python hl_lines="1 5 9 13 17"
@api.get("/path")
def get_operation(request):
    ...

@api.post("/path")
def post_operation(request):
    ...

@api.put("/path")
def put_operation(request):
    ...

@api.delete("/path")
def delete_operation(request):
    ...

@api.patch("/path")
def patch_operation(request):
    ...
```

For information about what can be passed to any of these decorators, see the [Operation Parameters](../../reference/operations-parameters.md) reference documentation.

## Handling Multiple Methods

If you need to handle multiple methods for a given path with a single function, you can use the `api_operation` decorator:

```python hl_lines="1"
@api.api_operation(["POST", "PATCH"], "/path")
def mixed_operation(request):
    ...
```

This feature can also be used to implement other HTTP methods that do not have a corresponding **Django Ninja** method, such as `HEAD` or `OPTIONS`.

```python hl_lines="1"
@api.api_operation(["HEAD", "OPTIONS"], "/path")
def mixed_operation(request):
    ...
```

!!! done

    Continue to the next chapter! **[Path Parameters](path-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
