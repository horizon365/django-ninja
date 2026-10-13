---
comments: true
---
# Path Parameters

You can declare path "parameters" using the same syntax as Python formatted strings (which, fortunately, also matches <a href="https://swagger.io/docs/specification/describing-parameters/#path-parameters" target="_blank">OpenAPI path parameters</a>):

```python hl_lines="1 2"
{!./src/tutorial/path/code01.py!}
```

The value of the path parameter `item_id` will be passed to your function as the argument `item_id`.

So, if you run this example and go to <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a>, you will see this response:

```JSON
{"item_id":"foo"}
```


### Path Parameters with Types

You can declare the type of a path parameter using standard Python type annotations in your function:

```python hl_lines="2"
{!./src/tutorial/path/code02.py!}
```

In this case, `item_id` is declared as an **`int`**. This gives you editor and linter support for error checking, code completion, etc.

If you run this code in your browser using <a href="http://localhost:8000/api/items/3" target="_blank">http://localhost:8000/api/items/3</a>, you will see this response:
```JSON
{"item_id":3}
```

!!! tip
    Note that the value your function receives (and returns) is **3**, as a Python `int` — not the string `"3"`.
    So, with just that type declaration, **Django Ninja** provides you with automatic request "parsing" and validation.



### Data Validation

On the other hand, if you visit <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a> <small>*(`"foo"` is not an int)*</small> in your browser, you will see an HTTP error like this:

```JSON hl_lines="8"
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```


### Django Path Converters

You can use [Django path converters](https://docs.djangoproject.com/en/stable/topics/http/urls/#path-converters)
to help parse the path:

```python hl_lines="1"
@api.get("/items/{int:item_id}")
def read_item(request, item_id):
    return {"item_id": item_id}
```

In this case, `item_id` will be parsed as an **`int`**. If `item_id` is not a valid `int`, the URL will not match.
(For example, if no other route matches, a 404 Not Found will be returned.)

!!! tip
    Note that since **Django Ninja** uses the default `str` type for un-annotated parameters, the value the above function receives (and returns) is `"3"`,
    as a Python `str` — not the integer **3**. To receive an `int`, simply declare `item_id` with an `int` type annotation in the function definition as usual:

    ```python hl_lines="2"
    @api.get("/items/{int:item_id}")
    def read_item(request, item_id:int):
        return {"item_id": item_id}
    ```
 
#### Path Parameters with Slashes

Django's `path` converter allows you to handle path-like parameters:

```python hl_lines="1"
@api.get('/dir/{path:value}')
def someview(request, value: str):
    return value
```
You can query this operation with `/dir/some/path/with-slashes`, and your `value` will equal `some/path/with-slashes`

### Multiple Parameters

You can pass as many variables as you want to the `path` — just remember to use unique names, and don't forget to use the same names in your function arguments.

```python
@api.get("/events/{year}/{month}/{day}")
def events(request, year: int, month: int, day: int):
    return {"date": [year, month, day]}
```


### Using a Schema

You can also use a schema to encapsulate interdependent path parameters (and validate them as a group):


```python hl_lines="1 2  5 6 7 8 9 10 11 15"
{!./src/tutorial/path/code010.py!}
```

!!! note
    Note that here we use a `Path` source hint to let **Django Ninja** know that this schema will be applied to path parameters.

### Documentation

Now, when you open <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a> in your browser, you will see the automatic, interactive API documentation.
![Django Ninja Swagger](../../img/tutorial-path-swagger.png)

!!! done

    Continue to the next chapter! **[Query Parameters](query-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
