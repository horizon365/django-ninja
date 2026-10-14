
#### Vereisten
- Python >= 3.6
- Django >= 2.1
- Django-Ninja >= 0.16.1
- Django-Ninja-Extra >= 0.11.0

Dit zijn de officieel ondersteunde Python- en pakketversies. Andere versies kunnen ook werken. Je bent vrij om de tox-configuratie aan te passen en te zien wat mogelijk is.

## Installatie

Ninja JWT kan via pip worden geïnstalleerd:

    pip install django-ninja-jwt

Daarnaast moet je de controller `NinjaJWTDefaultController` registreren bij je Django-Ninja API.

```python
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

```
`NinjaJWTDefaultController` wordt geleverd met drie routes: `obtain_token`, `refresh_token` en `verify_token`.
Het is een combinatie van twee subklassen, `TokenVerificationController` en `TokenObtainPairController`.
Als je deze routes wilt aanpassen, kun je van deze controllers erven en hun implementatie wijzigen.

```python
from ninja_extra import api_controller
from ninja_jwt.controller import TokenObtainPairController

@api_controller('token', tags=['Auth'])
class MyCustomController(TokenObtainPairController):
    """Only obtain token and refresh token"""
...
api.register_controllers(MyCustomController)
```

Als je lokalisatie/vertaling wilt gebruiken, voeg je eenvoudig `ninja_jwt` toe aan `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    ...
    'ninja_jwt',
    ...
]
```

## Gebruik

Om te verifiëren dat Ninja JWT werkt, kun je een paar testverzoeken met curl doen:

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

Je kunt het geretourneerde access token gebruiken om authenticatie aan te tonen voor beveiligde views:

``` {.sourceCode .bash}
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
  http://localhost:8000/api/some-protected-view/
```

Wanneer dit kortstondige access token verloopt, kun je het langer geldige refresh token gebruiken om een nieuw access token te verkrijgen:

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"}' \
  http://localhost:8000/api/token/refresh/

...
{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXN...", "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVm..."}
```

Cryptografische Afhankelijkheden (Optioneel)
-------------------------------------

Als je van plan bent tokens te encoderen of decoderen met bepaalde digitale handtekeningalgoritmen (d.w.z. RSA en ECDSA; zie PyJWT voor andere algoritmen),
moet je de library cryptography_ installeren. Dit kan expliciet gebeuren, of als vereist onderdeel van de requirements van `django-ninja-jwt`:

    pip install django-ninja-jwt[crypto]

Bij gebruik van het requirements-bestand van het `Ninja JWT`-project wordt het formaat `django-ninja-jwt[crypto]` aanbevolen,
omdat een aparte `cryptography`-requirementregel later kan worden aangezien voor een ongebruikte requirement en wordt verwijderd.
[cryptography](https://cryptography.io)

!!! success

    Ga verder naar het volgende hoofdstuk **[Route-authenticatie](auth_integration.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
