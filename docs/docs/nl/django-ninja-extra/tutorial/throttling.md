---
comments: true
---
# **Throttling / Snelheidsbeperking**

Throttling kan worden gezien als een permissie die bepaalt of een verzoek moet worden geautoriseerd.
Het vertegenwoordigt een tijdelijke toestand die wordt gebruikt om de snelheid te beheren waarmee clients verzoeken aan de API kunnen doen.

```python
from ninja_extra import NinjaExtraAPI, throttle
api = NinjaExtraAPI()

@api.get('/users')
@throttle  # This will apply the default throttle classes [UserRateThrottle, AnonRateThrottle]
def my_throttled_endpoint(request):
    return 'foo'
```

!!! note
    Het bovenstaande voorbeeld zal geen throttling ondergaan, omdat de standaard scope van `UserRateThrottle` en `AnonRateThrottle` `none` is

## **Meervoudige Throttling**
Throttling in Django-ninja-extra ondersteunt meerdere throttles, wat nuttig is voor het toepassen van verschillende beperkingen op een API,
zoals burst-throttle-tarieven of sustained-throttle-tarieven.
Bijvoorbeeld, je wilt gebruikers wellicht beperken tot maximaal 60 verzoeken per minuut en 1000 verzoeken per dag.

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
## **Throttle-beleidsinstellingen**
Je kunt de standaard throttle-klassen en -tarieven globaal instellen in de `settings.py` van je project door de volgende sleutels te overschrijven:
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
De tariefomschrijvingen die in `THROTTLE_RATES` worden gebruikt, kunnen `second`, `minute`, `hour` of `day` bevatten als throttle-periode.

```python
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import UserRateThrottle

api = NinjaExtraAPI()

@api.get('/users')
@throttle(UserRateThrottle)
def my_throttled_endpoint(request):
    return 'foo'
```

## **Clientidentificatie**
Clients worden geïdentificeerd via de HTTP-header X-Forwarded-For en de WSGI-variabele REMOTE_ADDR.
Dit zijn de unieke identificatoren die worden gebruikt om het client-IP-adres te bepalen voor throttling.
`X-Forwarded-For` heeft voorrang op `REMOTE_ADDR` en wordt zo gebruikt.

#### **Beperken van client-proxy's**
Als je unieke client-IP-adressen strikt wilt identificeren, moet je eerst het aantal applicatie-proxy's dat achter de API draait configureren door de instelling `NUM_PROXIES` in te stellen. Deze instelling moet een geheel getal van nul of groter zijn.
Als deze op een waarde ongelijk aan nul wordt ingesteld, dan wordt, nadat eerst eventuele IP-adressen van applicatie-proxy's zijn uitgesloten, het client-IP geïdentificeerd als het laatste IP-adres in de X-Forwarded-For-header. Als deze op nul wordt ingesteld, wordt de waarde REMOTE_ADDR altijd gebruikt als identificerend IP-adres.
Het is belangrijk te begrijpen dat als je `NUM_PROXIES` configureert, alle clients achter één unieke [Network Address Translation (NAT)](https://en.wikipedia.org/wiki/Network_address_translation)-gateway worden behandeld als één client.

!!! note
    Meer context over hoe de X-Forwarded-For-header werkt en over het identificeren van externe client-IP's is hier te vinden.

## **Cache-instellingen voor het Throttle-model**
Het in django-ninja-extra gebruikte throttle-model maakt gebruik van de Django cache-backend. Het gebruikt de `default`-waarde van [`LocMemCache`]().
Voor meer details kun je terecht bij Django's [cache-documentatie](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache).

Als je de standaard cache die in het throttle-model is gedefinieerd niet wilt gebruiken, is hier een voorbeeld van hoe je een andere cache voor het throttle-model definieert:
```python

from django.core.cache import caches
from ninja_extra.throttling import AnonRateThrottle


class CustomAnonRateThrottle(AnonRateThrottle):
    cache = caches['alternate']
```
## **API-referentie**

## **Anonieme Rate Throttling**
Het model `AnonRateThrottle` wordt gebruikt voor throttle-beperking met het IP-adres van niet-geauthenticeerde gebruikers als sleutel.

Het is geschikt voor het beperken van de snelheid van verzoeken van onbekende bronnen.

De rechten voor een verzoek worden bepaald door:
- De `rate` die is gedefinieerd in de afgeleide klasse
- De scope `anon` die is gedefinieerd in `THROTTLE_RATES` in de `NINJA_EXTRA`-instellingen in `settings.py`.

## **Gebruikers Rate Throttling**
Het model `UserRateThrottle` wordt gebruikt voor throttle-beperking door een sleutel te genereren op basis van de gebruikers-ID of primaire sleutel van geauthenticeerde gebruikers.
Niet-geauthenticeerde verzoeken vallen terug op het IP-adres van het binnenkomende verzoek om een unieke sleutel voor throttle-beperking te genereren.

De rechten voor een verzoek worden bepaald door:
- De `rate` die is gedefinieerd in de afgeleide klasse
- De scope `user` die is gedefinieerd in `THROTTLE_RATES` in de `NINJA_EXTRA`-instellingen in `settings.py`.


Je kunt meerdere gebruikers-throttle-tarieven gebruiken voor het model `UserRateThrottle`, bijvoorbeeld:
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
## **Dynamische Rate Throttling**
Het model `DynamicRateThrottle` wordt gebruikt om zowel geauthenticeerde als niet-geauthenticeerde gebruikers te throttlen op een vergelijkbare manier als `UserRateThrottle`.
De belangrijkste functie is de mogelijkheid om de `scope` dynamisch in te stellen op het moment van gebruik.
Bijvoorbeeld:
We kunnen een scope definiëren in de instellingen.

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
Hier passen we dynamisch het tarief `sustained` en het tarief `burst` toe op respectievelijk `get_users` en `get_user_by_id`.


!!! note "Nieuw in v0.15.8"
    Je kunt alle controller-endpoint-operaties throttlen op het klasseniveau van de controller.

## **Controller Throttling**

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
