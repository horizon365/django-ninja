---
comments: true
---
# Path Parameters

Je kunt path "parameters" declareren met dezelfde syntax als Python formatted strings (die, gelukkig, ook overeenkomt met <a href="https://swagger.io/docs/specification/describing-parameters/#path-parameters" target="_blank">OpenAPI path parameters</a>):

```python hl_lines="1 2"
{!./src/tutorial/path/code01.py!}
```

De waarde van de path parameter `item_id` wordt als argument `item_id` aan je functie doorgegeven.

Dus als je dit voorbeeld uitvoert en naar <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a> gaat, zie je deze response:

```JSON
{"item_id":"foo"}
```


### Path Parameters met types

Je kunt het type van een path parameter declareren met standaard Python type-annotaties in je functie:

```python hl_lines="2"
{!./src/tutorial/path/code02.py!}
```

In dit geval is `item_id` gedeclareerd als **`int`**. Dit geeft je editor- en linterondersteuning voor foutcontrole, code completion, enz.

Als je deze code in je browser uitvoert via <a href="http://localhost:8000/api/items/3" target="_blank">http://localhost:8000/api/items/3</a>, zie je deze response:
```JSON
{"item_id":3}
```

!!! tip
    Let op: de waarde die je functie ontvangt (en teruggeeft) is **3**, als Python `int` — niet de string `"3"`.
    Met alleen die typedefinitie biedt **Django Ninja** je dus automatisch request "parsing" en validatie.



### Data validatie

Aan de andere kant, als je <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a> <small>*(`"foo"` is geen int)*</small> in je browser bezoekt, zie je een HTTP foutmelding zoals deze:

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


### Django Path Converters

Je kunt [Django path converters](https://docs.djangoproject.com/en/stable/topics/http/urls/#path-converters)
gebruiken om het parsen van het path te ondersteunen:

```python hl_lines="1"
@api.get("/items/{int:item_id}")
def read_item(request, item_id):
    return {"item_id": item_id}
```

In dit geval wordt `item_id` geparst als **`int`**. Als `item_id` geen geldige `int` is, zal de URL niet matchen.
(Als bijvoorbeeld geen andere route matcht, wordt er een 404 Not Found teruggegeven.)

!!! tip
    Let op: aangezien **Django Ninja** het standaard type `str` gebruikt voor parameters zonder annotatie, is de waarde die de bovenstaande functie ontvangt (en teruggeeft) `"3"`,
    als Python `str` — niet het gehele getal **3**. Om een `int` te ontvangen, declareer je `item_id` gewoon met een `int` type-annotatie in de functiedefinitie zoals gebruikelijk:

    ```python hl_lines="2"
    @api.get("/items/{int:item_id}")
    def read_item(request, item_id:int):
        return {"item_id": item_id}
    ```
 
#### Path Parameters met slashes

Met de `path` converter van Django kun je path-achtige parameters afhandelen:

```python hl_lines="1"
@api.get('/dir/{path:value}')
def someview(request, value: str):
    return value
```
Je kunt deze operatie bevragen met `/dir/some/path/with-slashes`, en je `value` zal gelijk zijn aan `some/path/with-slashes`

### Meerdere parameters

Je kunt zoveel variabelen als je wilt doorgeven aan het `path` — vergeet niet unieke namen te gebruiken en denk eraan dezelfde namen te gebruiken in je functieargumenten.

```python
@api.get("/events/{year}/{month}/{day}")
def events(request, year: int, month: int, day: int):
    return {"date": [year, month, day]}
```


### Een Schema gebruiken

Je kunt ook een schema gebruiken om onderling afhankelijke path parameters in te kapselen (en ze als groep te valideren):


```python hl_lines="1 2  5 6 7 8 9 10 11 15"
{!./src/tutorial/path/code010.py!}
```

!!! note
    Let op: hier gebruiken we een `Path` source hint om **Django Ninja** te laten weten dat dit schema zal worden toegepast op path parameters.

### Documentatie

Wanneer je nu <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a> in je browser opent, zie je de automatische, interactieve API-documentatie.
![Django Ninja Swagger](../../img/tutorial-path-swagger.png)

!!! done

    Ga verder naar het volgende hoofdstuk! **[Query Parameters](query-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
