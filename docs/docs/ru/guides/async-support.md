---
comments: true
---
## Введение

Начиная с **версии 3.1**, Django поставляется с **поддержкой асинхронных представлений**. Это позволяет запускать эффективные конкурентные представления, ограниченные сетью и/или вводом-выводом.

```
pip install Django>=3.1 django-ninja
```

Асинхронные представления работают более эффективно, когда:
- Выполняются вызовы внешних API по сети
- Выполняются/ожидаются запросы к базе данных
- Выполняется чтение/запись на диски

**Django Ninja** полностью поддерживает асинхронные представления и делает их очень простыми в использовании.

## Быстрый пример

### Код

Рассмотрим пример. У нас есть API-операция, которая выполняет некоторую работу (пока это просто сон в течение заданного количества секунд) и возвращает слово:
```python hl_lines="5"
import time

@api.get("/say-after")
def say_after(request, delay: int, word: str):
    time.sleep(delay)
    return {"saying": word}
```

Чтобы этот код выполнялся асинхронно, всё, что нужно сделать — добавить ключевое слово **`async`** к функции (и использовать async-совместимую библиотеку для работы — в нашем случае мы заменяем `sleep` из стандартной библиотеки на `asyncio.sleep`):

```python hl_lines="1 4 5"
import asyncio

@api.get("/say-after")
async def say_after(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}
```

### Запуск

Для запуска этого кода нужен ASGI-сервер, например <a href="https://www.uvicorn.org/" target="_blank">Uvicorn</a> или <a href="https://github.com/django/daphne" target="_blank">Daphne</a>. Здесь мы используем Uvicorn, пример ниже:

Для установки Uvicorn используйте:

```
pip install uvicorn
```

Затем запустите сервер:

```
uvicorn your_project.asgi:application --reload
```

> <small>
> *Примечание: замените `your_project` на имя пакета вашего проекта*<br>
> *Флаг `--reload` используется для автоматической перезагрузки сервера при любом изменении кода (не используйте его в production)*
> </small>

!!! note
    Асинхронные представления можно запускать с помощью `manage.py runserver`, но это плохо работает с некоторыми библиотеками, поэтому на данный момент (июль 2020) рекомендуется использовать ASGI-сервер, такой как Uvicorn или Daphne.

### Тестирование

Откройте в браузере <a href="http://127.0.0.1:8000/api/say-after?delay=3&word=hello" target="_blank">http://127.0.0.1:8000/api/say-after?delay=3&word=hello</a> (**delay=3**).
Через 3 секунды вы должны увидеть сообщение "hello".

Теперь обрушим на эту операцию **100 параллельных запросов**:

```
ab -c 100 -n 100 "http://127.0.0.1:8000/api/say-after?delay=3&word=hello"
```

Результат будет примерно таким:

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

Согласно этим цифрам, наш сервис способен обрабатывать эти 100 конкурентных запросов лишь с небольшой дополнительной задержкой.

Чтобы добиться той же конкурентности с WSGI и синхронными операциями, пришлось бы запустить около 10 workers по 10 потоков в каждом!

## Смешивание синхронных и асинхронных операций

Имейте в виду, что в вашем проекте можно **использовать и синхронные, и асинхронные операции**, а **Django Ninja** будет автоматически направлять их:

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

## Пример с Elasticsearch

Рассмотрим пример из реальной практики. Для этого примера используем свежую версию Elasticsearch, в которой есть поддержка async:
```
pip install elasticsearch>=7.8.0
```

Теперь вместо класса `Elasticsearch` используйте класс `AsyncElasticsearch` и применяйте `await` к результату:

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

## Использование ORM

В настоящее время некоторые ключевые части Django не могут безопасно работать в асинхронной среде, потому что у них есть глобальное состояние, не учитывающее корутины. Эти части Django классифицируются как "асинхронно-небезопасные" и защищены от выполнения в асинхронной среде. **ORM** — главный пример, но есть и другие части, защищённые таким образом.
Подробнее о async-безопасности читайте в <a href="https://docs.djangoproject.com/en/stable/topics/async/#async-safety" target="_blank">официальной документации Django</a>.

Поэтому, если сделать так:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = Blog.objects.get(pk=post_id)
    ...
```

Будет выброшена ошибка. Пока не доступна реализация асинхронного ORM, вы можете использовать адаптер `sync_to_async()`:

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

Или даже короче:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await sync_to_async(Blog.objects.get)(pk=post_id)
    ...
```

Есть распространённая **ловушка**: Django querysets вычисляются лениво (запрос к базе данных выполняется только когда вы начинаете итерацию по ним), поэтому это **не** сработает:

```python
all_blogs = await sync_to_async(Blog.objects.all)()
# it will throw an error later when you try to iterate over all_blogs
...
```

Вместо этого форсируйте вычисление (с помощью `list`):

```python
all_blogs = await sync_to_async(list)(Blog.objects.all())
...
```

Начиная с Django **версии 4.1**, Django поставляется с асинхронными версиями операций ORM.
Они избавляют от необходимости использовать `sync_to_async` в большинстве случаев.
Асинхронные операции имеют те же имена, что и их синхронные аналоги, но с префиксом *a*. Так, используя пример выше,
его можно переписать как:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await Blog.objects.aget(pk=post_id)
    ...
```

При работе с querysets используйте `async for` в паре с генератором списка:

```python
all_blogs = [blog async for blog in Blog.objects.all()]
...
```

Подробнее об асинхронном интерфейсе ORM читайте в <a href="https://docs.djangoproject.com/en/4.1/releases/4.1/#asynchronous-orm-interface" target="_blank">официальной документации Django</a>.

!!! success

    Перейдите к следующему разделу **[Версионирование API](versioning.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
