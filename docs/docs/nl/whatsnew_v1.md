---
comments: true
---
# Welkom bij Django Ninja 1.0


Om te beginnen, installeer je de nieuwste versie met het volgende commando:
```
pip install -U django-ninja
```

django-ninja v1 is compatibel met Python 3.7 en hoger.


De Django Ninja 0.x-serie wordt nog steeds ondersteund, maar ontvangt alleen nog beveiligingsupdates en kritieke bugfixes.


✨ Wat is er nieuw in Django Ninja 1.0

## Pydantic2-ondersteuning

Pydantic versie 2 is herschreven in Rust en bevat veel verbeteringen en functies, zoals:

 - Veiligere types.
 - Betere uitbreidbaarheid.
 - Betere prestaties.

Volgens onze tests kan een gemiddeld project ongeveer 10% prestatieverbetering behalen, terwijl je in sommige randgevallen van parsing/serialisatie tot 4 keer sneller kunt zijn.
Aan de andere kant introduceert het brekende wijzigingen — pydantic 1 en 2 zijn niet volledig compatibel — maar we hebben geprobeerd deze overgang zo eenvoudig mogelijk te maken.
Dus als je de 'Schema'-klasse gebruikte, zou de migratie naar ninja v1 eenvoudig moeten verlopen. Anders kun je de [pydantic migration guide](https://pydantic.com.cn/migration/) volgen


Enkele nieuwe functies die pydantic2 biedt

### pydantic context

Pydantic ondersteunt nu context tijdens validatie en serialisatie, en Django Ninja geeft het "request"-object door tijdens het verwerken van requests en responses.
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

Tijdens de response-fase wordt ook "response_code" aan de context doorgegeven.

## Schema.Meta

Pydantic heeft de klasse BaseModel.Config inmiddels afgekeurd. Om echter consistent te blijven met alle andere Django-onderdelen, hebben we een "Meta"-klasse geïntroduceerd voor ModelSchema — deze werkt vergelijkbaar met Django's ModelForms:
```Python hl_lines="2 4"
class TxItem(ModelSchema):
    class Meta:
        model = Transaction
        fields = ["id", "account", "amount", "timestamp"]

```

(De "Config"-klasse wordt nog steeds ondersteund, maar is inmiddels afgekeurd)


## Kortere/nettere parametersyntaxis

```python
@api.post('/some')
def some_form(request, username: Form[str], password: Form[str]):
    return True
```

in plaats van

```python
@api.post('/some')
def some_form(request, username: str = Form(...), password: str = Form(...)):
    return True
```

of

```python
@api.post('/some')
def some_form(request, data: Form[AuthSchema]):
    return True
```


in plaats van

```python
@api.post('/some')
def some_form(request, data: AuthSchema = Form(...)):
    return True
```



evenals alle functies voor automatische aanvulling in je editor.


Aan de andere kant, **de oude syntaxis wordt nog steeds ondersteund**, dus je kunt je moeiteloos project naar de nieuwste django-ninja-versie overzetten.


#### + Annotated

typing.Annotated wordt ook nu ondersteund:

```Python
@api.get("/annotated")
def annotated(request, data: Annotated[SomeData, Form()]):
    return {"data": data.dict()}

```


## Ondersteuning voor async auth

Async-authenticatoren worden eindelijk ondersteund. Het enige dat je hoeft te doen, is `async` toevoegen aan je `authenticate`-methode:

```Python
class Auth(HttpBearer):
    async def authenticate(self, request, token):
        await asyncio.sleep(1)
        if token == "secret":
            return token

```


## Gewijzigd CSRF-gedrag


`csrf=True` is niet langer vereist als je cookie-gebaseerde authenticatie gebruikt. In plaats daarvan wordt CSRF-bescherming automatisch ingeschakeld. Hiermee kun je ook CSRF-beschermde authenticatoren combineren met andere methoden die geen cookies vereisen:

```Python
api = NinjaAPI(auth=[django_auth, Auth()])
```


## Documentatie

De documentatieweergave is nu configureerbaar en pluggable. Standaard wordt django-ninja geleverd met Swagger en Redoc:
```Python
from ninja import NinjaAPI, Redoc, Swagger


# use redoc
api = NinjaAPI(docs=Redoc()))

# use swagger:
api = NinjaAPI(docs=Swagger())

# set configuration for swagger:
api = NinjaAPI(docs=Swagger({"persistAuthorization": True}))
```

Gebruikers kunnen nu aangepaste documentatieweergaven maken door een subklasse van de klasse `DocsBase` te maken.

## Router

add_router ondersteunt string-paden:

```Python
api = NinjaAPI()


api.add_router('/app1', 'myproject.app1.router')
api.add_router('/app2', 'myproject.app2.router')
api.add_router('/app3', 'myproject.app3.router')
api.add_router('/app4', 'myproject.app4.router')
api.add_router('/app5', 'myproject.app5.router')
```


## Decorators

Wanneer django-ninja een view decoreert met .get/.post enz., wikkelt het het resultaat van de functie (in de meeste gevallen geen HttpResponse - maar een serialiseerbaar object), dus het is onwaarschijnlijk dat het werkt met sommige ingebouwde of externe decorators, zoals:
```python hl_lines="4"
from django.views.decorators.cache import cache_page

@api.get("/test")
@cache_page(5) # <----- will not work!
def test_view(request):
    return {"some": "Complex data"}
```
Dit voorbeeld zal niet werken.

Nu introduceert django-ninja een decorate_view-decorator die het mogelijk maakt decorators te injecteren die met http-responses werken:
```python hl_lines="1 4"
from ninja.decorators import decorate_view

@api.get("/test")
@decorate_view(cache_page(5))
def test_view(request):
    return str(datetime.now())
```


## Paginering

De methode `paginate_queryset` accepteert nu het `request`-object


#### Achterwaarts-incompatibele items
 - resolve_xxx(self, ...) - ondersteuning voor (self)-resolutie is afgekeurd ten gunste van de ingebouwde functionaliteit van pydantic.
 - pydantic v1 wordt niet langer ondersteund
 - python 3.6 wordt niet langer ondersteund

Terzijde - als je dit project waardeert en er nog geen GitHub-ster aan hebt gegeven - doe dat dan! [github star](img/github-star.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
