---
comments: true
---
# Authenticatie

## Introductie

**Django Ninja** biedt verschillende tools om je te helpen authenticatie en autorisatie eenvoudig, snel en op een standaard manier af te handelen, zonder dat je <a href="https://swagger.io/docs/specification/authentication/" target="_blank">alle securityspecificaties</a> hoeft te bestuderen en te leren.

De kerngedachte is dat je, wanneer je een API-operatie beschrijft, een authenticatieobject kunt definiëren.
```python hl_lines="2 7"
{!./src/tutorial/authentication/code001.py!}
```

In dit voorbeeld kan de client de methode `pets` alleen aanroepen als deze Django session authenticatie gebruikt (standaard cookie-gebaseerd), anders wordt er een HTTP-401 fout teruggegeven.
Als je alleen superusers wilt autoriseren, kun je in plaats daarvan `from ninja.security import django_auth_superuser` gebruiken.
## Automatisch OpenAPI schema

Hier is een voorbeeld waarin de client een header moet meesturen om te authenticeren:

`Authorization: Bearer supersecret`

```python hl_lines="4 5 6 7 10"
{!./src/tutorial/authentication/bearer01.py!}
```

Ga nu naar de <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a> documentatie.


![Swagger UI Auth](../img/auth-swagger-ui.png)

Wanneer je nu op de knop **Authorize** klikt, wordt je gevraagd je authenticatie token in te voeren.

![Swagger UI Auth](../img/auth-swagger-ui-prompt.png)

Wanneer je een testoproep doet, zal elk verzoek de autorisatieheader meesturen.

## Globale authenticatie

Als je **alle** methoden van je API wilt beveiligen, kun je het argument `auth` doorgeven aan de constructor van `NinjaAPI`:


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

En als je sommige methoden wilt overriden, kun je dat opnieuw doen op het niveau van de operatie door het argument `auth` door te geven. In dit voorbeeld is authenticatie uitgeschakeld voor de operatie `/token`:
```python hl_lines="19"
{!./src/tutorial/authentication/global01.py!}
```

## Beschikbare authenticatieopties

### Aangepaste functie


Het argument "`auth=`" accepteert elke callable. **NinjaAPI** past alleen authenticatie toe wanneer de callable een waarde teruggeeft die **truthy** is (converteert naar een boolean `True`). Deze retourwaarde wordt toegewezen aan het attribuut `request.auth`.

```python hl_lines="1 2 3 6"
{!./src/tutorial/authentication/code002.py!}
```


### API keys

Sommige API's gebruiken API keys voor autorisatie. Een API key is een token die een client meestuurt bij het aanroepen van de API om zich te identificeren. De key kan worden verstuurd in de query string:
```
GET /something?api_key=abcdef12345
```

Of als request header:

```
GET /something HTTP/1.1
X-API-Key: abcdef12345
```

Of als cookie:

```
GET /something HTTP/1.1
Cookie: X-API-KEY=abcdef12345
```

**Django Ninja** wordt geleverd met ingebouwde classes om je te helpen deze situaties af te handelen.


#### In Query

```python hl_lines="1 2 5 6 7 8 9 10 11 12"
{!./src/tutorial/authentication/apikey01.py!}
```

In dit voorbeeld halen we een token uit `GET['api_key']` en zoeken we de bijbehorende `Client` in de database. De Client instantie wordt ingesteld als het attribuut `request.auth`.

Let op: **`param_name`** is de naam van de GET-parameter die wordt gecontroleerd. Als deze niet is ingesteld, wordt standaard `"key"` gebruikt.


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

### HTTP Basic authenticatie

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/basic01.py!}
```


## Meerdere authenticators

Met het argument **`auth`** kun je ook meerdere authenticators doorgeven:

```python hl_lines="18"
{!./src/tutorial/authentication/multiple01.py!}
```

In dit geval controleert **Django Ninja** eerst de API key uit `GET`, en als die niet is ingesteld of ongeldig is, controleert het de `header` key.
Als beide ongeldig zijn, wordt er een authenticatiefout in de response gegooid.


## Router authenticatie

Gebruik het argument `auth` op een router om een authenticator toe te passen op alle operaties die erin worden gedeclareerd:

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

Of via de constructor van de router:
```python
router = Router(auth=BasicAuth())
```


## Aangepaste exceptions

Het gooien van een exception die een exception handler heeft, geeft de response van die handler terug op dezelfde manier als bij een operatie:

```python hl_lines="1 4"
{!./src/tutorial/authentication/bearer02.py!}
```


## Async authenticatie

**Django Ninja** heeft basisondersteuning voor asynchrone authenticatie. Hoewel de standaard authenticatie classes niet async-compatibel zijn, kun je je eigen asynchrone authenticatie-callable definiëren en deze met `auth` doorgeven.

```python
async def async_auth(request):
    ...


@api.get("/pets", auth=async_auth)
def pets(request):
    ...
```


Voor meer informatie, zie [Foutafhandeling](errors.md) .

!!! success

    Ga verder naar de volgende sectie **[Testen](testing.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
