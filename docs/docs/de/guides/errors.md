---
comments: true
---
# Fehlerbehandlung

**Django Ninja** ermöglicht es Ihnen, benutzerdefinierte Exception-Handler zu installieren, um zu steuern, wie Responses bei Fehlern oder behandelten Ausnahmen zurückgegeben werden.

## Benutzerdefinierte Exception-Handler

Angenommen, Sie bauen eine API, die von einem externen Dienst abhängt, der zu bestimmten Zeitpunkten nicht verfügbar sein soll. Sie können diesen Fehler behandeln und dem Client eine freundliche Response zurückgeben (mit dem Hinweis, es später erneut zu versuchen), anstatt beim Auftreten der Ausnahme den Standard-500-Fehler auszulösen.
Dazu müssen Sie:

 - 1) Eine Ausnahme erstellen (oder eine bestehende verwenden)
 - 2) Den Dekorator api.exception_handler verwenden


Beispiel:


```python hl_lines="9 10"
api = NinjaAPI()

class ServiceUnavailableError(Exception):
    pass


# initializing handler

@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=503,
    )


# some logic that throws exception

@api.get("/service")
def some_operation(request):
    if random.choice([True, False]):
        raise ServiceUnavailableError()
    return {"message": "Hello"}

```

Die Exception-Handler-Funktion nimmt 2 Argumente entgegen:

 - **request** – der HTTP-Request von Django
 - **exc** – die eigentliche Ausnahme

Die Funktion muss eine HTTP-Response zurückgeben

## Standard-Exception-Handler überschreiben

Standardmäßig initialisiert **Django Ninja** die folgenden Exception-Handler:


#### `ninja.errors.AuthenticationError`

Wird ausgelöst, wenn die Authentifizierungsdaten ungültig sind

#### `ninja.errors.ValidationError`

Wird ausgelöst, wenn die Request-Daten die Validierung nicht bestehen

#### `ninja.errors.HttpError`

Wird verwendet, um von beliebiger Stelle im Code aus einen HTTP-Fehler mit einem Statuscode auszulösen
#### `django.http.Http404`
 
Die Standard-404-Ausnahme von Django (kann zum Beispiel mit get_object_or_404 zurückgegeben werden)
#### `Exception`
 
Jede andere Ausnahme, die von der Anwendung nicht behandelt wird.
Standardverhalten
 
  - **Wenn `settings.DEBUG` auf `True` steht** – gibt einen Traceback als reinen Text zurück (nützlich beim Debuggen in der Konsole oder in der Swagger UI)
  - **sonst** – verwendet den Standardmechanismus von Django zur Ausnahmebehandlung (Fehler-Logging, Senden von E-Mails an ADMINS)


### Standard-Handler überschreiben

Wenn Sie die Standardausgabe von Validierungsfehlern ändern möchten – überschreiben Sie den Exception-Handler für ValidationError:

```python hl_lines="1 4"
from ninja.errors import ValidationError
...

@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return HttpResponse("Invalid input", status=422)
```


## HTTP-Responses über Ausnahmen auslösen

Als Alternative zum Erstellen einer benutzerdefinierten Ausnahme und zum Schreiben eines Handlers dafür – können Sie auch eine HTTP-Ausnahme auslösen, was dazu führt, dass eine HTTP-Response mit dem gewünschten Code zurückgegeben wird

```python
from ninja.errors import HttpError

@api.get("/some/resource")
def some_operation(request):
    if True:
        raise HttpError(503, "Service Unavailable. Please retry later.")

```
!!! success

    Fahren Sie mit dem nächsten Abschnitt fort: **[URLs reversen](urls.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
