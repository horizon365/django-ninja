---
comments: true
---
## Einführung
Von JWT hatte ich schon lange gehört, es aber nie tatsächlich verwendet. Kürzlich habe ich mich beim Studium des tus-Protokolls für fortsetzbare Uploads (Resumable Upload) bis auf die Ebene der HTTP-Hooks vorgearbeitet, mit dem Ziel, beim Datei-Upload eine Authentifizierung durchzuführen. Natürlich dachte ich dabei an das Paket `django-ninja-jwt`. Ich dachte, es müsste einfach sein, aber nach der Lektüre der [chinesischen Dokumentation](https://django-ninja.cn/django-ninja-jwt/) stellte ich fest, dass es nicht nur einfach war — es war in einem erstaunlichen Maße aufs Wesentliche reduziert.

## Erste Schritte

Laut dem Leitfaden müssen Sie nur `dango-ninja-jwt` und `django-ninja-extra` installieren und dann `NinjaAPI` durch `njaExtraAPI` ersetzen, und das genügt in einer einzigen Zeile.

```python
api.register_controllers(NinjaJWTDefaultController)
```

Ehrlich gesagt ist das schon etwas verwirrend.

Moment — schauen wir uns zuerst die Doku an. Es erscheinen drei neue Endpunkte: `pair`, `refresh` und `verify`.
![JWT swagger UI token](../img/jwt-token.png)
Beachten Sie das Schloss-Symbol in der oberen rechten Ecke — es wird später noch nützlich sein. Es erscheint nur, wenn Sie die Funktion `JWTAuth` verwenden.

### pair
Der erste ist der `pair`-Endpunkt. Das bedeutet: Nachdem Sie Benutzername und Passwort angegeben haben, werden Authentifizierungs-Tokens und Refresh-Tokens zurückgegeben.
Das Format des Request-Bodys sieht wie folgt aus:
```json
{
  "password": "string",
  "username": "string"
}
```
Hinweis: Hier steht `username` unten, was sich etwas davon unterscheidet, was man vielleicht annehmen würde.
Nach einem Klick auf „Execute" erhalten Sie etwa Folgendes:
```json
{
  "data": {
    "username": "lyq",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzE0NzU2NCwiaWF0IjoxNzQyNTQyNzY0LCJqdGkiOiI4MTZmMzg2YWYwNmY0NmVhOWY1YzlkMDJjYzQxZjFkOCIsInVzZXJfaWQiOjF9.G-mTefGtP-cTXWVrxAsqXGGKnZ1442jw67ilvTY5gcQ",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNjI5MTY0LCJpYXQiOjE3NDI1NDI3NjQsImp0aSI6IjdiMGY1Y2Y5NTVlZDRiMzQ5M2M3MmY4NzJmNDdkMzUxIiwidXNlcl9pZCI6MX0.JO9PxVA-rX6TPo9Db00eOuOorThjgX3nTjBT-CuOh90"
  }
}
```
### refresh
Der obige `access`-Token kann zur Authentifizierung verwendet werden, hat aber standardmäßig eine begrenzte Lebensdauer. Der `refresh`-Token hat eine längere Lebensdauer als `access` und wird verwendet, um einen neuen `access`-Token zu erhalten, nachdem der vorherige abgelaufen ist.
Nach dem Aktualisieren wird der vorherige `access`-Token ungültig.

Zu diesem Zeitpunkt können Sie den `access`-Token in das Schloss-Symbol in der oberen rechten Ecke kopieren. Auf diese Weise kann jeder Endpunkt auf der aktuellen Seite ihn verwenden, was das Debuggen erleichtert.
### verify
Sie können zum dritten Endpunkt, `verify`, gehen, um zu prüfen, ob der `access`-Token gültig ist.

Insgesamt baut Ihnen `django-ninja-jwt` also einfach drei Endpunkte, sodass es bequem ist, Tokens zu erhalten, zu aktualisieren und zu testen.

## Anpassung
Diese drei Endpunkte allein reichen nicht aus — zumindest müssen wir unsere eigenen, spezifischen Endpunkte authentifizieren.
Was Sie hier benötigen, ist `JWTAuth`; erst nach dessen Verwendung erscheint das Schloss-Symbol.
```python
from ninja_jwt.authentication import JWTAuth
@route.get('/some', auth=JWTAuth())
def some_endpoint(request):
    """Convenient for showing the auth button on the docs page"""
    return request.auth.username
```
Und beim Endpunkt `some` gibt es ebenfalls ein eigenständiges Schloss-Symbol.
![JWT swagger UI token custom](../img/jwt-token-custom.png)
Für den obigen Endpunkt `some` gilt: Wenn die Authentifizierung erfolgreich ist, antwortet er mit dem Benutzernamen des aktuell angemeldeten Benutzers. Schlägt sie fehl, wird eine 401-Antwort zurückgegeben.
Backend-Entwickler müssen dem Frontend-Team mitteilen, dass es diesen Wert mitsenden soll — lassen Sie es zum Abschnitt [pair](#pair) gehen, um ihn zu erhalten, und regelmäßig zu [refresh](#refresh), um ihn zu aktualisieren.

### Die Token-Lebensdauer konfigurieren

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Access token lifetime
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh token lifetime
    'AUTH_HEADER_TYPES': ('Bearer',),
}

```
### Weitere Anpassungen
Wenn `@route.get('/some', auth=JWTAuth())` in Ihrer Ninja-Route Ihren Anforderungen nicht genügt, können Sie `authenticate` innerhalb der Funktion aufrufen.

```python
@route.get('/some')
def some_endpoint(request):
    auth = JWTAuth()
    # If it fails, a 401 is raised internally
    if auth.authenticate(request, token):
        return request.auth.username

```
Der obige `token` muss von Ihnen selbst aus dem `request`-Objekt extrahiert werden.
