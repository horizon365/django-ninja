
#### Voraussetzungen
- Python >= 3.6
- Django >= 2.1
- Django-Ninja >= 0.16.1
- Django-Ninja-Extra >= 0.11.0

Dies sind die offiziell unterstützten Python- und Paketversionen. Andere Versionen funktionieren möglicherweise ebenfalls. Sie können die tox-Konfiguration gerne anpassen und ausprobieren, was möglich ist.

## Installation

Ninja JWT kann über pip installiert werden:

    pip install django-ninja-jwt

Zusätzlich müssen Sie den Controller `NinjaJWTDefaultController` bei Ihrer Django-Ninja-API registrieren.

```python
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

```
`NinjaJWTDefaultController` verfügt über drei Routen: `obtain_token`, `refresh_token` und `verify_token`.
Er ist eine Kombination aus zwei Unterklassen: `TokenVerificationController` und `TokenObtainPairController`.
Wenn Sie diese Routen anpassen möchten, können Sie von diesen Controllern erben und deren Implementierung ändern.

```python
from ninja_extra import api_controller
from ninja_jwt.controller import TokenObtainPairController

@api_controller('token', tags=['Auth'])
class MyCustomController(TokenObtainPairController):
    """Only obtain token and refresh token"""
...
api.register_controllers(MyCustomController)
```

Wenn Sie Lokalisierung/Übersetzung verwenden möchten, fügen Sie einfach `ninja_jwt` zu `INSTALLED_APPS` hinzu.

```python
INSTALLED_APPS = [
    ...
    'ninja_jwt',
    ...
]
```

## Verwendung

Um zu überprüfen, ob Ninja JWT funktioniert, können Sie einige Test-Requests mit curl ausführen:

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

Sie können das zurückgegebene Access-Token verwenden, um die Authentifizierung für geschützte Views nachzuweisen:

``` {.sourceCode .bash}
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
  http://localhost:8000/api/some-protected-view/
```

Wenn dieses kurzlebige Access-Token abläuft, können Sie das langlebigere Refresh-Token verwenden, um ein weiteres Access-Token zu erhalten:

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"}' \
  http://localhost:8000/api/token/refresh/

...
{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXN...", "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVm..."}
```

Kryptografische Abhängigkeiten (Optional)
-------------------------------------

Wenn Sie planen, Token mit bestimmten Algorithmen für digitale Signaturen zu kodieren oder zu dekodieren (d. h. RSA und ECDSA; siehe PyJWT für weitere Algorithmen),
müssen Sie die Bibliothek cryptography_ installieren. Diese kann explizit installiert werden oder als erforderlicher Bestandteil der Anforderungen von `django-ninja-jwt`:

    pip install django-ninja-jwt[crypto]

Wenn Sie die Requirements-Datei des Projekts `Ninja JWT` verwenden, wird das Format `django-ninja-jwt[crypto]` empfohlen,
da eine separate Requirements-Zeile für `cryptography` später fälschlicherweise als ungenutzte Anforderung angesehen und entfernt werden könnte.
[cryptography](https://cryptography.io)

!!! success

    Fahren Sie mit dem nächsten Kapitel fort: **[Routenauthentifizierung](auth_integration.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
