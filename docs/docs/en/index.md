---
title: Django Ninja - Fast Django REST framework
template: home.html
comments: true
---

Django Ninja is a web framework for building APIs with Django and Python 3.6+ type hints.

Main features:

 - **Easy to understand**: Designed to be easy to use and intuitive.
 - **Fast execution**: Thanks to **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** and **<a href="guides/async-support/">async support</a>**, it has very high performance.
 - **Fast to code**: Django Ninja is a web framework for building APIs with Django and Python 3.6+ type hints.
 - **Standards-based**: Based on standards: **OpenAPI** (formerly Swagger) and **JSON Schema**.
 - **Django friendly**: (obviously) integrates well with Django core and the ORM.
 - **Production ready**: Used by multiple companies in real projects (if you use Django Ninja and want to publish your feedback, please email ppr.vitaly@gmail.com).

<a href="https://github.com/vitalik/django-ninja-benchmarks" target="_blank">Benchmarks</a>:

![Django Ninja REST Framework](img/benchmark.png)

## Installation

```
pip install django-ninja
```

## Quick example

Start a new Django project (or use an existing one)
```
django-admin startproject apidemo
```

In `urls.py`

```python hl_lines="3 5 8 9 10 15"
{!./src/index001.py!}
```

Now, run it as usual:
```
./manage.py runserver
```

Note: you don't have to add Django Ninja to your installed apps for it to work.

## Check it

Open your browser at <a href="http://127.0.0.1:8000/api/add?a=1&b=2" target="_blank">http://127.0.0.1:8000/api/add?a=1&b=2</a>

You will see the JSON response as:
```JSON
{"result": 3}
```
Now you have just created an API that:

 - Receives an HTTP GET request at `/api/add`
 - Receives, validates, and type-converts GET parameters `a` and `b`
 - Decodes the result as JSON
 - Generates an OpenAPI schema for the defined operation

## Interactive API documentation

Now go to <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

You will see the automatic, interactive API documentation (provided by <a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a> or <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a>) :

![Swagger UI](img/index-swagger-ui.png)


## Summary

In short, you only declare the types of parameters, request bodies, etc. **once**, as function arguments.

You do this with standard, modern Python types.

You don't have to learn a new syntax, the methods or classes of a specific library, etc.

Just standard **Python 3.6+**.

For example, for an `int`:

```python
a: int
```

Or, for a more complex `Item` model:

```python
class Item(Schema):
    foo: str
    bar: float

def operation(a: Item):
    ...
```

...with just this one declaration, you get:

* Editor support, including:
    * Autocompletion
    * Type checking
* Data validation:
    * Automatic and clear errors when data is invalid
    * Validation even for deeply nested JSON objects
* <abbr title="Also known as: serialization, parsing, marshalling">Serialization</abbr> of network input data and conversion to Python data output, and reading from:
    * JSON
    * Path parameters
    * Query parameters
    * Cookies
    * Headers
    * Forms
    * Files
* Automatic, interactive API documentation

This project was heavily inspired by <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a>.

!!! note

    Check out the **[Tutorial](tutorial/index.md)** to get started quickly.

    Ecosystem around Django Ninja:

    1. [django-ninja](index.md): A framework based on Django that takes the best of Django and pairs it with the power of Pydantic — the optimal choice at the intersection of security and convenience.

    2. [django-ninja-crud](django-ninja-crud/index.md): A framework built on django-ninja to simplify CRUD interface development, providing declarative model viewsets and scenario-based testing methods.

    3. [django-ninja-extra](django-ninja-extra/index.md): A tool that lets developers skip verbose Django documentation and quickly build powerful web applications and modern API interfaces with minimal code.

    4. [django-ninja-jwt](django-ninja-jwt/index.md): A JSON Web Token plugin for django-ninja that implements authentication and related features, forked from a popular Django Rest Framework plugin.
