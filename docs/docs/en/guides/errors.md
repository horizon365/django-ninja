---
comments: true
---
# Error handling

**Django Ninja** allows you to install custom exception handlers to control how responses are returned when errors or handled exceptions occur.

## Custom exception handlers

Suppose you are building an API that depends on some external service that is designed to be unavailable at certain moments. You can handle that error and return some friendly response to the client (telling them to come back later) instead of throwing the default 500 error when the exception occurs.
To achieve this, you need to:

 - 1) Create some exception (or use an existing one)
 - 2) Use the api.exception_handler decorator


Example:


```python hl_lines="9 10"
api = NinjaAPI()

class ServiceUnavailableError(Exception):
    pass


# initializing handler

@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=503,
    )


# some logic that throws exception

@api.get("/service")
def some_operation(request):
    if random.choice([True, False]):
        raise ServiceUnavailableError()
    return {"message": "Hello"}

```

The exception handler function takes 2 arguments:

 - **request** - Django's HTTP request
 - **exc** - the actual exception

The function must return an HTTP response

## Override default exception handlers

By default, **Django Ninja** initializes the following exception handlers:


#### `ninja.errors.AuthenticationError`

Thrown when authentication data is invalid

#### `ninja.errors.ValidationError`

Thrown when request data fails validation

#### `ninja.errors.HttpError`

Used to throw an HTTP error with a status code from anywhere in the code
#### `django.http.Http404`
 
Django's default 404 exception (can be returned, for example, using get_object_or_404)
#### `Exception`
 
Any other exception not handled by the application.
Default behavior
 
  - **If `settings.DEBUG` is `True`** - returns a traceback in plain text (useful when debugging in the console or Swagger UI)
  - **else** - uses the default Django exception handling mechanism (error logging, sending emails to ADMINS)


### Override default handlers

If you need to change the default output of validation errors - override the ValidationError exception handler:

```python hl_lines="1 4"
from ninja.errors import ValidationError
...

@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return HttpResponse("Invalid input", status=422)
```


## Throwing HTTP responses via exceptions

As an alternative to creating a custom exception and writing a handler for it - you can also throw an HTTP exception, which will result in an HTTP response with the desired code being returned

```python
from ninja.errors import HttpError

@api.get("/some/resource")
def some_operation(request):
    if True:
        raise HttpError(503, "Service Unavailable. Please retry later.")

```
!!! success

    Continue to the next section **[Reversing URLs](urls.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
