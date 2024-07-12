---
comments: true
---
## 介绍

自 ** 3.1 版本** 起, Django 带有 **异步视图支持**。 这允许你运行高效的受网络和/或 I/O 限制的并发视图。

```
pip install Django>=3.1 django-ninja
```

在以下方面异步视图工作得更高效:
- 通过网络调用外部 API
- 执行/等待数据库查询
- 对磁盘驱动器进行读/写

**Django Ninja** 充分利用异步视图，并使其非常容易使用。

## 快速示例

### 代码

让我们举个例子。我们有一个 API 操作，它做一些工作（目前只是为给定的秒数休眠）并返回一个单词：
```python hl_lines="5"
import time

@api.get("/say-after")
def say_after(request, delay: int, word: str):
    time.sleep(delay)
    return {"saying": word}
```

要使这段代码异步执行， 你所要做的就是给函数添加 **`async`** 关键字 (并使用对工作处理有感知的异步库 - 在我们的例子中，我们将标准库的 `sleep` 替换为 `asyncio.sleep`):

```python hl_lines="1 4 5"
import asyncio

@api.get("/say-after")
async def say_after(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}
```

### 运行

要运行此代码，你需要一个像<a href="https://www.uvicorn.org/" target="_blank">Uvicorn</a> 或 <a href="https://github.com/django/daphne" target="_blank">Daphne</a>的 ASGI 服务。我们这里就使用 Uvicorn 吧, 示例如下:

要安装 Uvicorn，使用:

```
pip install uvicorn
```

然后启动服务:

```
uvicorn your_project.asgi:application --reload
```

> <small>
> *注意: 用你的项目包名替换 `your_project` *<br>
> *`--reload` 标志用于在你对代码进行任何更改时自动重新加载服务器（在生产环境中不要使用）*
> </small>

!!! 注意
    你可以使用 `manage.py runserver` 运行异步视图，但它与一些库配合不太好，所以在此时（2020 年 7 月）建议使用像 Uvicorn 或 Daphne 这样的 ASGI 服务器。

### 测试

在你的浏览器中打开 <a href="http://127.0.0.1:8000/api/say-after?delay=3&word=hello" target="_blank">http://127.0.0.1:8000/api/say-after?delay=3&word=hello</a> (**delay=3**)
等待 3 秒后，你应该看到 "hello" 消息。

现在让我们用 **100 parallel requests** 来淹没这个操作:

```
ab -c 100 -n 100 "http://127.0.0.1:8000/api/say-after?delay=3&word=hello"
```

这将得到类似这样的结果：

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

根据这些数字，我们的服务能够处理这 100 个并发请求，只有一点开销。

要使用 WSGI 和同步操作实现相同的并发，你需要启动大约 10 个每个有 10 个线程的工作者！

## 混合同步和异步操作

请记住，你可以在你的项目中 **同时使用 sync 和 async 操作** ，并且 **Django Ninja** 将自动路由它:

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

## Elasticsearch 示例

让我们举一个实际的用例。对于这个例子，让我们使用现在带有异步支持的最新版本的 Elasticsearch：
```
pip install elasticsearch>=7.8.0
```

现在，不是使用 `Elasticsearch` 类，而是使用 `AsyncElasticsearch` 类并 `await` 结果:

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

## 使用 ORM

目前，Django 的某些关键部分不能在异步环境中安全操作，因为它们具有全局状态，该状态不是协程感知的。Django 的这些部分被分类为“异步不安全”，并在异步环境中受到保护，不执行。*** ORM*** 是主要示例，但还有其他部分也以这种方式受到保护。
在<a href="https://docs.djangoproject.com/en/stable/topics/async/#async-safety" target="_blank">Django 官方文档</a>中了解更多关于异步安全的信息。

所以，如果你这样做：

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = Blog.objects.get(pk=post_id)
    ...
```

它会抛出一个错误。在异步 ORM 实现之前，你可以使用 `sync_to_async()` 适配器:

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

或者甚至更短：

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await sync_to_async(Blog.objects.get)(pk=post_id)
    ...
```

有一个常见的 **陷阱**: Django 查询集是惰性评估的（数据库查询仅在你开始迭代时发生），所以这将 **不** 起作用：

```python
all_blogs = await sync_to_async(Blog.objects.all)()
# it will throw an error later when you try to iterate over all_blogs
...
```

相反，使用评估 (用 `list`):

```python
all_blogs = await sync_to_async(list)(Blog.objects.all())
...
```

自从 Django **version 4.1**，Django 带有异步版本的 ORM 操作。
这些在大多数情况下消除了使用 `sync_to_async`的需要。
异步操作具有与它们的同步对应操作相同的名称，但前面加上 *a*。所以使用上面的例子，
你可以重写为:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await Blog.objects.aget(pk=post_id)
    ...
```

当处理查询集时，使用 `async for`与列表推导式配对：

```python
all_blogs = [blog async for blog in Blog.objects.all()]
...
```

在<a href="https://docs.djangoproject.com/en/4.1/releases/4.1/#asynchronous-orm-interface" target="_blank">Django 官方文档</a>中了解更多关于异步 ORM 接口的信息。

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
