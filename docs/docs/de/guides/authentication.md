---
comments: true
---
# Authentifizierung

## Einführung

**Django Ninja** stellt mehrere Werkzeuge bereit, mit denen Sie Authentifizierung und Autorisierung einfach, schnell und auf Standardkonforme Weise handhaben können, ohne <a href="https://swagger.io/docs/specification/authentication/" target="_blank">alle Sicherheits-Spezifikationen</a> studieren und lernen zu müssen.

Die Grundidee ist, dass Sie beim Beschreiben einer API-Operation ein Authentifizierungsobjekt definieren können.
```python hl_lines="2 7"
{!./src/tutorial/authentication/code001.py!}
```

In diesem Beispiel kann der Client die Methode `pets` nur aufrufen, wenn er die Django-Session-Authentifizierung verwendet (standardmäßig cookie-basiert), andernfalls wird ein HTTP-401-Fehler zurückgegeben.
Wenn Sie nur Superuser autorisieren möchten, können Sie stattdessen `from ninja.security import django_auth_superuser` verwenden.
## Automatisches OpenAPI-Schema

Hier ist ein Beispiel, bei dem der Client einen Header übergeben muss, um sich zu authentifizieren:

`Authorization: Bearer supersecret`

```python hl_lines="4 5 6 7 10"
{!./src/tutorial/authentication/bearer01.py!}
```

Öffnen Sie nun die Dokumentation unter <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a>.


![Swagger UI Auth](../img/auth-swagger-ui.png)

Wenn Sie nun auf die Schaltfläche **Authorize** klicken, werden Sie aufgefordert, Ihr Authentifizierungs-Token einzugeben.

![Swagger UI Auth](../img/auth-swagger-ui-prompt.png)

Wenn Sie einen Testaufruf durchführen, übergibt jeder Request den Authorization-Header.

## Globale Authentifizierung

Wenn Sie **alle** Methoden Ihrer API schützen möchten, können Sie das Argument `auth` an den Konstruktor von `NinjaAPI` übergeben:


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

Und wenn Sie einzelne der Methoden überschreiben müssen, können Sie dies erneut auf Operationsebene tun, indem Sie das Argument `auth` übergeben. In diesem Beispiel ist die Authentifizierung für die Operation `/token` deaktiviert:
```python hl_lines="19"
{!./src/tutorial/authentication/global01.py!}
```

## Verfügbare Authentifizierungsoptionen

### Benutzerdefinierte Funktion


Das Argument „`auth=`" akzeptiert jedes Callable. **NinjaAPI** wendet die Authentifizierung nur an, wenn das Callable einen Wert zurückgibt, der **truthy** ist (in ein boolesches `True` konvertierbar). Dieser Rückgabewert wird dem Attribut `request.auth` zugewiesen.

```python hl_lines="1 2 3 6"
{!./src/tutorial/authentication/code002.py!}
```


### API-Keys

Einige APIs verwenden API-Keys zur Autorisierung. Ein API-Key ist ein Token, den ein Client bei einem API-Aufruf übergibt, um sich zu identifizieren. Der Key kann im Query-String gesendet werden:
```
GET /something?api_key=abcdef12345
```

Oder als Request-Header:

```
GET /something HTTP/1.1
X-API-Key: abcdef12345
```

Oder als Cookie:

```
GET /something HTTP/1.1
Cookie: X-API-KEY=abcdef12345
```

**Django Ninja** wird mit integrierten Klassen geliefert, die Ihnen bei diesen Situationen helfen.


#### Im Query

```python hl_lines="1 2 5 6 7 8 9 10 11 12"
{!./src/tutorial/authentication/apikey01.py!}
```

In diesem Beispiel holen wir einen Token aus `GET['api_key']` und suchen den entsprechenden `Client` in der Datenbank. Die Client-Instanz wird als Attribut `request.auth` gesetzt.

Hinweis: **`param_name`** ist der Name des GET-Parameters, der geprüft wird. Wenn er nicht gesetzt ist, wird der Standardwert `"key"` verwendet.


#### Im Header

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey02.py!}
```

#### Im Cookie

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey03.py!}
```



### HTTP Bearer

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/bearer01.py!}
```

### HTTP-Basic-Authentifizierung

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/basic01.py!}
```


## Mehrere Authentifikatoren

Das Argument **`auth`** erlaubt Ihnen außerdem, mehrere Authentifikatoren zu übergeben:

```python hl_lines="18"
{!./src/tutorial/authentication/multiple01.py!}
```

In diesem Fall prüft **Django Ninja** zuerst den API-Key aus `GET`, und wenn dieser nicht gesetzt oder ungültig ist, wird der Key aus dem `header` geprüft.
Wenn beide ungültig sind, wird ein Authentifizierungsfehler an die Response ausgelöst.


## Router-Authentifizierung

Verwenden Sie das Argument `auth` an einem Router, um einen Authentifikator auf alle darin deklarierten Operationen anzuwenden:

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

Oder über den Konstruktor des Routers:
```python
router = Router(auth=BasicAuth())
```


## Benutzerdefinierte Ausnahmen

Das Auslösen einer Ausnahme, für die ein Exception-Handler registriert ist, gibt die Response dieses Handlers auf dieselbe Weise wie bei einer Operation zurück:

```python hl_lines="1 4"
{!./src/tutorial/authentication/bearer02.py!}
```


## Asynchrone Authentifizierung

**Django Ninja** bietet grundlegende Unterstützung für asynchrone Authentifizierung. Auch wenn die Standard-Authentifizierungsklassen nicht async-kompatibel sind, können Sie Ihr eigenes asynchrones Authentifizierungs-Callable definieren und es mit `auth` übergeben.

```python
async def async_auth(request):
    ...


@api.get("/pets", auth=async_auth)
def pets(request):
    ...
```


Weitere Informationen finden Sie unter [Fehlerbehandlung](errors.md) .

!!! success

    Fahren Sie mit dem nächsten Abschnitt fort: **[Testen](testing.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
