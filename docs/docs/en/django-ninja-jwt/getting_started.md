
#### Requirements
- Python >= 3.6
- Django >= 2.1
- Django-Ninja >= 0.16.1
- Django-Ninja-Extra >= 0.11.0

These are the officially supported Python and package versions. Other versions may also work. You are free to modify the tox configuration and see what is possible.

## Installation

Ninja JWT can be installed via pip:

    pip install django-ninja-jwt

Additionally, you need to register the `NinjaJWTDefaultController` controller with your Django-Ninja API.

```python
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

```
`NinjaJWTDefaultController` comes with three routes `obtain_token`, `refresh_token` and `verify_token`.
It is a combination of two subclasses, `TokenVerificationController` and `TokenObtainPairController`.
If you wish to customize these routes, you can inherit from these controllers and change their implementation.

```python
from ninja_extra import api_controller
from ninja_jwt.controller import TokenObtainPairController

@api_controller('token', tags=['Auth'])
class MyCustomController(TokenObtainPairController):
    """Only obtain token and refresh token"""
...
api.register_controllers(MyCustomController)
```

If you wish to use localization/translation, simply add `ninja_jwt` to `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    ...
    'ninja_jwt',
    ...
]
```

## Usage

To verify that Ninja JWT is working, you can issue a few test requests with curl:

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "davidattenborough", "password": "boatymcboatface"}' \
  http://localhost:8000/api/token/pair

...
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}
```

You can use the returned access token to prove authentication for protected views:

``` {.sourceCode .bash}
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
  http://localhost:8000/api/some-protected-view/
```

When this short-lived access token expires, you can use the longer-lived refresh token to obtain another access token:

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"}' \
  http://localhost:8000/api/token/refresh/

...
{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXN...", "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVm..."}
```

Cryptographic Dependencies (Optional)
-------------------------------------

If you plan to encode or decode tokens using certain digital signature algorithms (i.e., RSA and ECDSA; see PyJWT for other algorithms),
you will need to install the cryptography_ library. This can be installed explicitly, or as a required item of the `django-ninja-jwt` requirements:

    pip install django-ninja-jwt[crypto]

When using the `Ninja JWT` project's requirements file, the `django-ninja-jwt[crypto]` format is recommended,
because a separate `cryptography` requirement line may later be mistaken as an unused requirement and removed.
[cryptography](https://cryptography.io)

!!! success

    Continue to the next chapter **[Route Authentication](auth_integration.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
