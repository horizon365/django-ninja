---
comments: true
---
# Tutorial - Omgaan met inputparameters

## Parameters doorgeven vanuit de query string

Laten we de operatie aanpassen zodat deze een naam uit de URL-query string accepteert. Om dit te doen, voeg je simpelweg een argument `name` toe aan onze functie.

```python
@api.get("/hello")
def hello(request, name):
    return f"Hello {name}"
```

Wanneer we het benoemde argument opgeven, krijgen we de verwachte (HTTP 200) response.

<a href="http://localhost:8000/api/hello?name=you"
target="_blank">localhost:8000/api/hello?name=you</a>:

```json
"Hello you"
```

### Standaardwaarden

Als je de parameter niet opgeeft, wordt een HTTP 422-foutresponse teruggestuurd.

*[HTTP 422]: Unprocessable Entity

<a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a>:

```json
{
  "detail": [
    {
      "loc": ["query", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

We kunnen een standaardwaarde opgeven voor het argument `name`, voor het geval dit niet wordt meegegeven:

```python hl_lines="2"
@api.get("/hello")
def hello(request, name="world"):
    return f"Hello {name}"
```

## Inputtypes

**Django Ninja** gebruikt standaard [Python type hints](https://docs.python.org/3/library/typing.html) om inputtypes te formatteren. Als er geen type wordt opgegeven, wordt een string aangenomen (maar het is best practice om type hints op te geven voor alle argumenten).

Laten we een tweede operatie toevoegen die wat eenvoudige rekenkunde met gehele getallen uitvoert.

```python hl_lines="5-7"
@api.get("/hello")
def hello(request, name: str = "world"):
    return f"Hello {name}"

@api.get("/math")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

<a href="http://localhost:8000/api/math?a=2&b=3"
target="_blank">localhost:8000/api/math?a=2&b=3</a>:

```json
{
  "add": 5,
  "multiply": 6
}
```

## Parameters doorgeven via pad-strings

Je kunt "parameters" in het pad declareren met dezelfde syntaxis als Python-formatstrings.

Elke parameter die in de pad-string wordt gevonden, wordt als argument aan je functie doorgegeven, in plaats van dat deze uit de query string wordt gehaald.

```python hl_lines="1"
@api.get("/math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

Nu openen we de math-operatie via <a href="http://localhost:8000/api/math/2and3"
target="_blank">localhost:8000/api/math/2and3</a>.


## Parameters doorgeven via de request body

We zullen de `hello`-operatie wijzigen zodat deze een HTTP `POST`-request gebruikt en de parameters uit de request body haalt.

Om aan te geven dat parameters uit de request body komen, moeten we een schema declareren.

*[Schema]: Een uitbreiding van een Pydantic "Model"

```python hl_lines="1 5-6 8-10"
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class HelloSchema(Schema):
    name: str = "world"

@api.post("/hello")
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"
```

### Zelfdocumenterende API

Nu zal het openen van <a href="http://localhost:8000/api/hello" target="_blank">localhost:8000/api/hello</a> resulteren in een HTTP 405-foutresponse, omdat we het verzoek aan deze URL moeten wijzigen naar het POST-type.

*[HTTP 405]: Method Not Allowed

Een eenvoudige manier om dit te doen is het gebruik van de Swagger-documentatie die automatisch voor ons wordt aangemaakt, op de standaard-URL "/docs" (toegevoegd aan de root van onze API-URL).

1. Bezoek <a href="http://localhost:8000/api/docs" target="_blank">localhost:8000/api/docs</a> om de operaties te bekijken die we hebben gemaakt
1. Open de operatie `/api/hello`
2. Klik op "Try it out"
3. Pas de request body aan
4. Klik op "Execute"

!!! success

    Ga verder naar het volgende hoofdstuk **[Omgaan met responses](step3.md)**
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
