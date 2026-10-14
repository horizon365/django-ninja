---
comments: true
---
## 소개

**버전 3.1**부터 Django는 **비동기 뷰 지원**을 기본 제공합니다. 이를 통해 네트워크 및/또는 I/O 바운드인 효율적인 동시성 뷰를 실행할 수 있습니다.

```
pip install Django>=3.1 django-ninja
```

비동기 뷰는 다음과 같은 경우에 더 효율적으로 동작합니다:
- 네트워크를 통해 외부 API 호출
- 데이터베이스 쿼리 수행/대기
- 디스크 드라이브 읽기/쓰기

**Django Ninja**는 비동기 뷰를 완전히 지원하며 매우 쉽게 사용할 수 있게 해줍니다.

## 간단한 예제

### 코드

예를 들어 보겠습니다. 어떤 작업을 수행하고(지금은 주어진 초만큼 sleep) 단어를 반환하는 API operation이 있다고 합시다:
```python hl_lines="5"
import time

@api.get("/say-after")
def say_after(request, delay: int, word: str):
    time.sleep(delay)
    return {"saying": word}
```

이 코드를 비동기로 실행하려면 함수에 **`async`** 키워드를 추가하기만 하면 됩니다(그리고 작업에 async 지원 라이브러리를 사용해야 합니다 - 여기서는 표준 라이브러리의 `sleep`을 `asyncio.sleep`으로 교체합니다):

```python hl_lines="1 4 5"
import asyncio

@api.get("/say-after")
async def say_after(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}
```

### 실행

이 코드를 실행하려면 <a href="https://www.uvicorn.org/" target="_blank">Uvicorn</a>이나 <a href="https://github.com/django/daphne" target="_blank">Daphne</a> 같은 ASGI 서버가 필요합니다. 여기서는 Uvicorn을 사용해 보겠습니다. 예제는 아래와 같습니다:

Uvicorn을 설치하려면 다음을 사용하세요:

```
pip install uvicorn
```

그다음 서버를 시작합니다:

```
uvicorn your_project.asgi:application --reload
```

> <small>
> *참고: `your_project`를 여러분의 프로젝트 패키지 이름으로 교체하세요*<br>
> *`--reload` 플래그는 코드를 변경할 때마다 서버를 자동으로 재시작하는 데 사용됩니다 (프로덕션에서는 사용하지 마세요)*
> </small>

!!! note
    비동기 뷰는 `manage.py runserver`로도 실행할 수 있지만, 일부 라이브러리와 잘 호환되지 않으므로, 현재 시점(2020년 7월)에는 Uvicorn이나 Daphne 같은 ASGI 서버를 사용하는 것이 권장됩니다.

### 테스트

브라우저에서 <a href="http://127.0.0.1:8000/api/say-after?delay=3&word=hello" target="_blank">http://127.0.0.1:8000/api/say-after?delay=3&word=hello</a> (**delay=3**) 를 열어 보세요.
3초를 기다린 후 "hello" 메시지가 표시될 것입니다.

이제 이 operation에 **100개의 병렬 요청**을 몰아넣어 보겠습니다:

```
ab -c 100 -n 100 "http://127.0.0.1:8000/api/say-after?delay=3&word=hello"
```

이렇게 하면 다음과 같은 결과가 나옵니다:

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

이 수치에 따르면, 우리 서비스는 약간의 오버헤드만으로 100개의 동시 요청을 처리할 수 있습니다.

WSGI와 동기 operation으로 동일한 동시성을 달성하려면 각각 10개의 스레드를 가진 약 10개의 worker를 시작해야 할 것입니다!

## 동기와 비동기 operation 혼합

프로젝트에서 **동기와 비동기 operation을 함께 사용할 수 있고**, **Django Ninja**가 이를 자동으로 라우팅한다는 점을 기억하세요:

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

## Elasticsearch 예제

실제 사용 사례를 살펴보겠습니다. 이 예제에서는 async 지원이 포함된 최신 버전의 Elasticsearch를 사용해 보겠습니다:
```
pip install elasticsearch>=7.8.0
```

이제 `Elasticsearch` 클래스 대신 `AsyncElasticsearch` 클래스를 사용하고 결과에 `await`를 적용하세요:

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

## ORM 사용

현재 Django의 특정 핵심 부분은 코루틴을 인식하지 못하는 전역 상태를 가지고 있어 비동기 환경에서 안전하게 동작할 수 없습니다. Django의 이러한 부분은 "비동기 안전하지 않음(asynchronous-unsafe)"으로 분류되며 비동기 환경에서의 실행이 차단됩니다. **ORM**이 대표적인 예이지만, 이런 방식으로 보호되는 다른 부분들도 있습니다.
비동기 안전성에 대해 자세히 알아보려면 <a href="https://docs.djangoproject.com/en/stable/topics/async/#async-safety" target="_blank">Django 공식 문서</a>를 참조하세요.

따라서 다음과 같이 하면:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = Blog.objects.get(pk=post_id)
    ...
```

에러가 발생합니다. 비동기 ORM 구현이 제공되기 전까지는 `sync_to_async()` 어댑터를 사용할 수 있습니다:

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

또는 더 짧게:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await sync_to_async(Blog.objects.get)(pk=post_id)
    ...
```

흔히 겪는 **함정**이 하나 있습니다. Django queryset은 지연 평가(lazy evaluation)되므로(데이터베이스 쿼리는 이터레이션을 시작할 때만 발생합니다), 다음 코드는 동작하지 **않습니다**:

```python
all_blogs = await sync_to_async(Blog.objects.all)()
# it will throw an error later when you try to iterate over all_blogs
...
```

대신 (`list`로) 강제 평가하세요:

```python
all_blogs = await sync_to_async(list)(Blog.objects.all())
...
```

Django **버전 4.1**부터 Django는 ORM operation의 비동기 버전을 기본 제공합니다.
이를 통해 대부분의 경우 `sync_to_async`를 사용할 필요가 없어졌습니다.
비동기 operation은 동기 버전과 이름이 같지만 접두사 *a*가 붙습니다. 따라서 위의 예제는 다음과 같이 다시 작성할 수 있습니다:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await Blog.objects.aget(pk=post_id)
    ...
```

queryset을 다룰 때는 `async for`를 리스트 컴프리헨션과 함께 사용하세요:

```python
all_blogs = [blog async for blog in Blog.objects.all()]
...
```

비동기 ORM 인터페이스에 대해 자세히 알아보려면 <a href="https://docs.djangoproject.com/en/4.1/releases/4.1/#asynchronous-orm-interface" target="_blank">Django 공식 문서</a>를 참조하세요.

!!! success

    다음 섹션 **[API 버저닝](versioning.md)**으로 계속 진행하세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
