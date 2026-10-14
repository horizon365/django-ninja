
#### आवश्यकताएँ
- Python >= 3.6
- Django >= 2.1
- Django-Ninja >= 0.16.1
- Django-Ninja-Extra >= 0.11.0

ये आधिकारिक रूप से समर्थित Python और package versions हैं। अन्य versions भी काम कर सकते हैं। आप tox configuration को संशोधित कर सकते हैं और देख सकते हैं कि क्या संभव है।

## Installation

Ninja JWT को pip के माध्यम से install किया जा सकता है:

    pip install django-ninja-jwt

साथ ही, आपको अपने Django-Ninja API के साथ `NinjaJWTDefaultController` controller को register करने की आवश्यकता है।

```python
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

```
`NinjaJWTDefaultController` तीन routes के साथ आता है: `obtain_token`, `refresh_token` और `verify_token`।
यह दो subclasses, `TokenVerificationController` और `TokenObtainPairController` का एक संयोजन है।
यदि आप इन routes को customize करना चाहते हैं, तो आप इन controllers से inherit कर सकते हैं और उनका implementation बदल सकते हैं।

```python
from ninja_extra import api_controller
from ninja_jwt.controller import TokenObtainPairController

@api_controller('token', tags=['Auth'])
class MyCustomController(TokenObtainPairController):
    """Only obtain token and refresh token"""
...
api.register_controllers(MyCustomController)
```

यदि आप localization/translation का उपयोग करना चाहते हैं, तो बस `ninja_jwt` को `INSTALLED_APPS` में जोड़ें।

```python
INSTALLED_APPS = [
    ...
    'ninja_jwt',
    ...
]
```

## उपयोग

यह सत्यापित करने के लिए कि Ninja JWT काम कर रहा है, आप curl के साथ कुछ test requests भेज सकते हैं:

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

आप protected views के लिए authentication सिद्ध करने के लिए लौटाए गए access token का उपयोग कर सकते हैं:

``` {.sourceCode .bash}
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
  http://localhost:8000/api/some-protected-view/
```

जब यह short-lived access token समाप्त हो जाता है, तो आप दोबारा एक access token प्राप्त करने के लिए longer-lived refresh token का उपयोग कर सकते हैं:

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

यदि आप कुछ विशेष digital signature algorithms (यानी RSA और ECDSA; अन्य algorithms के लिए PyJWT देखें) का उपयोग करके tokens को encode या decode करने की योजना बना रहे हैं,
तो आपको cryptography_ library install करने की आवश्यकता होगी। इसे स्पष्ट रूप से install किया जा सकता है, या `django-ninja-jwt` requirements के एक आवश्यक item के रूप में:

    pip install django-ninja-jwt[crypto]

`Ninja JWT` project की requirements file का उपयोग करते समय, `django-ninja-jwt[crypto]` format की अनुशंसा की जाती है,
क्योंकि एक अलग `cryptography` requirement line को बाद में एक अप्रयुक्त requirement मानकर हटाया जा सकता है।
[cryptography](https://cryptography.io)

!!! success

    अगले अध्याय **[Route Authentication](auth_integration.md)** पर जारी रखें।

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
