---
comments: true
---
# Willkommen bei Django Ninja 1.0


Um loszulegen, installieren Sie die neueste Version mit dem folgenden Befehl:
```
pip install -U django-ninja
```

django-ninja v1 ist kompatibel mit Python 3.7 und höher.


Die Django-Ninja-0.x-Serie wird weiterhin unterstützt, erhält aber nur noch Sicherheitsupdates und kritische Bugfixes.


✨ Was ist neu in Django Ninja 1.0

## Pydantic2-Unterstützung

Pydantic Version 2 wurde in Rust neu geschrieben und enthält viele Verbesserungen und Funktionen, wie z. B.:

 - Sicherere Typen.
 - Bessere Erweiterbarkeit.
 - Bessere Performance.

Laut unseren Tests kann ein durchschnittliches Projekt eine durchschnittliche Performance-Verbesserung von etwa 10 % erzielen, während Sie in bestimmten Randfällen beim Parsen/Serialisieren eine 4-fache Beschleunigung erreichen können.
Andererseits führt es breaking changes ein — pydantic 1 und 2 sind nicht vollständig kompatibel — aber wir haben versucht, diesen Übergang so einfach wie möglich zu gestalten.
Wenn Sie also die Klasse `Schema` verwendet haben, sollte die Migration auf ninja v1 unkompliziert sein. Andernfalls folgen Sie bitte dem [pydantic-Migrationsleitfaden](https://pydantic.com.cn/migration/)


Einige neue Funktionen, die pydantic2 bietet

### pydantic-Kontext

Pydantic unterstützt nun einen Kontext während der Validierung und Serialisierung, und Django Ninja reicht das „request"-Objekt bei der Verarbeitung von Anfragen und Responses durch.
```Python hl_lines="6 7"
class Payload(Schema):
    id: int
    name: str
    request_path: str

    @staticmethod
    def resolve_request_path(data, context):
        request = context["request"]
        return request.get_full_path()

```

Während der Response-Phase wird außerdem „response_code" an den Kontext übergeben.

## Schema.Meta

Pydantic hat die Klasse BaseModel.Config inzwischen als veraltet markiert. Um jedoch konsistent mit allen anderen Django-Teilen zu bleiben, haben wir eine Klasse „Meta" für ModelSchema eingeführt — sie funktioniert ähnlich wie Djangos ModelForms:
```Python hl_lines="2 4"
class TxItem(ModelSchema):
    class Meta:
        model = Transaction
        fields = ["id", "account", "amount", "timestamp"]

```

(Die Klasse „Config" wird weiterhin unterstützt, ist aber jetzt veraltet)


## Kürzere/sauberere Parametersyntax

```python
@api.post('/some')
def some_form(request, username: Form[str], password: Form[str]):
    return True
```

statt

```python
@api.post('/some')
def some_form(request, username: str = Form(...), password: str = Form(...)):
    return True
```

oder

```python
@api.post('/some')
def some_form(request, data: Form[AuthSchema]):
    return True
```


statt

```python
@api.post('/some')
def some_form(request, data: AuthSchema = Form(...)):
    return True
```



sowie alle Autovervollständigungs-Funktionen in Ihrem Editor.


Andererseits **wird die alte Syntax weiterhin unterstützt**, sodass Sie Ihr Projekt mühelos auf die neueste django-ninja-Version portieren können.


#### + Annotated

typing.Annotated wird nun ebenfalls unterstützt:

```Python
@api.get("/annotated")
def annotated(request, data: Annotated[SomeData, Form()]):
    return {"data": data.dict()}

```


## Async-Auth-Unterstützung

Asynchrone Authentifikatoren werden endlich unterstützt. Alles, was Sie tun müssen, ist, `async` zu Ihrer Methode `authenticate` hinzuzufügen:

```Python
class Auth(HttpBearer):
    async def authenticate(self, request, token):
        await asyncio.sleep(1)
        if token == "secret":
            return token

```


## Geändertes CSRF-Verhalten


`csrf=True` ist nicht mehr erforderlich, wenn Sie Cookie-basierte Authentifizierung verwenden. Stattdessen wird der CSRF-Schutz automatisch aktiviert. Dies ermöglicht es Ihnen auch, CSRF-geschützte Authentifikatoren mit anderen Methoden zu mischen, die keine Cookies benötigen:

```Python
api = NinjaAPI(auth=[django_auth, Auth()])
```


## Dokumentation

Der Dokumentations-Viewer ist jetzt konfigurierbar und austauschbar. Standardmäßig wird django-ninja mit Swagger und Redoc ausgeliefert:
```Python
from ninja import NinjaAPI, Redoc, Swagger


# use redoc
api = NinjaAPI(docs=Redoc()))

# use swagger:
api = NinjaAPI(docs=Swagger())

# set configuration for swagger:
api = NinjaAPI(docs=Swagger({"persistAuthorization": True}))
```

Benutzer können jetzt eigene Dokumentations-Viewer erstellen, indem sie die Klasse `DocsBase` ableiten.

## Router

add_router unterstützt String-Pfade:

```Python
api = NinjaAPI()


api.add_router('/app1', 'myproject.app1.router')
api.add_router('/app2', 'myproject.app2.router')
api.add_router('/app3', 'myproject.app3.router')
api.add_router('/app4', 'myproject.app4.router')
api.add_router('/app5', 'myproject.app5.router')
```


## Decorators

Wenn django-ninja eine View mit .get/.post usw. dekoriert, umhüllt es das Ergebnis der Funktion (in den meisten Fällen keine HttpResponse — sondern ein serialisierbares Objekt), daher funktioniert es wahrscheinlich nicht mit einigen eingebauten oder Third-Party-Decorators, wie zum Beispiel:
```python hl_lines="4"
from django.views.decorators.cache import cache_page

@api.get("/test")
@cache_page(5) # <----- will not work!
def test_view(request):
    return {"some": "Complex data"}
```
Dieses Beispiel funktioniert nicht.

Jetzt führt django-ninja einen Decorator decorate_view ein, der das Injizieren von Decorators ermöglicht, die mit HTTP-Responses arbeiten:
```python hl_lines="1 4"
from ninja.decorators import decorate_view

@api.get("/test")
@decorate_view(cache_page(5))
def test_view(request):
    return str(datetime.now())
```


## Pagination

Die Methode `paginate_queryset` akzeptiert nun das `request`-Objekt


#### Nicht rückwärtskompatible Punkte
 - resolve_xxx(self, ...) - die Unterstützung der Auflösung mit (self) ist veraltet und wird durch pydantics eingebaute Funktionalität ersetzt.
 - pydantic v1 wird nicht mehr unterstützt
 - python 3.6 wird nicht mehr unterstützt

Übrigens — wenn Ihnen dieses Projekt gefällt und Sie noch keinen GitHub-Stern vergeben haben, dann tun Sie es bitte! [GitHub-Stern](img/github-star.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
