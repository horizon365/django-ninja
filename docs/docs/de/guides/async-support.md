---
comments: true
---
## Einführung

Seit **Version 3.1** bringt Django **Unterstützung für asynchrone Views** mit. Dadurch können Sie effiziente, nebenläufige Views betreiben, die netzwerk- und/oder I/O-gebunden sind.

```
pip install Django>=3.1 django-ninja
```

Asynchrone Views arbeiten effizienter, wenn:
- externe APIs über das Netzwerk aufgerufen werden
- Datenbankabfragen ausgeführt bzw. auf sie gewartet wird
- auf Festplatten gelesen/geschrieben wird

**Django Ninja** setzt voll und ganz auf asynchrone Views und macht sie sehr einfach nutzbar.

## Kurzes Beispiel

### Code

Nehmen wir ein Beispiel. Wir haben eine API-Operation, die etwas Arbeit erledigt (im Moment schläft sie nur für eine bestimmte Anzahl von Sekunden) und ein Wort zurückgibt:
```python hl_lines="5"
import time

@api.get("/say-after")
def say_after(request, delay: int, word: str):
    time.sleep(delay)
    return {"saying": word}
```

Um diesen Code asynchron auszuführen, müssen Sie nur das Schlüsselwort **`async`** zur Funktion hinzufügen (und eine async-fähige Bibliothek für die Arbeit verwenden – in unserem Fall ersetzen wir das `sleep` der Standardbibliothek durch `asyncio.sleep`):

```python hl_lines="1 4 5"
import asyncio

@api.get("/say-after")
async def say_after(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}
```

### Ausführen

Um diesen Code auszuführen, benötigen Sie einen ASGI-Server wie <a href="https://www.uvicorn.org/" target="_blank">Uvicorn</a> oder <a href="https://github.com/django/daphne" target="_blank">Daphne</a>. Verwenden wir hier Uvicorn; das Beispiel finden Sie unten:

Zur Installation von Uvicorn verwenden Sie:

```
pip install uvicorn
```

Starten Sie dann den Server:

```
uvicorn your_project.asgi:application --reload
```

> <small>
> *Hinweis: Ersetzen Sie `your_project` durch den Paketnamen Ihres Projekts*<br>
> *Das Flag `--reload` sorgt dafür, dass der Server bei jeder Änderung am Code automatisch neu geladen wird (nicht für die Produktion verwenden)*
> </small>

!!! note
    Sie können asynchrone Views mit `manage.py runserver` ausführen, das funktioniert jedoch nicht gut mit einigen Bibliotheken, daher wird derzeit (Juli 2020) empfohlen, einen ASGI-Server wie Uvicorn oder Daphne zu verwenden.

### Testen

Öffnen Sie <a href="http://127.0.0.1:8000/api/say-after?delay=3&word=hello" target="_blank">http://127.0.0.1:8000/api/say-after?delay=3&word=hello</a> (**delay=3**) in Ihrem Browser.
Nach 3 Sekunden Wartezeit sollten Sie die Meldung „hello" sehen.

Fluten wir nun diese Operation mit **100 parallelen Requests**:

```
ab -c 100 -n 100 "http://127.0.0.1:8000/api/say-after?delay=3&word=hello"
```

Das führt zu einer Ausgabe wie dieser:

```
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   1.1      1       4
Processing:  3008 3063  16.2   3069    3082
Waiting:     3008 3062  15.7   3068    3079
Total:       3008 3065  16.3   3070    3083

Percentage of the requests served within a certain time (ms)
  50%   3070
  66%   3072
  75%   3075
  80%   3076
  90%   3081
  95%   3082
  98%   3083
  99%   3083
 100%   3083 (longest request)
```

Laut diesen Zahlen ist unser Dienst in der Lage, diese 100 gleichzeitigen Requests mit nur wenig zusätzlichem Aufwand zu verarbeiten.

Um dieselbe Nebenläufigkeit mit WSGI und synchronen Operationen zu erreichen, müssten Sie etwa 10 Worker mit jeweils 10 Threads starten!

## Mischung aus synchronen und asynchronen Operationen

