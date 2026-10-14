---
comments: true
---
# **Throttling / Ratenbegrenzung**

Throttling kann als eine Berechtigung betrachtet werden, die bestimmt, ob ein Request autorisiert werden soll.
Es stellt einen temporären Zustand dar, mit dem gesteuert wird, in welcher Rate Clients Requests an die API senden können.

```python
from ninja_extra import NinjaExtraAPI, throttle
api = NinjaExtraAPI()

@api.get('/users')
@throttle  # This will apply the default throttle classes [UserRateThrottle, AnonRateThrottle]
def my_throttled_endpoint(request):
    return 'foo'
```

!!! note
    Das obige Beispiel wird nicht gedrosselt, da der Standard-Scope von `UserRateThrottle` und `AnonRateThrottle` `none` ist

## **Mehrere Throttles**
Das Throttling von Django-ninja-extra unterstützt mehrere Throttles, was nützlich ist, um verschiedene Einschränkungen auf eine API anzuwenden,
wie z. B. Burst-Raten oder dauerhafte (sustained) Raten.
Beispielsweise möchten Sie Benutzer vielleicht auf maximal 60 Requests pro Minute und 1000 Requests pro Tag begrenzen.

```python
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import UserRateThrottle
api = NinjaExtraAPI()

class User60MinRateThrottle(UserRateThrottle):
    rate = "60/min"
    scope = "minutes"


class User1000PerDayRateThrottle(UserRateThrottle):
    rate = "1000/day"
    scope = "days"

@api.get('/users')
@throttle(User60MinRateThrottle, User1000PerDayRateThrottle)
def my_throttled_endpoint(request):
    return 'foo'

```
## **Einstellungen der Throttle-Richtlinie**
Sie können die Standard-Throttle-Klassen und -Raten global in der `settings.py` Ihres Projekts festlegen, indem Sie die folgenden Schlüssel überschreiben:
```python
# django settings.py
NINJA_EXTRA = {
    'THROTTLE_CLASSES': [
        "ninja_extra.throttling.AnonRateThrottle",
        "ninja_extra.throttling.UserRateThrottle",
    ],
    'THROTTLE_RATES': {
        'user': '1000/day',
        'anon': '100/day',
    },
    'NUM_PROXIES': None
}
```
Die in `THROTTLE_RATES` verwendeten Ratenbeschreibungen können `second`, `minute`, `hour` oder `day` als Throttle-Zeitraum enthalten.

```python
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import UserRateThrottle

api = NinjaExtraAPI()

@api.get('/users')
@throttle(UserRateThrottle)
def my_throttled_endpoint(request):
    return 'foo'
```

## **Client-Identifikation**
Clients werden über den HTTP-Header X-Forwarded-For und die WSGI-Variable REMOTE_ADDR identifiziert.
Dies sind die eindeutigen Kennungen, die zur Identifizierung der Client-IP-Adresse für das Throttling verwendet werden.
`X-Forwarded-For` hat Vorrang vor `REMOTE_ADDR` und wird entsprechend verwendet.

