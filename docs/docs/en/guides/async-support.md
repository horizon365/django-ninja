---
comments: true
---
## Introduction

Since **version 3.1**, Django ships with **asynchronous view support**. This allows you to run efficient concurrent views that are network- and/or I/O-bound.

```
pip install Django>=3.1 django-ninja
```

Asynchronous views work more efficiently when:
- Calling external APIs over the network
- Performing/awaiting database queries
- Reading/writing to disk drives

**Django Ninja** fully embraces asynchronous views and makes them very easy to use.

## Quick example

### Code

Let's take an example. We have an API operation that does some work (for now, just sleeping for a given number of seconds) and returns a word:
```python hl_lines="5"
import time

@api.get("/say-after")
def say_after(request, delay: int, word: str):
    time.sleep(delay)
    return {"saying": word}
```

To make this code run asynchronously, all you have to do is add the **`async`** keyword to the function (and use an async-aware library for the work - in our case we replace the standard library's `sleep` with `asyncio.sleep`):

```python hl_lines="1 4 5"
import asyncio

@api.get("/say-after")
async def say_after(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}
```

### Running

To run this code, you need an ASGI server like <a href="https://www.uvicorn.org/" target="_blank">Uvicorn</a> or <a href="https://github.com/django/daphne" target="_blank">Daphne</a>. Let's use Uvicorn here, the example is below:

To install Uvicorn, use:

```
pip install uvicorn
```

Then start the server:

```
uvicorn your_project.asgi:application --reload
```

> <small>
> *Note: replace `your_project` with your project's package name*<br>
> *The `--reload` flag is used to automatically reload the server whenever you make any changes to the code (do not use in production)*
> </small>

!!! note
    You can run asynchronous views with `manage.py runserver`, but it does not play well with some libraries, so at this time (July 2020) it is recommended to use an ASGI server like Uvicorn or Daphne.

### Testing

Open <a href="http://127.0.0.1:8000/api/say-after?delay=3&word=hello" target="_blank">http://127.0.0.1:8000/api/say-after?delay=3&word=hello</a> (**delay=3**) in your browser.
After waiting 3 seconds, you should see the "hello" message.

Now let's flood this operation with **100 parallel requests**:

```
ab -c 100 -n 100 "http://127.0.0.1:8000/api/say-after?delay=3&word=hello"
```

This will produce something like this:

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

According to these numbers, our service is able to handle these 100 concurrent requests with only a little overhead.

To achieve the same concurrency with WSGI and synchronous operations, you would need to start about 10 workers with 10 threads each!

## Mixing synchronous and asynchronous operations

Keep in mind that you can **use both sync and async operations** in your project, and **Django Ninja** will route them automatically:

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

## Elasticsearch example

Let's take a real-world use case. For this example, let's use a recent version of Elasticsearch that comes with async support:
```
pip install elasticsearch>=7.8.0
```

Now, instead of using the `Elasticsearch` class, use the `AsyncElasticsearch` class and `await` the result:

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

## Using the ORM

Currently, certain key parts of Django are not able to operate safely in an asynchronous environment because they have global state that is not coroutine-aware. These parts of Django are classified as "asynchronous-unsafe" and are protected from execution in an asynchronous environment. The **ORM** is the main example, but there are other parts that are protected in this way.
Learn more about async safety in the <a href="https://docs.djangoproject.com/en/stable/topics/async/#async-safety" target="_blank">Django official documentation</a>.

So if you do this:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = Blog.objects.get(pk=post_id)
    ...
```

It will throw an error. Until the async ORM implementation is available, you can use the `sync_to_async()` adapter:

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

Or even shorter:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await sync_to_async(Blog.objects.get)(pk=post_id)
    ...
```

There is a common **pitfall**: Django querysets are lazily evaluated (the database query happens only when you start iterating over them), so this will **not** work:

```python
all_blogs = await sync_to_async(Blog.objects.all)()
# it will throw an error later when you try to iterate over all_blogs
...
```

Instead, force evaluation (with `list`):

```python
all_blogs = await sync_to_async(list)(Blog.objects.all())
...
```

Since Django **version 4.1**, Django ships with asynchronous versions of ORM operations.
These eliminate the need to use `sync_to_async` in most cases.
The asynchronous operations have the same names as their synchronous counterparts, but prefixed with *a*. So using the example above,
you can rewrite it as:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await Blog.objects.aget(pk=post_id)
    ...
```

When working with querysets, use `async for` paired with a list comprehension:

```python
all_blogs = [blog async for blog in Blog.objects.all()]
...
```

Learn more about the asynchronous ORM interface in the <a href="https://docs.djangoproject.com/en/4.1/releases/4.1/#asynchronous-orm-interface" target="_blank">Django official documentation</a>.

!!! success

    Continue to the next section **[API versioning](versioning.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
