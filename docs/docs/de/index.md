---
title: Django Ninja - Schnelles Django REST Framework
template: home.html
comments: true
---

Django Ninja ist ein Webframework zum Erstellen von APIs mit Django und Python 3.6+ Type Hints.

Hauptmerkmale:

 - **Leicht verständlich**: Entworfen für einfache Bedienung und Intuitivität.
 - **Schnelle Ausführung**: Dank **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** und **<a href="guides/async-support/">Async-Unterstützung</a>** bietet es sehr hohe Performance.
 - **Schnell im Schreiben von Code**: Django Ninja ist ein Webframework zum Erstellen von APIs mit Django und Python 3.6+ Type Hints.
 - **Standardbasiert**: Basiert auf Standards: **OpenAPI** (früher Swagger) und **JSON Schema**.
 - **Django-freundlich**: (natürlich) integriert es sich gut mit Django Core und dem ORM.
 - **Produktionsreif**: Wird von mehreren Unternehmen in echten Projekten eingesetzt (wenn Sie Django Ninja verwenden und Ihr Feedback veröffentlichen möchten, schreiben Sie bitte an ppr.vitaly@gmail.com).

<a href="https://github.com/vitalik/django-ninja-benchmarks" target="_blank">Benchmarks</a>:

![Django Ninja REST Framework](img/benchmark.png)

## Installation

```
pip install django-ninja
```

## Schnelles Beispiel

Starten Sie ein neues Django-Projekt (oder verwenden Sie ein bestehendes)
```
django-admin startproject apidemo
```

In `urls.py`

```python hl_lines="3 5 8 9 10 15"
{!./src/index001.py!}
```

Starten Sie es nun wie gewohnt:
```
./manage.py runserver
```

Hinweis: Sie müssen Django Ninja nicht zu Ihren installierten Apps hinzufügen, damit es funktioniert.

## Probieren Sie es aus

Öffnen Sie Ihren Browser unter <a href="http://127.0.0.1:8000/api/add?a=1&b=2" target="_blank">http://127.0.0.1:8000/api/add?a=1&b=2</a>

Sie sehen die JSON-Antwort wie folgt:
```JSON
{"result": 3}
```
Sie haben gerade eine API erstellt, die:

 - Eine HTTP-GET-Anfrage unter `/api/add` entgegennimmt
 - GET-Parameter `a` und `b` entgegennimmt, validiert und in Typen konvertiert
 - Das Ergebnis als JSON dekodiert
 - Ein OpenAPI-Schema für die definierte Operation generiert

## Interaktive API-Dokumentation

Rufen Sie nun <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a> auf

Sie sehen die automatische, interaktive API-Dokumentation (bereitgestellt von <a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a> oder <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a>) :

![Swagger UI](img/index-swagger-ui.png)


## Zusammenfassung

Kurz gesagt: Sie deklarieren die Typen von Parametern, Request Bodies usw. nur **einmal**, als Funktionsargumente.

Dies geschieht mit standardmäßigen, modernen Python-Typen.

Sie müssen keine neue Syntax lernen, keine Methoden oder Klassen einer bestimmten Bibliothek usw.

Nur standardmäßiges **Python 3.6+**.

Zum Beispiel für einen `int`:

```python
a: int
```

Oder für ein komplexeres `Item`-Modell:

```python
class Item(Schema):
    foo: str
    bar: float

def operation(a: Item):
    ...
```

...mit nur dieser einen Deklaration erhalten Sie:

* Editor-Unterstützung, einschließlich:
    * Autovervollständigung
    * Typprüfung
* Datenvalidierung:
    * Automatische und klare Fehlermeldungen bei ungültigen Daten
    * Validierung selbst für tief verschachtelte JSON-Objekte
* <abbr title="Also known as: serialization, parsing, marshalling">Serialisierung</abbr> von Netzwerkeingabedaten und Konvertierung in Python-Datenausgabe, mit Lesen aus:
    * JSON
    * Pfadparametern
    * Query-Parametern
    * Cookies
    * Headern
    * Formularen
    * Dateien
* Automatische, interaktive API-Dokumentation

Dieses Projekt wurde stark von <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a> inspiriert.

!!! note

    Sehen Sie sich das **[Tutorial](tutorial/index.md)** an, um schnell loszulegen.

    Das Ökosystem rund um Django Ninja:

    1. [django-ninja](index.md): Ein auf Django basierendes Framework, das das Beste von Django mit der Leistungsfähigkeit von Pydantic verbindet — die optimale Wahl an der Schnittstelle von Sicherheit und Komfort.

    2. [django-ninja-crud](django-ninja-crud/index.md): Ein auf django-ninja aufbauendes Framework zur Vereinfachung der Entwicklung von CRUD-Schnittstellen, mit deklarativen Model-Viewsets und szenariobasierten Testmethoden.

    3. [django-ninja-extra](django-ninja-extra/index.md): Ein Werkzeug, mit dem Entwickler umfangreiche Django-Dokumentation überspringen und mit minimalem Code schnell leistungsfähige Webanwendungen und moderne API-Schnittstellen erstellen können.

    4. [django-ninja-jwt](django-ninja-jwt/index.md): Ein JSON-Web-Token-Plugin für django-ninja, das Authentifizierung und verwandte Funktionen implementiert, geforkt von einem beliebten Django Rest Framework Plugin.
