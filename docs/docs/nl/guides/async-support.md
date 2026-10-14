---
comments: true
---
## Introductie

Sinds **versie 3.1** wordt Django geleverd met **ondersteuning voor asynchrone views**. Hiermee kun je efficiënte gelijktijdige views draaien die netwerk- en/of I/O-gebonden zijn.

```
pip install Django>=3.1 django-ninja
```

Asynchrone views werken efficiënter wanneer:
- Externe API's via het netwerk worden aangeroepen
- Databasequery's worden uitgevoerd/waarop wordt gewacht
- Er wordt gelezen van en geschreven naar schijven

**Django Ninja** omarmt asynchrone views volledig en maakt ze heel eenvoudig te gebruiken.

## Snel voorbeeld

### Code

Laten we een voorbeeld nemen. We hebben een API-operatie die wat werk verricht (voorlopig alleen slapen gedurende een opgegeven aantal seconden) en een woord teruggeeft:
```python hl_lines="5"
import time

@api.get("/say-after")
def say_after(request, delay: int, word: str):
    time.sleep(delay)
    return {"saying": word}
```

Om deze code asynchroon te laten draaien, hoef je alleen het sleutelwoord **`async`** aan de functie toe te voegen (en een async-bewuste library te gebruiken voor het werk - in ons geval vervangen we de `sleep` van de standaardbibliotheek door `asyncio.sleep`):

```python hl_lines="1 4 5"
import asyncio

@api.get("/say-after")
async def say_after(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}
```

### Uitvoeren

Om deze code uit te voeren heb je een ASGI-server nodig zoals <a href="https://www.uvicorn.org/" target="_blank">Uvicorn</a> of <a href="https://github.com/django/daphne" target="_blank">Daphne</a>. Laten we hier Uvicorn gebruiken, het voorbeeld staat hieronder:

Om Uvicorn te installeren, gebruik je:

```
pip install uvicorn
```

Start daarna de server:

```
uvicorn your_project.asgi:application --reload
```

> <small>
> *Let op: vervang `your_project` door de pakketnaam van je project*<br>
> *De vlag `--reload` zorgt ervoor dat de server automatisch wordt herladen wanneer je iets aan de code wijzigt (niet gebruiken in productie)*
> </small>

!!! note
    Je kunt asynchrone views draaien met `manage.py runserver`, maar dat werkt niet goed samen met sommige libraries, dus op dit moment (juli 2020) wordt aangeraden een ASGI-server zoals Uvicorn of Daphne te gebruiken.

### Testen

Open <a href="http://127.0.0.1:8000/api/say-after?delay=3&word=hello" target="_blank">http://127.0.0.1:8000/api/say-after?delay=3&word=hello</a> (**delay=3**) in je browser.
Na 3 seconden wachten zou je het bericht "hello" moeten zien.

Nu overspoelen we deze operatie met **100 parallelle verzoeken**:

```
ab -c 100 -n 100 "http://127.0.0.1:8000/api/say-after?delay=3&word=hello"
```

Dit levert zoiets als dit op:

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

Volgens deze cijfers kan onze service deze 100 gelijktijdige verzoeken afhandelen met slechts weinig overhead.

Om dezelfde gelijktijdigheid te bereiken met WSGI en synchrone operaties, zou je ongeveer 10 workers met elk 10 threads moeten starten!

## Synchrone en asynchrone operaties door elkaar gebruiken

Houd er rekening mee dat je **zowel synchrone als asynchrone operaties** in je project kunt gebruiken, en dat **Django Ninja** ze automatisch routeert:

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

## Elasticsearch voorbeeld

Laten we een realistisch gebruiksvoorbeeld nemen. Voor dit voorbeeld gebruiken we een recente versie van Elasticsearch die wordt geleverd met async-ondersteuning:
```
pip install elasticsearch>=7.8.0
```

Gebruik nu, in plaats van de class `Elasticsearch`, de class `AsyncElasticsearch` en `await` het resultaat:

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

## De ORM gebruiken

Momenteel kunnen bepaalde belangrijke onderdelen van Django niet veilig opereren in een asynchrone omgeving, omdat ze globale state bevatten die niet coroutine-bewust is. Deze onderdelen van Django worden geclassificeerd als "async-unsafe" en worden beschermd tegen uitvoering in een asynchrone omgeving. De **ORM** is het belangrijkste voorbeeld, maar er zijn meer onderdelen die op deze manier worden beschermd.
Lees meer over async-veiligheid in de <a href="https://docs.djangoproject.com/en/stable/topics/async/#async-safety" target="_blank">officiële Django-documentatie</a>.

Dus als je dit doet:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = Blog.objects.get(pk=post_id)
    ...
```

Dan treedt er een fout op. Totdat de asynchrone ORM-implementatie beschikbaar is, kun je de adapter `sync_to_async()` gebruiken:

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

Of zelfs korter:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await sync_to_async(Blog.objects.get)(pk=post_id)
    ...
```

Er is een veelvoorkomende **valkuil**: Django querysets worden lui geëvalueerd (de databasequery vindt pas plaats wanneer je begint met itereren), dus dit zal **niet** werken:

```python
all_blogs = await sync_to_async(Blog.objects.all)()
# it will throw an error later when you try to iterate over all_blogs
...
```

Forceer in plaats daarvan de evaluatie (met `list`):

```python
all_blogs = await sync_to_async(list)(Blog.objects.all())
...
```

Sinds Django **versie 4.1** wordt Django geleverd met asynchrone versies van ORM-operaties.
Deze maken het in de meeste gevallen overbodig om `sync_to_async` te gebruiken.
De asynchrone operaties hebben dezelfde namen als hun synchrone tegenhangers, maar voorzien van het voorvoegsel *a*. Dus met het voorbeeld hierboven
kun je het herschrijven als:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await Blog.objects.aget(pk=post_id)
    ...
```

Wanneer je met querysets werkt, gebruik je `async for` in combinatie met een list comprehension:

```python
all_blogs = [blog async for blog in Blog.objects.all()]
...
```

Lees meer over de asynchrone ORM-interface in de <a href="https://docs.djangoproject.com/en/4.1/releases/4.1/#asynchronous-orm-interface" target="_blank">officiële Django-documentatie</a>.

!!! success

    Ga verder naar de volgende sectie **[API-versiebeheer](versioning.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
