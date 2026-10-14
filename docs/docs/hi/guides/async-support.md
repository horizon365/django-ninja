---
comments: true
---
## परिचय

**version 3.1** से, Django **asynchronous view support** के साथ आता है। यह आपको ऐसे कुशल concurrent views चलाने की सुविधा देता है जो network- और/या I/O-bound होते हैं।

```
pip install Django>=3.1 django-ninja
```

Asynchronous views इन स्थितियों में अधिक कुशलता से काम करते हैं:
- Network के माध्यम से external APIs को कॉल करना
- Database queries निष्पादित करना/उनकी प्रतीक्षा करना
- Disk drives पर पढ़ना/लिखना

**Django Ninja** asynchronous views को पूरी तरह अपनाता है और उन्हें उपयोग करना बहुत आसान बनाता है।

## त्वरित उदाहरण

### Code

एक उदाहरण लेते हैं। हमारे पास एक API operation है जो कुछ काम करता है (अभी के लिए, बस दिए गए सेकंडों के लिए sleep करता है) और एक शब्द लौटाता है:
```python hl_lines="5"
import time

@api.get("/say-after")
def say_after(request, delay: int, word: str):
    time.sleep(delay)
    return {"saying": word}
```

इस code को asynchronously चलाने के लिए, आपको बस function में **`async`** keyword जोड़ना है (और काम के लिए एक async-aware library का उपयोग करना है - हमारे मामले में हम standard library के `sleep` को `asyncio.sleep` से बदल देते हैं):

```python hl_lines="1 4 5"
import asyncio

@api.get("/say-after")
async def say_after(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}
```

### चलाना

इस code को चलाने के लिए, आपको <a href="https://www.uvicorn.org/" target="_blank">Uvicorn</a> या <a href="https://github.com/django/daphne" target="_blank">Daphne</a> जैसे ASGI server की आवश्यकता है। आइए यहाँ Uvicorn का उपयोग करें, उदाहरण नीचे है:

Uvicorn इंस्टॉल करने के लिए, उपयोग करें:

```
pip install uvicorn
```

फिर server शुरू करें:

```
uvicorn your_project.asgi:application --reload
```

> <small>
> *ध्यान दें: `your_project` को अपने project के package नाम से बदलें*<br>
> *`--reload` flag का उपयोग code में कोई भी बदलाव करने पर server को स्वचालित रूप से reload करने के लिए किया जाता है (production में उपयोग न करें)*
> </small>

!!! note
    आप `manage.py runserver` के साथ asynchronous views चला सकते हैं, लेकिन यह कुछ libraries के साथ अच्छी तरह काम नहीं करता है, इसलिए इस समय (July 2020) Uvicorn या Daphne जैसे ASGI server का उपयोग करने की सलाह दी जाती है।

### Testing

अपने browser में <a href="http://127.0.0.1:8000/api/say-after?delay=3&word=hello" target="_blank">http://127.0.0.1:8000/api/say-after?delay=3&word=hello</a> (**delay=3**) खोलें।
3 सेकंड प्रतीक्षा करने के बाद, आपको "hello" संदेश दिखाई देना चाहिए।

अब आइए इस operation को **100 parallel requests** से भर दें:

```
ab -c 100 -n 100 "http://127.0.0.1:8000/api/say-after?delay=3&word=hello"
```

इससे इस तरह का परिणाम आएगा:

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

इन आंकड़ों के अनुसार, हमारी service थोड़े से overhead के साथ इन 100 concurrent requests को संभालने में सक्षम है।

WSGI और synchronous operations के साथ वही concurrency प्राप्त करने के लिए, आपको लगभग 10 workers प्रत्येक में 10 threads के साथ शुरू करने पड़ते!

## Synchronous और asynchronous operations को मिलाना

ध्यान रखें कि आप अपने project में **sync और async दोनों operations का उपयोग कर सकते हैं**, और **Django Ninja** उन्हें स्वचालित रूप से route करेगा:

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

## Elasticsearch उदाहरण

आइए एक वास्तविक दुनिया का उपयोग का मामला लेते हैं। इस उदाहरण के लिए, हम Elasticsearch का हालिया version उपयोग करेंगे जो async support के साथ आता है:
```
pip install elasticsearch>=7.8.0
```

अब, `Elasticsearch` class का उपयोग करने के बजाय, `AsyncElasticsearch` class का उपयोग करें और परिणाम का `await` करें:

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

## ORM का उपयोग करना

वर्तमान में, Django के कुछ महत्वपूर्ण हिस्से asynchronous वातावरण में सुरक्षित रूप से संचालित नहीं हो सकते क्योंकि उनके पास ऐसा global state है जो coroutine-aware नहीं है। Django के इन हिस्सों को "asynchronous-unsafe" के रूप में वर्गीकृत किया गया है और इन्हें asynchronous वातावरण में निष्पादन से सुरक्षित रखा गया है। **ORM** इसका मुख्य उदाहरण है, लेकिन अन्य हिस्से भी हैं जो इस तरह से सुरक्षित हैं।
Async safety के बारे में अधिक जानें <a href="https://docs.djangoproject.com/en/stable/topics/async/#async-safety" target="_blank">Django आधिकारिक दस्तावेज़ीकरण</a> में।

तो यदि आप ऐसा करते हैं:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = Blog.objects.get(pk=post_id)
    ...
```

तो यह एक error फेंकेगा। Async ORM implementation उपलब्ध होने तक, आप `sync_to_async()` adapter का उपयोग कर सकते हैं:

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

या इससे भी छोटा:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await sync_to_async(Blog.objects.get)(pk=post_id)
    ...
```

यहाँ एक सामान्य **pitfall** है: Django querysets का मूल्यांकन आलसी (lazily) तरीके से होता है (database query केवल तब होती है जब आप उन पर iterate करना शुरू करते हैं), इसलिए यह **काम नहीं** करेगा:

```python
all_blogs = await sync_to_async(Blog.objects.all)()
# it will throw an error later when you try to iterate over all_blogs
...
```

इसके बजाय, मूल्यांकन को बाध्य करें (`list` के साथ):

```python
all_blogs = await sync_to_async(list)(Blog.objects.all())
...
```

Django **version 4.1** से, Django ORM operations के asynchronous संस्करणों के साथ आता है।
ये अधिकांश स्थितियों में `sync_to_async` का उपयोग करने की आवश्यकता को समाप्त कर देते हैं।
Asynchronous operations के नाम उनके synchronous समकक्षों के समान हैं, बस *a* prefix के साथ। तो ऊपर दिए गए उदाहरण का उपयोग करते हुए,
आप इसे इस प्रकार फिर से लिख सकते हैं:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await Blog.objects.aget(pk=post_id)
    ...
```

Querysets के साथ काम करते समय, list comprehension के साथ `async for` का उपयोग करें:

```python
all_blogs = [blog async for blog in Blog.objects.all()]
...
```

Asynchronous ORM interface के बारे में अधिक जानें <a href="https://docs.djangoproject.com/en/4.1/releases/4.1/#asynchronous-orm-interface" target="_blank">Django आधिकारिक दस्तावेज़ीकरण</a> में।

!!! success

    अगले भाग पर जाएँ **[API versioning](versioning.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
