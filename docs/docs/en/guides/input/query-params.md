---
comments: true
---
# Query Parameters

When you declare function parameters that are not part of path parameters, they are automatically interpreted as "query" parameters.
```python hl_lines="5"
{!./src/tutorial/query/code01.py!}
```

To query this operation, you can use a URL like this:

```
http://localhost:8000/api/weapons?offset=0&limit=10
```
By default, all GET parameters are strings; when you annotate your function parameters with types, they will be converted to that type and validated against it.

The same benefits that apply to path parameters also apply to query parameters:

- Editor support (obviously)
- Data "parsing"
- Data validation
- Automatic documentation


!!! note
    If you do not annotate your parameters, they will be treated as `str` type

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit, offset):
    # type(limit) == str
    # type(offset) == str
```

### Default Values

Since query parameters are not a fixed part of the path, they are optional and can have default values:

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit: int = 10, offset: int = 0):
    return weapons[offset : offset + limit]
```

In the example above, we set the default values of `offset=0` and `limit=10`.

So, visiting the URL:
```
http://localhost:8000/api/weapons
```
will be the same as visiting:
```
http://localhost:8000/api/weapons?offset=0&limit=10
```
If you visit, for example:
```
http://localhost:8000/api/weapons?offset=20
```

The parameter values in your function will be:

 - `offset=20` (because you set it in the URL)
 - `limit=10` (because that is the default value)


### Required and Optional Parameters

You can declare required or optional GET parameters the same way you declare Python function parameters:

```python hl_lines="5"
{!./src/tutorial/query/code02.py!}
```

In this case, **Django Ninja** will always validate the `q` parameter you pass in the GET request, while the `offset` parameter is an optional integer.

### GET Parameter Type Conversion

Let's declare multiple typed parameters:
```python hl_lines="5"
{!./src/tutorial/query/code03.py!}
```
The `str` type is passed as-is.

For the `bool` type, all of the following:
```
http://localhost:8000/api/example?b=1
http://localhost:8000/api/example?b=True
http://localhost:8000/api/example?b=true
http://localhost:8000/api/example?b=on
http://localhost:8000/api/example?b=yes
```
or any other case variation (uppercase, capitalized, etc.), your function will see
that the parameter `b` has the `bool` value `True`, otherwise `False`.

Dates can be date strings and integers (Unix timestamps):

<pre style="font-size: .85em; background-color:rgb(245, 245, 245);">
http://localhost:8000/api/example?d=<strong>1577836800</strong>  # equivalent to 2020-01-01
http://localhost:8000/api/example?d=<strong>2020-01-01</strong>
</pre>


### Using a Schema

You can also use a schema to encapsulate GET parameters:

```python hl_lines="1 2  5 6 7 8"
{!./src/tutorial/query/code010.py!}
```

For more complex filtering scenarios, refer to [Filtering](./filtering.md).

!!! done

    Continue to the next chapter! **[Request Body](body.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
