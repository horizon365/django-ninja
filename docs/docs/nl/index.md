---
title: Django Ninja - Snel REST-framework voor Django
template: home.html
comments: true
---

Django Ninja is een webframework voor het bouwen van API's met Django en Python 3.6+ type-hints.

Belangrijkste functies:

 - **Makkelijk te begrijpen**: Ontworpen om eenvoudig te gebruiken en intuïtief te zijn.
 - **Snelle uitvoering**: Dankzij **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** en **<a href="guides/async-support/">async-ondersteuning</a>** levert het zeer hoge prestaties.
 - **Snel te coderen**: Django Ninja is een webframework voor het bouwen van API's met Django en Python 3.6+ type-hints.
 - **Gebaseerd op standaarden**: Gebaseerd op standaarden: **OpenAPI** (voorheen Swagger) en **JSON Schema**.
 - **Django-vriendelijk**: (uiteraard) integreert het goed met de Django-kern en de ORM.
 - **Productieklaar**: Gebruikt door meerdere bedrijven in echte projecten (als je Django Ninja gebruikt en je feedback wilt delen, mail dan naar ppr.vitaly@gmail.com).

<a href="https://github.com/vitalik/django-ninja-benchmarks" target="_blank">Benchmarks</a>:

![Django Ninja REST Framework](img/benchmark.png)

## Installatie

```
pip install django-ninja
```

## Snel voorbeeld

Start een nieuw Django-project (of gebruik een bestaand)
```
django-admin startproject apidemo
```

In `urls.py`

```python hl_lines="3 5 8 9 10 15"
{!./src/index001.py!}
```

Voer het nu op de gebruikelijke manier uit:
```
./manage.py runserver
```

Let op: je hoeft Django Ninja niet toe te voegen aan je geïnstalleerde apps om het te laten werken.

## Controleer het

Open je browser op <a href="http://127.0.0.1:8000/api/add?a=1&b=2" target="_blank">http://127.0.0.1:8000/api/add?a=1&b=2</a>

Je ziet het JSON-antwoord als:
```JSON
{"result": 3}
```
Je hebt zojuist een API gemaakt die:

 - Een HTTP GET-verzoek ontvangt op `/api/add`
 - De GET-parameters `a` en `b` ontvangt, valideert en omzet naar het juiste type
 - Het resultaat decodeert als JSON
 - Een OpenAPI-schema genereert voor de gedefinieerde operatie

## Interactieve API-documentatie

Ga nu naar <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

Je ziet de automatische, interactieve API-documentatie (aangeboden door <a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a> of <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a>) :

![Swagger UI](img/index-swagger-ui.png)


## Samenvatting

Kortom, je declareert de types van parameters, request-bodies enzovoort slechts **één keer**, als functieargumenten.

Je doet dit met standaard, moderne Python-types.

Je hoeft geen nieuwe syntaxis, de methoden of klassen van een specifieke bibliotheek, enzovoort te leren.

Gewoon standaard **Python 3.6+**.

Bijvoorbeeld, voor een `int`:

```python
a: int
```

Of, voor een complexer `Item`-model:

```python
class Item(Schema):
    foo: str
    bar: float

def operation(a: Item):
    ...
```

...met alleen deze ene declaratie krijg je:

* Ondersteuning in de editor, waaronder:
    * Automatische aanvulling
    * Typecontrole
* Datavalidatie:
    * Automatische en duidelijke foutmeldingen bij ongeldige gegevens
    * Validatie zelfs voor diep geneste JSON-objecten
* <abbr title="Also known as: serialization, parsing, marshalling">Serialisatie</abbr> van netwerkinvoergegevens en conversie naar Python-uitvoergegevens, en het lezen uit:
    * JSON
    * Pad-parameters
    * Query-parameters
    * Cookies
    * Headers
    * Formulieren
    * Bestanden
* Automatische, interactieve API-documentatie

Dit project is sterk geïnspireerd door <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a>.

!!! note

    Bekijk de **[Tutorial](tutorial/index.md)** om snel aan de slag te gaan.

    Het ecosysteem rond Django Ninja:

    1. [django-ninja](index.md): Een framework gebaseerd op Django dat het beste van Django benut en combineert met de kracht van Pydantic — de optimale keuze op het snijpunt van veiligheid en gebruiksgemak.

    2. [django-ninja-crud](django-ninja-crud/index.md): Een framework gebouwd op django-ninja om de ontwikkeling van CRUD-interfaces te vereenvoudigen, met declaratieve model-viewsets en scenario-gebaseerde testmethoden.

    3. [django-ninja-extra](django-ninja-extra/index.md): Een tool waarmee ontwikkelaars de uitgebreide Django-documentatie kunnen overslaan en met minimale code snel krachtige webapplicaties en moderne API-interfaces kunnen bouwen.

    4. [django-ninja-jwt](django-ninja-jwt/index.md): Een JSON Web Token-plugin voor django-ninja die authenticatie en verwante functies implementeert, geforkt van een populaire Django Rest Framework-plugin.
