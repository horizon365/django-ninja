---
comments: true
---
# Tweaking the Response

Sometimes you will want to alter a response just before it is served, for example to add a header or modify a cookie.

To do this, simply declare a function argument of type `HttpResponse`:

```python
from django.http import HttpRequest, HttpResponse

@api.get("/cookie/")
def feed_cookiemonster(request: HttpRequest, response: HttpResponse):
    # Set a cookie.
    response.set_cookie("cookie", "delicious")
    # Set a header.
    response["X-Cookiemonster"] = "blue"
    return {"cookiemonster_happy": True}
```


## Temporal Response Object

This response object is used as the base for all responses built by Django Ninja, including error responses.
If a Django `HttpResponse` object is returned directly by an operation, then this object is *not* used.

Obviously this response object will not yet contain content, but it does set `content_type` (though you probably do not want to change it).

The `status_code` will be overridden based on the return value (default is 200, or the status code if a two-part tuple is returned).


## Changing the Base Response Object

You can change this temporal response object by overriding the `NinjaAPI.create_temporal_response` method.

```python
    def create_temporal_response(self, request: HttpRequest) -> HttpResponse:
        response = super().create_temporal_response(request)
        # Do your magic here...
        return response
```

!!! done

    Continue to the next chapter! **[Generating Schemas from Django Models](django-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
