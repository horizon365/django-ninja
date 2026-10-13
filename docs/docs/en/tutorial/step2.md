---
comments: true
---
# Tutorial - Handling input parameters

## Passing parameters from the query string

Let's modify the operation to accept a name from the URL query string. To do this, simply add a `name` argument to our function.

```python
@api.get("/hello")
def hello(request, name):
    return f"Hello {name}"
```

When we provide the named argument, we get the expected (HTTP 200) response.

<a href="http://localhost:8000/api/hello?name=you"
target="_blank">localhost:8000/api/hello?name=you</a>:

```json
"Hello you"
```

### Default values

If you don't provide the parameter, an HTTP 422 error response is returned.

*[HTTP 422]: Unprocessable Entity

<a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a>:

```json
{
  "detail": [
    {
      "loc": ["query", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

We can specify a default value for the `name` argument in case it is not provided:

```python hl_lines="2"
@api.get("/hello")
def hello(request, name="world"):
    return f"Hello {name}"
```

## Input types

**Django Ninja** uses standard [Python type hints](https://docs.python.org/3/library/typing.html) to format input types. If no type is provided, string is assumed (but providing type hints for all arguments is best practice).

Let's add a second operation that does some basic math with integers.

```python hl_lines="5-7"
@api.get("/hello")
def hello(request, name: str = "world"):
    return f"Hello {name}"

@api.get("/math")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

<a href="http://localhost:8000/api/math?a=2&b=3"
target="_blank">localhost:8000/api/math?a=2&b=3</a>:

```json
{
  "add": 5,
  "multiply": 6
}
```

## Passing parameters via path strings

You can declare path "parameters" using the same syntax as Python format strings.

Any parameter found in the path string will be passed to your function as an argument, instead of being taken from the query string.

```python hl_lines="1"
@api.get("/math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

Now we access the math operation via <a href="http://localhost:8000/api/math/2and3"
target="_blank">localhost:8000/api/math/2and3</a>.


## Passing parameters via the request body

We will change the `hello` operation to use an HTTP `POST` request, and get the parameters from the request body.

To specify that parameters come from the request body, we need to declare a schema.

*[Schema]: An extension of a Pydantic "Model"

```python hl_lines="1 5-6 8-10"
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class HelloSchema(Schema):
    name: str = "world"

@api.post("/hello")
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"
```

### Self-documenting API

Now accessing <a href="http://localhost:8000/api/hello" target="_blank">localhost:8000/api/hello</a> will result in an HTTP 405 error response, because we need to change the request made to this URL to the POST type.

*[HTTP 405]: Method Not Allowed

An easy way to do this is to use the Swagger documentation that is automatically created for us, at the default "/docs" URL (appended to our API URL root).

1. Visit <a href="http://localhost:8000/api/docs" target="_blank">localhost:8000/api/docs</a> to view the operations we created
1. Open the `/api/hello` operation
2. Click "Try it out"
3. Modify the request body
4. Click "Execute"

!!! success

    Continue to the next chapter **[Handling responses](step3.md)**
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
