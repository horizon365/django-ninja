---
comments: true
---
# CSRF (Cross-Site Request Forgery)

## Wat is cross-site request forgery?
> [Cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery) doet zich voor wanneer een kwaadwillende website een link, een formulierknop of JavaScript bevat dat is bedoeld om de inloggegevens van een ingelogde gebruiker (die de kwaadwillende website in zijn browser bezoekt) te gebruiken om een actie op jouw website uit te voeren (of op andere locaties die niet door dit document worden gedekt).


## Hoe je je met Django Ninja verdedigt tegen cross-site request forgery
### Gebruik authenticatiemethoden die niet automatisch in requests worden meegestuurd
Cross-site request forgery-aanvallen zijn afhankelijk van authenticatiemethoden die automatisch worden meegestuurd in requests afkomstig van andere websites, zoals [cookies](https://en.wikipedia.org/wiki/HTTP_cookie) of [Basic access authentication](https://en.wikipedia.org/wiki/Basic_access_authentication).
Het gebruik van een authenticatiemethode die niet automatisch wordt meegestuurd, zoals `Authorization: Bearer`, beperkt deze aanval.


### Gebruik de ingebouwde bescherming tegen cross-site request forgery van Django
Als je de standaard Django-authenticatie gebruikt, die cookies gebruikt, moet je ook de standaard [Django cross-site request forgery-bescherming](https://docs.djangoproject.com/en/4.2/ref/csrf/) gebruiken.


Standaard staat de bescherming tegen cross-site request forgery bij **Django Ninja** **UIT** voor alle operaties.
Om deze aan te zetten, moet je het argument `csrf` van de NinjaAPI-klasse gebruiken:

```python hl_lines="3"
from ninja import NinjaAPI

api = NinjaAPI(csrf=True)
```

<span style="color: red;">Warning</span>: Het gebruik van cookie-gebaseerde authenticatie met cross-site request forgery uitgeschakeld is onveilig! (bijv. `CookieKey`, of `django_auth`).


**Django Ninja** zet cross-site request forgery-bescherming automatisch aan voor cookie-gebaseerde authenticatie.


```python hl_lines="8"
from ninja import NinjaAPI
from ninja.security import APIKeyCookie

class CookieAuth(APIKeyCookie):
    def authenticate(self, request, key):
        return key == "test"

api = NinjaAPI(auth=CookieAuth())

```


Of op basis van django-auth (dat overerft van cookie-gebaseerde authenticatie):

```python hl_lines="4"
from ninja import NinjaAPI
from ninja.security import django_auth

api = NinjaAPI(auth=django_auth)
```


#### De Django `ensure_csrf_cookie`-decorator
Je kunt de Django [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie)-decorator gebruiken op een onbeveiligde route om deze een `Set-Cookie`-header laten meesturen voor het cross-site request forgery-token. Let daarbij op:
- De route-decorator moet vóór (dus boven) de [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie)-decorator worden uitgevoerd.
- Je moet die route `csrf_exempt` maken.
- De `ensure_csrf_cookie`-decorator werkt alleen op een Django `HttpResponse`, niet op een dictionary zoals bij de meeste Django Ninja-decorators het geval is.
```python hl_lines="4"
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

@api.post("/csrf")
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request):
    return HttpResponse()
```
Een request naar deze route zorgt ervoor dat Django reageert met de juiste `Set-Cookie`-header.


#### Front-end code
Je kunt de secties [Using CSRF protection with AJAX](https://docs.djangoproject.com/en/4.2/howto/csrf/#using-csrf-protection-with-ajax) en [Setting the token on the AJAX request](https://docs.djangoproject.com/en/4.2/howto/csrf/#setting-the-token-on-the-ajax-request) van [How to use Django's CSRF protection](https://docs.djangoproject.com/en/4.2/howto/csrf/) raadplegen om te leren hoe je het cross-site request forgery-beschermingstoken in je front-end code verwerkt.


## Over CORS
Mogelijk wil je je front-end en API op verschillende sites onderbrengen (in dat geval kun je [django-cors-headers](https://github.com/adamchainz/django-cors-headers) bekijken).
Hoewel dit niet direct gerelateerd is aan cross-site request forgery, kan CORS (Cross-Origin Resource Sharing) nuttig zijn wanneer je cross-site request forgery-cookies op een andere site definieert dan de site die de front-end gebruikt, omdat dit standaard niet is toegestaan volgens het [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy).
Vervolgens kun je de [django-cors-headers README](https://github.com/adamchainz/django-cors-headers#readme) bekijken.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
