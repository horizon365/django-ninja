---
comments: true
---
# Authentication

## Introduction

**Django Ninja** provides several tools to help you handle authentication and authorization easily, quickly, and in a standard way, without having to study and learn <a href="https://swagger.io/docs/specification/authentication/" target="_blank">all the security specifications</a>.

The core idea is that when you describe an API operation, you can define an authentication object.
```python hl_lines="2 7"
{!./src/tutorial/authentication/code001.py!}
```

In this example, the client will only be able to call the `pets` method if it uses Django session authentication (which is cookie-based by default), otherwise an HTTP-401 error will be returned.
If you only want to authorize superusers, you can use `from ninja.security import django_auth_superuser` instead.
## Automatic OpenAPI schema

Here is an example where the client needs to pass a header in order to authenticate:

`Authorization: Bearer supersecret`

```python hl_lines="4 5 6 7 10"
{!./src/tutorial/authentication/bearer01.py!}
```

Now go to the <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a> documentation.


![Swagger UI Auth](../img/auth-swagger-ui.png)

Now, when you click the **Authorize** button, you will be prompted to enter your authentication token.

![Swagger UI Auth](../img/auth-swagger-ui-prompt.png)

When you make a test call, every request will pass the authorization header.

## Global authentication

If you need to protect **all** of your API's methods, you can pass the `auth` argument to the `NinjaAPI` constructor:


```python hl_lines="11 19"
from ninja import NinjaAPI, Form
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaAPI(auth=GlobalAuth())

# @api.get(...)
# def ...

# @api.post(...)
# def ...
```

And, if you need to override some of the methods, you can do it again at the operation level by passing the `auth` argument. In this example, authentication will be disabled for the `/token` operation:
```python hl_lines="19"
{!./src/tutorial/authentication/global01.py!}
```

## Available authentication options

### Custom function


The "`auth=`" argument accepts any callable. **NinjaAPI** will only pass authentication when the callable returns a value that is **truthy** (converts to a boolean `True`). This return value will be assigned to the `request.auth` attribute.

```python hl_lines="1 2 3 6"
{!./src/tutorial/authentication/code002.py!}
```


### API keys

Some APIs use API keys for authorization. An API key is a token that a client provides when making an API call to identify itself. The key can be sent in the query string:
```
GET /something?api_key=abcdef12345
```

Or as a request header:

```
GET /something HTTP/1.1
X-API-Key: abcdef12345
```

Or as a cookie:

```
GET /something HTTP/1.1
Cookie: X-API-KEY=abcdef12345
```

**Django Ninja** comes with built-in classes to help you handle these situations.


#### In Query

```python hl_lines="1 2 5 6 7 8 9 10 11 12"
{!./src/tutorial/authentication/apikey01.py!}
```

In this example, we get a token from `GET['api_key']` and find the corresponding `Client` in the database. The Client instance will be set as the `request.auth` attribute.

Note: **`param_name`** is the name of the GET parameter that will be checked. If not set, the default `"key"` is used.


#### In Header

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey02.py!}
```

#### In Cookie

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey03.py!}
```



### HTTP Bearer

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/bearer01.py!}
```

### HTTP Basic authentication

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/basic01.py!}
```


## Multiple authenticators

The **`auth`** argument also allows you to pass multiple authenticators:

```python hl_lines="18"
{!./src/tutorial/authentication/multiple01.py!}
```

In this case, **Django Ninja** will first check the API key from `GET`, and if it is not set or invalid, it will check the `header` key.
If both are invalid, it will raise an authentication error to the response.


## Router authentication

Use the `auth` argument on a router to apply an authenticator to all operations declared within it:

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

Or using the router constructor
```python
router = Router(auth=BasicAuth())
```


## Custom exceptions

Raising an exception that has an exception handler will return that handler's response in the same way as an operation:

```python hl_lines="1 4"
{!./src/tutorial/authentication/bearer02.py!}
```


## Async authentication

**Django Ninja** has basic support for asynchronous authentication. While the default authentication classes are not async-compatible, you can still define your custom async authentication callable and pass it with `auth`.

```python
async def async_auth(request):
    ...


@api.get("/pets", auth=async_auth)
def pets(request):
    ...
```


For more information, see [Error handling](errors.md) .

!!! success

    Continue to the next section **[Testing](testing.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
