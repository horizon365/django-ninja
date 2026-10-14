---
comments: true
---
# Formulardaten

**Django Ninja** erlaubt es Ihnen außerdem, `request.POST`-Daten zu parsen und zu validieren
(das heißt, `application/x-www-form-urlencoded` oder `multipart/form-data`).

## Formulardaten als Parameter

```python hl_lines="1 4"
from ninja import NinjaAPI, Form

@api.post("/login")
def login(request, username: Form[str], password: Form[str]):
    return {'username': username, 'password': '*****'}
```

Beachten Sie Folgendes:

1) Sie müssen die Klasse `Form` aus `ninja` importieren
```python
from ninja import Form
```

2) Verwenden Sie `Form` als Standardwert für den Parameter:
```python
username: Form[str]
```

## Verwendung eines Schemas

Ähnlich wie bei [Request Body](body.md#declare-it-as-a-parameter) können Sie ein Schema verwenden, um Ihre Parameter zu strukturieren.

```python hl_lines="12"
{!./src/tutorial/form/code01.py!}
```

## Request-Formular + Path- + Query-Parameter

Ähnlich wie bei [Request Body](body.md#request-body-path-query-parameters) können Sie Formulardaten mit anderen Parameterquellen kombinieren.

Sie können Query-Parameter **und** Path-Parameter **und** Formularfelder **usw.** gleichzeitig deklarieren.

**Django Ninja** erkennt, dass Funktionsparameter, die Path-Parametern entsprechen, **aus dem Pfad** genommen werden sollen,
während Funktionsparameter, die mit `Form(...)` deklariert wurden, **aus den Formularfeldern des Requests** genommen werden sollen, und so weiter.

```python hl_lines="12"
{!./src/tutorial/form/code02.py!}
```
## Leere Formularfelder auf Standardwerte abbilden

Optionale Formularfelder werden häufig mit leeren Werten gesendet. Dieser Wert wird als leerer String interpretiert, sodass die Validierung für Felder wie `int` oder `bool` fehlschlagen kann.

Wie in der Pydantic-Dokumentation beschrieben, lässt sich das mit [generischen Klassen als Typen](https://pydantic.com.cn/usage/types/#generic-classes-as-types) lösen.

```python hl_lines="15 16 23-25"
{!./src/tutorial/form/code03.py!}
```

!!! done

    Weiter zum nächsten Kapitel! **[Datei-Uploads](file-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
