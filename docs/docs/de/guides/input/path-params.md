---
comments: true
---
# Path-Parameter

Sie können Path-„Parameter" mit derselben Syntax deklarieren wie formatierte Python-Strings (die, angenehmerweise, auch mit den <a href="https://swagger.io/docs/specification/describing-parameters/#path-parameters" target="_blank">OpenAPI-Path-Parametern</a> übereinstimmen):

```python hl_lines="1 2"
{!./src/tutorial/path/code01.py!}
```

Der Wert des Path-Parameters `item_id` wird Ihrer Funktion als Argument `item_id` übergeben.

Wenn Sie dieses Beispiel ausführen und <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a> aufrufen, sehen Sie diese Response:

```JSON
{"item_id":"foo"}
```


### Path-Parameter mit Typen

Sie können den Typ eines Path-Parameters mit Standard-Python-Typannotationen in Ihrer Funktion deklarieren:

```python hl_lines="2"
{!./src/tutorial/path/code02.py!}
```

In diesem Fall ist `item_id` als **`int`** deklariert. Dadurch erhalten Sie Editor- und Linter-Unterstützung für die Fehlerprüfung, Codevervollständigung usw.

Wenn Sie diesen Code in Ihrem Browser über <a href="http://localhost:8000/api/items/3" target="_blank">http://localhost:8000/api/items/3</a> ausführen, sehen Sie diese Response:
```JSON
{"item_id":3}
```

!!! tip
    Beachten Sie, dass der Wert, den Ihre Funktion erhält (und zurückgibt), **3** ist, als Python-`int` – nicht der String `"3"`.
    Allein mit dieser Typdeklaration bietet Ihnen **Django Ninja** also automatisches „Parsing" und Validierung des Requests.



### Datenvalidierung

Wenn Sie andererseits <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a> <small>*(`"foo"` is not an int)*</small> in Ihrem Browser aufrufen, sehen Sie einen HTTP-Fehler wie diesen:

```JSON hl_lines="8"
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```


### Django-Path-Converter

Sie können [Django-Path-Converter](https://docs.djangoproject.com/en/stable/topics/http/urls/#path-converters) verwenden,
um beim Parsen des Pfads zu helfen:

```python hl_lines="1"
@api.get("/items/{int:item_id}")
def read_item(request, item_id):
    return {"item_id": item_id}
```

In diesem Fall wird `item_id` als **`int`** geparst. Ist `item_id` kein gültiger `int`, greift die URL nicht.
(Wenn keine andere Route passt, wird zum Beispiel ein 404 Not Found zurückgegeben.)

!!! tip
    Beachten Sie, dass **Django Ninja** für Parameter ohne Typannotation den Standardtyp `str` verwendet, sodass der Wert, den die obige Funktion erhält (und zurückgibt), `"3"` ist,
    als Python-`str` – nicht die Ganzzahl **3**. Um ein `int` zu erhalten, deklarieren Sie `item_id` wie üblich mit einer `int`-Typannotation in der Funktionsdefinition:

    ```python hl_lines="2"
    @api.get("/items/{int:item_id}")
    def read_item(request, item_id:int):
        return {"item_id": item_id}
    ```
 
#### Path-Parameter mit Schrägstrichen

Djangos `path`-Converter erlaubt es Ihnen, pfadähnliche Parameter zu verarbeiten:

```python hl_lines="1"
@api.get('/dir/{path:value}')
def someview(request, value: str):
    return value
```
Sie können diese Operation mit `/dir/some/path/with-slashes` abfragen, und Ihr `value` wird `some/path/with-slashes` entsprechen

### Mehrere Parameter

Sie können beliebig viele Variablen an den `path` übergeben – denken Sie nur daran, eindeutige Namen zu verwenden, und vergessen Sie nicht, dieselben Namen in Ihren Funktionsargumenten zu verwenden.

```python
@api.get("/events/{year}/{month}/{day}")
def events(request, year: int, month: int, day: int):
    return {"date": [year, month, day]}
```


### Verwendung eines Schemas

Sie können auch ein Schema verwenden, um voneinander abhängige Path-Parameter zu kapseln (und sie als Gruppe zu validieren):


```python hl_lines="1 2  5 6 7 8 9 10 11 15"
{!./src/tutorial/path/code010.py!}
```

!!! note
    Beachten Sie, dass wir hier einen `Path`-Source-Hinweis verwenden, um **Django Ninja** mitzuteilen, dass dieses Schema auf Path-Parameter angewendet wird.

### Dokumentation

Wenn Sie nun <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a> in Ihrem Browser öffnen, sehen Sie die automatische, interaktive API-Dokumentation.
![Django Ninja Swagger](../../img/tutorial-path-swagger.png)

!!! done

    Weiter zum nächsten Kapitel! **[Query-Parameter](query-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
