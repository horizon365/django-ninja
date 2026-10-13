---
comments: true
---
# Form Data

**Django Ninja** also allows you to parse and validate `request.POST` data
(that is, `application/x-www-form-urlencoded` or `multipart/form-data`).

## Form Data as Parameters

```python hl_lines="1 4"
from ninja import NinjaAPI, Form

@api.post("/login")
def login(request, username: Form[str], password: Form[str]):
    return {'username': username, 'password': '*****'}
```

Note the following:

1) You need to import the `Form` class from `ninja`
```python
from ninja import Form
```

2) Use `Form` as the default value for the parameter:
```python
username: Form[str]
```

## Using a Schema

Similar to [Request Body](body.md#declare-it-as-a-parameter), you can use a schema to organize your parameters.

```python hl_lines="12"
{!./src/tutorial/form/code01.py!}
```

## Request Form + Path + Query Parameters

Similar to [Request Body](body.md#request-body-path-query-parameters), you can combine form data with other parameter sources.

You can declare query parameters **and** path parameters **and** form fields, **etc.** at the same time.

**Django Ninja** will recognize that function parameters matching path parameters should be **taken from the path**,
while function parameters declared with `Form(...)` should be **taken from the request form fields**, and so on.

```python hl_lines="12"
{!./src/tutorial/form/code02.py!}
```
## Mapping Empty Form Fields to Default Values

Optional form fields are often sent with empty values. This value is interpreted as an empty string, so for fields such as `int` or `bool`, it may fail validation.

As described in the Pydantic documentation, this can be solved by using [generic classes as types](https://pydantic.com.cn/usage/types/#generic-classes-as-types).

```python hl_lines="15 16 23-25"
{!./src/tutorial/form/code03.py!}
```

!!! done

    Continue to the next chapter! **[File Uploads](file-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
