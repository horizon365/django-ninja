---
comments: true
---
# CSRF (Cross-Site Request Forgery)

## Was ist Cross-Site Request Forgery?
> [Cross-Site Request Forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery) liegt vor, wenn eine bösartige Website einen Link, eine Formularschaltfläche oder JavaScript-Code enthält, der die Anmeldeinformationen eines eingeloggten Benutzers (der die bösartige Website in seinem Browser besucht) dazu verwenden soll, eine Aktion auf Ihrer Website auszuführen (oder an anderen Stellen, die nicht durch dieses Dokument abgedeckt sind).


## Wie man sich mit Django Ninja gegen Cross-Site Request Forgery verteidigt
### Authentifizierungsmethoden verwenden, die nicht automatisch in Anfragen eingebettet sind
Cross-Site-Request-Forgery-Angriffe beruhen auf Authentifizierungsmethoden, die automatisch in Anfragen von anderen Websites eingebettet sind, wie z. B. [Cookies](https://en.wikipedia.org/wiki/HTTP_cookie) oder [Basic Access Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication).
Die Verwendung einer Authentifizierungsmethode, die nicht automatisch eingebettet ist, wie z. B. `Authorization: Bearer`, mildert diesen Angriff ab.


### Den eingebauten Cross-Site-Request-Forgery-Schutz von Django verwenden
Wenn Sie die Standard-Authentifizierung von Django verwenden, die auf Cookies basiert, müssen Sie auch den standardmäßigen [Django-Cross-Site-Request-Forgery-Schutz](https://docs.djangoproject.com/en/4.2/ref/csrf/) verwenden.


Standardmäßig ist der Cross-Site-Request-Forgery-Schutz bei **Django Ninja** für alle Operationen **AUS**geschaltet.
Um ihn einzuschalten, müssen Sie das Argument `csrf` der Klasse NinjaAPI verwenden:

```python hl_lines="3"
from ninja import NinjaAPI

api = NinjaAPI(csrf=True)
```

<span style="color: red;">Warnung</span>: Die Verwendung von Cookie-basierter Authentifizierung mit deaktiviertem Cross-Site-Request-Forgery-Schutz ist unsicher! (z. B. `CookieKey` oder `django_auth`).


**Django Ninja** aktiviert den Cross-Site-Request-Forgery-Schutz automatisch für Cookie-basierte Authentifizierung.


```python hl_lines="8"
from ninja import NinjaAPI
from ninja.security import APIKeyCookie

class CookieAuth(APIKeyCookie):
    def authenticate(self, request, key):
        return key == "test"

api = NinjaAPI(auth=CookieAuth())

```


Oder basierend auf django-auth (das von der Cookie-basierten Authentifizierung erbt):

```python hl_lines="4"
from ninja import NinjaAPI
from ninja.security import django_auth

api = NinjaAPI(auth=django_auth)
```


#### Der Django-Decorator `ensure_csrf_cookie`
Sie können den Django-Decorator [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie) auf einer ungeschützten Route verwenden, damit sie einen `Set-Cookie`-Header für das Cross-Site-Request-Forgery-Token enthält. Beachten Sie:
- Der Routen-Decorator muss vor (d. h. über) dem Decorator [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie) ausgeführt werden.
- Sie müssen diese Route mit `csrf_exempt` versehen.
- Der Decorator `ensure_csrf_cookie` funktioniert nur auf einer Django-`HttpResponse`, nicht auf einem Dictionary wie bei den meisten Django-Ninja-Decorators.
```python hl_lines="4"
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

@api.post("/csrf")
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request):
    return HttpResponse()
```
Eine Anfrage an diese Route löst eine Antwort von Django mit dem entsprechenden `Set-Cookie`-Header aus.


#### Frontend-Code
Sie können die Abschnitte [Verwendung des CSRF-Schutzes mit AJAX](https://docs.djangoproject.com/en/4.2/howto/csrf/#using-csrf-protection-with-ajax) und [Setzen des Tokens auf der AJAX-Anfrage](https://docs.djangoproject.com/en/4.2/howto/csrf/#setting-the-token-on-the-ajax-request) aus [Verwendung des CSRF-Schutzes von Django](https://docs.djangoproject.com/en/4.2/howto/csrf/) lesen, um zu erfahren, wie Sie das Cross-Site-Request-Forgery-Schutz-Token in Ihrem Frontend-Code behandeln.


## Über CORS
Möglicherweise möchten Sie Ihr Frontend und Ihre API auf verschiedenen Sites betreiben (in diesem Fall können Sie sich [django-cors-headers](https://github.com/adamchainz/django-cors-headers) ansehen).
Obwohl nicht direkt mit Cross-Site Request Forgery verwandt, kann CORS (Cross-Origin Resource Sharing) hilfreich sein, wenn Sie Cross-Site-Request-Forgery-Cookies auf einer anderen Site definieren als der vom Frontend verwendeten, da dies standardmäßig von der [Same-Origin-Policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) nicht erlaubt ist.
Dann können Sie sich die [django-cors-headers README](https://github.com/adamchainz/django-cors-headers#readme) ansehen.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
