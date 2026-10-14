---
comments: true
---
# CSRF (Cross-Site Request Forgery)

## Qu'est-ce que la falsification de requête intersites ?
> La [falsification de requête intersites](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (cross-site request forgery) se produit lorsqu'un site malveillant contient un lien, un bouton de formulaire ou du code JavaScript destiné à utiliser les identifiants d'un utilisateur connecté (qui visite le site malveillant dans son navigateur) pour effectuer une action sur votre site web (ou ailleurs, ce que ce document ne couvre pas).


## Comment se défendre contre la falsification de requête intersites avec Django Ninja
### Utiliser des méthodes d'authentification qui ne sont pas intégrées automatiquement dans les requêtes
Les attaques par falsification de requête intersites s'appuient sur des méthodes d'authentification qui sont incluses automatiquement dans les requêtes provenant d'autres sites web, comme les [cookies](https://en.wikipedia.org/wiki/HTTP_cookie) ou l'[authentification basique](https://en.wikipedia.org/wiki/Basic_access_authentication).
Utiliser une méthode d'authentification qui n'est pas intégrée automatiquement, comme `Authorization: Bearer`, atténue cette attaque.


### Utiliser la protection intégrée de Django contre la falsification de requête intersites
Si vous utilisez l'authentification par défaut de Django, qui repose sur les cookies, vous devez également utiliser la [protection de Django contre la falsification de requête intersites](https://docs.djangoproject.com/en/4.2/ref/csrf/) par défaut.


Par défaut, **Django Ninja** a la protection contre la falsification de requête intersites désactivée (**OFF**) pour toutes les opérations.
Pour l'activer, vous devez utiliser l'argument `csrf` de la classe NinjaAPI :

```python hl_lines="3"
from ninja import NinjaAPI

api = NinjaAPI(csrf=True)
```

<span style="color: red;">Avertissement</span> : utiliser une authentification basée sur les cookies avec la protection contre la falsification de requête intersites désactivée n'est pas sécurisé ! (par ex. `CookieKey`, ou `django_auth`).


**Django Ninja** activera automatiquement la protection contre la falsification de requête intersites pour l'authentification basée sur les cookies.


```python hl_lines="8"
from ninja import NinjaAPI
from ninja.security import APIKeyCookie

class CookieAuth(APIKeyCookie):
    def authenticate(self, request, key):
        return key == "test"

api = NinjaAPI(auth=CookieAuth())

```


Ou basée sur django-auth (qui hérite de l'authentification basée sur les cookies) :

```python hl_lines="4"
from ninja import NinjaAPI
from ninja.security import django_auth

api = NinjaAPI(auth=django_auth)
```


#### Le décorateur Django `ensure_csrf_cookie`
Vous pouvez utiliser le décorateur Django [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie) sur une route non protégée pour lui faire inclure un en-tête `Set-Cookie` portant le jeton de protection contre la falsification de requête intersites. Notez que :
- Le décorateur de route doit s'exécuter avant (c'est-à-dire au-dessus) du décorateur [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie).
- Vous devez appliquer `csrf_exempt` à cette route.
- Le décorateur `ensure_csrf_cookie` ne fonctionne que sur une `HttpResponse` de Django, et non sur un dictionnaire comme le font la plupart des décorateurs de Django Ninja.
```python hl_lines="4"
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

@api.post("/csrf")
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request):
    return HttpResponse()
```
Une requête vers cette route déclenchera une réponse de Django avec l'en-tête `Set-Cookie` approprié.


#### Code front-end
Vous pouvez consulter les sections [Using CSRF protection with AJAX](https://docs.djangoproject.com/en/4.2/howto/csrf/#using-csrf-protection-with-ajax) et [Setting the token on the AJAX request](https://docs.djangoproject.com/en/4.2/howto/csrf/#setting-the-token-on-the-ajax-request) de [How to use Django's CSRF protection](https://docs.djangoproject.com/en/4.2/howto/csrf/) pour apprendre à gérer le jeton de protection contre la falsification de requête intersites dans votre code front-end.


## À propos de CORS
Vous souhaiterez peut-être héberger votre front-end et votre API sur des sites différents (auquel cas vous pouvez consulter [django-cors-headers](https://github.com/adamchainz/django-cors-headers)).
Bien que cela ne soit pas directement lié à la falsification de requête intersites, CORS (Cross-Origin Resource Sharing) peut être utile lorsque vous définissez des cookies de protection contre la falsification de requête intersites sur un site différent de celui utilisé par le front-end, car cela n'est pas autorisé par défaut par la [même origine (same-origin policy)](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy).
Vous pouvez alors consulter le [README de django-cors-headers](https://github.com/adamchainz/django-cors-headers#readme).

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