#### **Einschränkung von Client-Proxies**
Wenn Sie eindeutige Client-IP-Adressen strikt identifizieren müssen, müssen Sie zunächst die Anzahl der Anwendungs-Proxies konfigurieren, die hinter der API laufen, indem Sie die Einstellung `NUM_PROXIES` setzen. Diese Einstellung sollte eine ganze Zahl größer oder gleich null sein.
Wird sie auf einen Wert ungleich null gesetzt, wird die Client-IP – nachdem etwaige IP-Adressen der Anwendungs-Proxies zuerst ausgeschlossen wurden – als letzte IP-Adresse im Header X-Forwarded-For identifiziert. Wird sie auf null gesetzt, wird der Wert REMOTE_ADDR immer als identifizierende IP-Adresse verwendet.
Es ist wichtig zu verstehen, dass alle Clients hinter einem einzelnen eindeutigen [Network Address Translation (NAT)](https://en.wikipedia.org/wiki/Network_address_translation)-Gateway als ein einzelner Client behandelt werden, wenn Sie `NUM_PROXIES` konfigurieren.

!!! note
    Mehr Kontext zur Funktionsweise des Headers X-Forwarded-For und zur Identifizierung entfernter Client-IPs finden Sie hier.

## **Cache-Einstellungen des Throttle-Modells**
Das in django-ninja-extra verwendete Throttle-Modell nutzt das Django-Cache-Backend. Es verwendet den `default`-Wert von [`LocMemCache`]().
Weitere Details finden Sie in der [Cache-Dokumentation](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache) von Django.

Wenn Sie den im Throttle-Modell definierten Standard-Cache nicht verwenden möchten, finden Sie hier ein Beispiel, wie Sie einen anderen Cache für das Throttle-Modell definieren:
```python

from django.core.cache import caches
from ninja_extra.throttling import AnonRateThrottle


class CustomAnonRateThrottle(AnonRateThrottle):
    cache = caches['alternate']
```
## **API-Referenz**

## **Anonymes Rate Throttling**
Das Modell `AnonRateThrottle` wird für die Ratenbegrenzung unter Verwendung der IP-Adresse nicht authentifizierter Benutzer als Schlüssel verwendet.

Es eignet sich zur Begrenzung der Request-Rate von unbekannten Quellen.

Request-Berechtigungen werden bestimmt durch:
- Die in der abgeleiteten Klasse definierte `rate`
- Den in `THROTTLE_RATES` definierten Scope `anon` in den `NINJA_EXTRA`-Einstellungen in der `settings.py`.

## **User Rate Throttling**
Das Modell `UserRateThrottle` wird für die Ratenbegrenzung verwendet, indem ein Schlüssel aus der Benutzer-ID oder dem Primärschlüssel authentifizierter Benutzer erzeugt wird.
Nicht authentifizierte Requests greifen auf die IP-Adresse des eingehenden Requests zurück, um einen eindeutigen Schlüssel für die Ratenbegrenzung zu erzeugen.

Request-Berechtigungen werden bestimmt durch:
- Die in der abgeleiteten Klasse definierte `rate`
- Den in `THROTTLE_RATES` definierten Scope `user` in den `NINJA_EXTRA`-Einstellungen in der `settings.py`.


Sie können mehrere Benutzer-Throttle-Raten für das Modell `UserRateThrottle` verwenden, zum Beispiel:
```python
# example/throttles.py
from ninja_extra.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
```

```python
# django settings.py
NINJA_EXTRA = {
    'THROTTLE_CLASSES': [
        'example.throttles.BurstRateThrottle',
        'example.throttles.SustainedRateThrottle'
    ],
    'THROTTLE_RATES': {
        'burst': '60/min',
        'sustained': '1000/day'
    }
}
```
## **Dynamisches Rate Throttling**
Das Modell `DynamicRateThrottle` wird verwendet, um authentifizierte und nicht authentifizierte Benutzer ähnlich wie `UserRateThrottle` zu drosseln.
Sein Hauptmerkmal ist die Möglichkeit, den `scope` bei der Verwendung dynamisch festzulegen.
Zum Beispiel:
Wir können einen Scope in den Einstellungen definieren.

```python
# django settings.py
NINJA_EXTRA = {
    'THROTTLE_RATES': {
        'burst': '60/min',
        'sustained': '1000/day'
    }
}
```

```python
# api.py
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import DynamicRateThrottle
api = NinjaExtraAPI()

@api.get('/users')
@throttle(DynamicRateThrottle, scope='burst')
def get_users(request):
    return 'foo'

@api.get('/users/<int:id>')
@throttle(DynamicRateThrottle, scope='sustained')
def get_user_by_id(request, id: int):
    return 'foo'
```
Hier wenden wir dynamisch die Rate `sustained` und die Rate `burst` auf `get_users` bzw. `get_user_by_id` an.


!!! note "New in v0.15.8"
    Sie können alle Endpoint-Operationen eines Controllers auf Klassenebene des Controllers drosseln.

## **Controller-Throttling**

```python
# api.py
from ninja_extra import (
    NinjaExtraAPI, throttle, api_controller, ControllerBase,
    http_get
)
from ninja_extra.throttling import DynamicRateThrottle
api = NinjaExtraAPI()

@api_controller("/throttled-controller")
class ThrottlingControllerSample(ControllerBase):
    throttling_classes = [
        DynamicRateThrottle,
    ]
    throttling_init_kwargs = dict(scope="sustained")

    @http_get("/endpoint_1")
    @throttle(DynamicRateThrottle, scope='burst')
    def endpoint_1(self, request):
        # this will override the generally throttling applied at the controller
        return "foo"

    @http_get("/endpoint_2")
    def endpoint_2(self, request):
        return "foo"

    @http_get("/endpoint_3")
    def endpoint_3(self, request):
        return "foo"


api.register_controllers(ThrottlingControllerSample)
```
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
