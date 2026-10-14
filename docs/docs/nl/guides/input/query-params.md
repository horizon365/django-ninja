---
comments: true
---
# Query Parameters

Wanneer je functieparameters declareert die geen onderdeel zijn van de path parameters, worden ze automatisch geïnterpreteerd als "query" parameters.
```python hl_lines="5"
{!./src/tutorial/query/code01.py!}
```

Om deze operatie te bevragen, kun je een URL zoals deze gebruiken:

```
http://localhost:8000/api/weapons?offset=0&limit=10
```
Standaard zijn alle GET parameters strings; wanneer je je functieparameters van types voorziet, worden ze naar dat type geconverteerd en daartegen gevalideerd.

Dezelfde voordelen die gelden voor path parameters gelden ook voor query parameters:

- Editorondersteuning (uiteraard)
- Data "parsing"
- Data validatie
- Automatische documentatie


!!! note
    Als je je parameters niet van annotaties voorziet, worden ze behandeld als het type `str`

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit, offset):
    # type(limit) == str
    # type(offset) == str
```

### Standaardwaarden

Omdat query parameters geen vast onderdeel van het path zijn, zijn ze optioneel en kunnen ze standaardwaarden hebben:

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit: int = 10, offset: int = 0):
    return weapons[offset : offset + limit]
```

In het voorbeeld hierboven hebben we de standaardwaarden `offset=0` en `limit=10` ingesteld.

Dus een bezoek aan de URL:
```
http://localhost:8000/api/weapons
```
is hetzelfde als een bezoek aan:
```
http://localhost:8000/api/weapons?offset=0&limit=10
```
Als je bijvoorbeeld bezoekt:
```
http://localhost:8000/api/weapons?offset=20
```

Zijn de parameterwaarden in je functie:

 - `offset=20` (omdat je die in de URL hebt ingesteld)
 - `limit=10` (omdat dat de standaardwaarde is)


### Verplichte en optionele parameters

Je kunt verplichte of optionele GET parameters declareren op dezelfde manier als je Python functieparameters declareert:

```python hl_lines="5"
{!./src/tutorial/query/code02.py!}
```

In dit geval zal **Django Ninja** de parameter `q` die je in het GET verzoek doorgeeft altijd valideren, terwijl de parameter `offset` een optioneel geheel getal is.

### Typeconversie van GET parameters

Laten we meerdere getypeerde parameters declareren:
```python hl_lines="5"
{!./src/tutorial/query/code03.py!}
```
Het type `str` wordt ongewijzigd doorgegeven.

Voor het type `bool` zal je functie bij alle volgende varianten:
```
http://localhost:8000/api/example?b=1
http://localhost:8000/api/example?b=True
http://localhost:8000/api/example?b=true
http://localhost:8000/api/example?b=on
http://localhost:8000/api/example?b=yes
```
of elke andere schrijfwijze (hoofdletters, met hoofdletter aan het begin, enz.) zien dat de parameter `b` de `bool` waarde `True` heeft, anders `False`.

Datums kunnen datumstrings en integers zijn (Unix timestamps):

<pre style="font-size: .85em; background-color:rgb(245, 245, 245);">
http://localhost:8000/api/example?d=<strong>1577836800</strong>  # equivalent to 2020-01-01
http://localhost:8000/api/example?d=<strong>2020-01-01</strong>
</pre>


### Een Schema gebruiken

Je kunt ook een schema gebruiken om GET parameters in te kapselen:

```python hl_lines="1 2  5 6 7 8"
{!./src/tutorial/query/code010.py!}
```

Voor complexere filterscenario's, zie [Filtering](./filtering.md).

!!! done

    Ga verder naar het volgende hoofdstuk! **[Request Body](body.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