Denken Sie daran, dass Sie in Ihrem Projekt **sowohl synchrone als auch asynchrone Operationen verwenden** können, und **Django Ninja** routet sie automatisch:

```python hl_lines="2 7"

@api.get("/say-sync")
def say_after_sync(request, delay: int, word: str):
    time.sleep(delay)
    return {"saying": word}

@api.get("/say-async")
async def say_after_async(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}
```

## Elasticsearch-Beispiel

Betrachten wir einen realen Anwendungsfall. Verwenden wir für dieses Beispiel eine aktuelle Version von Elasticsearch, die asynchrone Unterstützung mitbringt:
```
pip install elasticsearch>=7.8.0
```

Verwenden Sie nun anstelle der Klasse `Elasticsearch` die Klasse `AsyncElasticsearch` und warten Sie mit `await` auf das Ergebnis:

```python hl_lines="2 7 11 12"
from ninja import NinjaAPI
from elasticsearch import AsyncElasticsearch


api = NinjaAPI()

es = AsyncElasticsearch()


@api.get("/search")
async def search(request, q: str):
    resp = await es.search(
        index="documents", 
        body={"query": {"query_string": {"query": q}}},
        size=20,
    )
    return resp["hits"]
```

## Verwendung des ORM

Derzeit können bestimmte zentrale Teile von Django nicht sicher in einer asynchronen Umgebung arbeiten, da sie einen globalen Zustand besitzen, der coroutine-untauglich ist. Diese Teile von Django werden als „asynchron-unsicher" eingestuft und vor der Ausführung in einer asynchronen Umgebung geschützt. Das **ORM** ist das Hauptbeispiel, aber es gibt weitere Teile, die auf diese Weise geschützt sind.
Erfahren Sie mehr über asynchrone Sicherheit in der <a href="https://docs.djangoproject.com/en/stable/topics/async/#async-safety" target="_blank">offiziellen Django-Dokumentation</a>.

Wenn Sie also Folgendes tun:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = Blog.objects.get(pk=post_id)
    ...
```

Wird ein Fehler ausgelöst. Bis die asynchrone ORM-Implementierung verfügbar ist, können Sie den Adapter `sync_to_async()` verwenden:

```python hl_lines="1 3 9"
from asgiref.sync import sync_to_async

@sync_to_async
def get_blog(post_id):
    return Blog.objects.get(pk=post_id)

@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await get_blog(post_id)
    ...
```

Oder sogar kürzer:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await sync_to_async(Blog.objects.get)(pk=post_id)
    ...
```

Es gibt eine häufige **Falle**: Django-Querysets werden lazy ausgewertet (die Datenbankabfrage passiert erst, wenn Sie mit der Iteration darüber beginnen), daher wird Folgendes **nicht** funktionieren:

```python
all_blogs = await sync_to_async(Blog.objects.all)()
# it will throw an error later when you try to iterate over all_blogs
...
```

Erzwingen Sie stattdessen die Auswertung (mit `list`):

```python
all_blogs = await sync_to_async(list)(Blog.objects.all())
...
```

Seit Django **Version 4.1** bringt Django asynchrone Varianten der ORM-Operationen mit.
Diese machen die Verwendung von `sync_to_async` in den meisten Fällen überflüssig.
Die asynchronen Operationen tragen dieselben Namen wie ihre synchronen Gegenstücke, jedoch mit dem Präfix *a*. Das obige Beispiel
lässt sich damit umschreiben als:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await Blog.objects.aget(pk=post_id)
    ...
```

Beim Arbeiten mit Querysets verwenden Sie `async for` in Kombination mit einem List Comprehension:

```python
all_blogs = [blog async for blog in Blog.objects.all()]
...
```

Erfahren Sie mehr über die asynchrone ORM-Schnittstelle in der <a href="https://docs.djangoproject.com/en/4.1/releases/4.1/#asynchronous-orm-interface" target="_blank">offiziellen Django-Dokumentation</a>.

!!! success

    Fahren Sie mit dem nächsten Abschnitt fort: **[API-Versionierung](versioning.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
