---
comments: true
---
# CSRF (Cross-Site Request Forgery)

## What is cross-site request forgery?
> [Cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery) occurs when a malicious website contains a link, a form button, or some JavaScript that is intended to use the credentials of a logged-in user (who visits the malicious website in their browser) to perform some action on your website (or other locations not covered by this document).


## How to defend against cross-site request forgery with Django Ninja
### Use authentication methods that are not automatically embedded in requests
Cross-site request forgery attacks rely on authentication methods that are automatically included in requests originating from other websites, such as [cookies](https://en.wikipedia.org/wiki/HTTP_cookie) or [Basic access authentication](https://en.wikipedia.org/wiki/Basic_access_authentication).
Using an authentication method that is not automatically embedded, such as `Authorization: Bearer`, mitigates this attack.


### Use Django's built-in cross-site request forgery protection
If you are using the default Django authentication, which uses cookies, you must also use the default [Django cross-site request forgery protection](https://docs.djangoproject.com/en/4.2/ref/csrf/).


By default, **Django Ninja** has cross-site request forgery protection turned **OFF** for all operations.
To turn it on, you need to use the `csrf` argument of the NinjaAPI class:

```python hl_lines="3"
from ninja import NinjaAPI

api = NinjaAPI(csrf=True)
```

<span style="color: red;">Warning</span>: Using cookie-based authentication with cross-site request forgery turned off is insecure! (e.g. `CookieKey`, or `django_auth`).


**Django Ninja** will automatically enable cross-site request forgery for cookie-based authentication.


```python hl_lines="8"
from ninja import NinjaAPI
from ninja.security import APIKeyCookie

class CookieAuth(APIKeyCookie):
    def authenticate(self, request, key):
        return key == "test"

api = NinjaAPI(auth=CookieAuth())

```


Or based on django-auth (which inherits from cookie-based authentication):

```python hl_lines="4"
from ninja import NinjaAPI
from ninja.security import django_auth

api = NinjaAPI(auth=django_auth)
```


#### Django `ensure_csrf_cookie` decorator
You can use the Django [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie) decorator on an unprotected route to make it include a `Set-Cookie` header for the cross-site request forgery token. Note that:
- The route decorator must execute before (i.e. above) the [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie) decorator.
- You must `csrf_exempt` that route.
- The `ensure_csrf_cookie` decorator only works on a Django `HttpResponse`, not on a dictionary like most Django Ninja decorators do.
```python hl_lines="4"
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

@api.post("/csrf")
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request):
    return HttpResponse()
```
A request to this route will trigger a response from Django with the appropriate `Set-Cookie` header.


#### Front-end code
You can use the [Using CSRF protection with AJAX](https://docs.djangoproject.com/en/4.2/howto/csrf/#using-csrf-protection-with-ajax) and [Setting the token on the AJAX request](https://docs.djangoproject.com/en/4.2/howto/csrf/#setting-the-token-on-the-ajax-request) sections of [How to use Django's CSRF protection](https://docs.djangoproject.com/en/4.2/howto/csrf/) to learn how to handle the cross-site request forgery protection token in your front-end code.


## About CORS
You may want to set up your front-end and API on different sites (in which case you can check out [django-cors-headers](https://github.com/adamchainz/django-cors-headers)).
Although not directly related to cross-site request forgery, CORS (Cross-Origin Resource Sharing) can be helpful when you define cross-site request forgery cookies on a different site than the one used by the front-end, as this is not allowed by the [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) by default.
Then you can check out the [django-cors-headers README](https://github.com/adamchainz/django-cors-headers#readme).

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
