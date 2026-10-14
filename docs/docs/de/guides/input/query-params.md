---
comments: true
---
# Query-Parameter

Wenn Sie Funktionsparameter deklarieren, die nicht zu den Path-Parametern gehören, werden sie automatisch als „Query"-Parameter interpretiert.
```python hl_lines="5"
{!./src/tutorial/query/code01.py!}
```

Um diese Operation abzufragen, können Sie eine URL wie diese verwenden:

```
http://localhost:8000/api/weapons?offset=0&limit=10
```
Standardmäßig sind alle GET-Parameter Strings; wenn Sie Ihre Funktionsparameter mit Typen annotieren, werden sie in diesen Typ konvertiert und gegen ihn validiert.

Dieselben Vorteile, die für Path-Parameter gelten, treffen auch auf Query-Parameter zu:

- Editor-Unterstützung (offensichtlich)
- „Parsing" der Daten
- Datenvalidierung
- Automatische Dokumentation


!!! note
    Wenn Sie Ihre Parameter nicht annotieren, werden sie als Typ `str` behandelt

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit, offset):
    # type(limit) == str
    # type(offset) == str
```

### Standardwerte

Da Query-Parameter kein fester Bestandteil des Pfads sind, sind sie optional und können Standardwerte haben:

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit: int = 10, offset: int = 0):
    return weapons[offset : offset + limit]
```

Im obigen Beispiel haben wir die Standardwerte `offset=0` und `limit=10` gesetzt.

Der Aufruf der URL:
```
http://localhost:8000/api/weapons
```
ist daher identisch mit dem Aufruf von:
```
http://localhost:8000/api/weapons?offset=0&limit=10
```
Wenn Sie zum Beispiel aufrufen:
```
http://localhost:8000/api/weapons?offset=20
```

lauten die Parameterwerte in Ihrer Funktion:

 - `offset=20` (weil Sie ihn in der URL gesetzt haben)
 - `limit=10` (weil das der Standardwert ist)


### Pflicht- und optionale Parameter

Pflicht- oder optionale GET-Parameter können Sie genauso deklarieren wie Python-Funktionsparameter:

```python hl_lines="5"
{!./src/tutorial/query/code02.py!}
```

In diesem Fall validiert **Django Ninja** den Parameter `q`, den Sie im GET-Request übergeben, immer, während der Parameter `offset` eine optionale Ganzzahl ist.

### Typkonvertierung von GET-Parametern

Deklarieren wir mehrere typisierte Parameter:
```python hl_lines="5"
{!./src/tutorial/query/code03.py!}
```
Der Typ `str` wird unverändert übergeben.

Beim Typ `bool` wird Ihre Funktion bei allen folgenden Varianten:
```
http://localhost:8000/api/example?b=1
http://localhost:8000/api/example?b=True
http://localhost:8000/api/example?b=true
http://localhost:8000/api/example?b=on
http://localhost:8000/api/example?b=yes
```
oder jeder anderen Schreibweise (Großbuchstaben, initialer Großbuchstabe usw.) sehen, dass der Parameter `b` den `bool`-Wert `True` hat, andernfalls `False`.

Datumswerte können Date-Strings und Integer (Unix-Timestamps) sein:

<pre style="font-size: .85em; background-color:rgb(245, 245, 245);">
http://localhost:8000/api/example?d=<strong>1577836800</strong>  # equivalent to 2020-01-01
http://localhost:8000/api/example?d=<strong>2020-01-01</strong>
</pre>


### Verwendung eines Schemas

Sie können auch ein Schema verwenden, um GET-Parameter zu kapseln:

```python hl_lines="1 2  5 6 7 8"
{!./src/tutorial/query/code010.py!}
```

Für komplexere Filterszenarien siehe [Filterung](./filtering.md).

!!! done

    Weiter zum nächsten Kapitel! **[Request Body](body.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
