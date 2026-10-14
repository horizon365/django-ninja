---
comments: true
---
## Introduction

Depuis la **version 3.1**, Django est livré avec la **prise en charge des vues asynchrones**. Cela vous permet d'exécuter des vues concurrentes efficaces, limitées par le réseau et/ou les E/S.

```
pip install Django>=3.1 django-ninja
```

Les vues asynchrones fonctionnent plus efficacement lorsque :
- Vous appelez des API externes via le réseau
- Vous effectuez/attendez des requêtes de base de données
- Vous lisez/écrivez sur des disques

**Django Ninja** adopte pleinement les vues asynchrones et les rend très faciles à utiliser.

## Exemple rapide

### Code

Prenons un exemple. Nous avons une opération d'API qui effectue un travail (pour l'instant, simplement dormir pendant un nombre de secondes donné) et renvoie un mot :
```python hl_lines="5"
import time

@api.get("/say-after")
def say_after(request, delay: int, word: str):
    time.sleep(delay)
    return {"saying": word}
```

Pour rendre ce code asynchrone, il vous suffit d'ajouter le mot-clé **`async`** à la fonction (et d'utiliser une bibliothèque compatible async pour le travail - dans notre cas, nous remplaçons le `sleep` de la bibliothèque standard par `asyncio.sleep`) :

```python hl_lines="1 4 5"
import asyncio

@api.get("/say-after")
async def say_after(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}
```

### Exécution

Pour exécuter ce code, vous avez besoin d'un serveur ASGI comme <a href="https://www.uvicorn.org/" target="_blank">Uvicorn</a> ou <a href="https://github.com/django/daphne" target="_blank">Daphne</a>. Utilisons ici Uvicorn, l'exemple est ci-dessous :

Pour installer Uvicorn, utilisez :

```
pip install uvicorn
```

Démarrez ensuite le serveur :

```
uvicorn your_project.asgi:application --reload
```

> <small>
> *Note : remplacez `your_project` par le nom du package de votre projet*<br>
> *L'option `--reload` est utilisée pour recharger automatiquement le serveur chaque fois que vous modifiez le code (à ne pas utiliser en production)*
> </small>

!!! note
    Vous pouvez exécuter des vues asynchrones avec `manage.py runserver`, mais cela ne fonctionne pas bien avec certaines bibliothèques, donc pour le moment (juillet 2020), il est recommandé d'utiliser un serveur ASGI comme Uvicorn ou Daphne.

### Test

Ouvrez <a href="http://127.0.0.1:8000/api/say-after?delay=3&word=hello" target="_blank">http://127.0.0.1:8000/api/say-after?delay=3&word=hello</a> (**delay=3**) dans votre navigateur.
Après avoir attendu 3 secondes, vous devriez voir le message « hello ».

Inondons maintenant cette opération avec **100 requêtes parallèles** :

```
ab -c 100 -n 100 "http://127.0.0.1:8000/api/say-after?delay=3&word=hello"
```

Cela produira quelque chose comme ceci :

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

Selon ces chiffres, notre service est capable de gérer ces 100 requêtes concurrentes avec seulement un peu de surcharge.

Pour obtenir la même concurrence avec WSGI et des opérations synchrones, vous devriez démarrer environ 10 workers avec 10 threads chacun !

## Mélanger des opérations synchrones et asynchrones

Gardez à l'esprit que vous pouvez **utiliser à la fois des opérations sync et async** dans votre projet, et **Django Ninja** les routera automatiquement :

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

## Exemple avec Elasticsearch

Prenons un cas d'utilisation réel. Pour cet exemple, utilisons une version récente d'Elasticsearch qui est livrée avec la prise en charge asynchrone :
```
pip install elasticsearch>=7.8.0
```

Maintenant, au lieu d'utiliser la classe `Elasticsearch`, utilisez la classe `AsyncElasticsearch` et attendez (await) le résultat :

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

## Utilisation de l'ORM

Actuellement, certaines parties clés de Django ne peuvent pas fonctionner en toute sécurité dans un environnement asynchrone car elles ont un état global qui n'est pas compatible avec les coroutines. Ces parties de Django sont classées comme « asynchrones non sûres » (asynchronous-unsafe) et sont protégées contre l'exécution dans un environnement asynchrone. L'**ORM** est le principal exemple, mais il existe d'autres parties protégées de cette manière.
Apprenez-en plus sur la sécurité asynchrone dans la <a href="https://docs.djangoproject.com/en/stable/topics/async/#async-safety" target="_blank">documentation officielle de Django</a>.

Donc, si vous faites ceci :

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = Blog.objects.get(pk=post_id)
    ...
```

Une erreur sera levée. Jusqu'à ce que l'implémentation de l'ORM asynchrone soit disponible, vous pouvez utiliser l'adaptateur `sync_to_async()` :

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

Ou encore plus court :

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await sync_to_async(Blog.objects.get)(pk=post_id)
    ...
```

Il y a un **piège** courant : les querysets de Django sont évalués paresseusement (la requête de base de données n'a lieu que lorsque vous commencez à les itérer), donc ceci ne fonctionnera **pas** :

```python
all_blogs = await sync_to_async(Blog.objects.all)()
# it will throw an error later when you try to iterate over all_blogs
...
```

À la place, forcez l'évaluation (avec `list`) :

```python
all_blogs = await sync_to_async(list)(Blog.objects.all())
...
```

Depuis Django **version 4.1**, Django est livré avec des versions asynchrones des opérations de l'ORM.
Celles-ci éliminent le besoin d'utiliser `sync_to_async` dans la plupart des cas.
Les opérations asynchrones portent les mêmes noms que leurs homologues synchrones, mais préfixés par *a*. Ainsi, en reprenant l'exemple ci-dessus,
vous pouvez le réécrire ainsi :

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await Blog.objects.aget(pk=post_id)
    ...
```

Lorsque vous travaillez avec des querysets, utilisez `async for` associé à une compréhension de liste :

```python
all_blogs = [blog async for blog in Blog.objects.all()]
...
```

Apprenez-en plus sur l'interface ORM asynchrone dans la <a href="https://docs.djangoproject.com/en/4.1/releases/4.1/#asynchronous-orm-interface" target="_blank">documentation officielle de Django</a>.

!!! success

    Poursuivez avec la section suivante **[Versionnage de l'API](versioning.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
