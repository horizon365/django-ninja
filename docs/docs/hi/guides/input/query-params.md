---
comments: true
---
# Query Parameters

जब आप ऐसे function parameters घोषित करते हैं जो path parameters का हिस्सा नहीं हैं, तो उन्हें स्वचालित रूप से "query" parameters के रूप में व्याख्यायित किया जाता है।
```python hl_lines="5"
{!./src/tutorial/query/code01.py!}
```

इस operation को query करने के लिए, आप इस तरह का एक URL उपयोग कर सकते हैं:

```
http://localhost:8000/api/weapons?offset=0&limit=10
```
डिफ़ॉल्ट रूप से, सभी GET parameters strings होते हैं; जब आप अपने function parameters को types के साथ annotate करते हैं, तो उन्हें उस type में बदल दिया जाएगा और उसके विरुद्ध validate किया जाएगा।

वही लाभ जो path parameters पर लागू होते हैं, वे query parameters पर भी लागू होते हैं:

- Editor समर्थन (जाहिर है)
- Data "parsing"
- Data validation
- Automatic दस्तावेज़ीकरण


!!! note
    यदि आप अपने parameters को annotate नहीं करते, तो उन्हें `str` type माना जाएगा

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit, offset):
    # type(limit) == str
    # type(offset) == str
```

### डिफ़ॉल्ट मान

चूँकि query parameters path का एक निश्चित हिस्सा नहीं होते, वे optional होते हैं और उनके डिफ़ॉल्ट मान हो सकते हैं:

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit: int = 10, offset: int = 0):
    return weapons[offset : offset + limit]
```

ऊपर दिए गए उदाहरण में, हमने `offset=0` और `limit=10` के डिफ़ॉल्ट मान सेट किए हैं।

तो, इस URL पर जाना:
```
http://localhost:8000/api/weapons
```
इस पर जाने के समान होगा:
```
http://localhost:8000/api/weapons?offset=0&limit=10
```
यदि आप, उदाहरण के लिए, इस पर जाते हैं:
```
http://localhost:8000/api/weapons?offset=20
```

तो आपके function में parameter मान होंगे:

 - `offset=20` (क्योंकि आपने इसे URL में सेट किया है)
 - `limit=10` (क्योंकि वह डिफ़ॉल्ट मान है)


### Required और Optional Parameters

आप required या optional GET parameters को उसी तरह घोषित कर सकते हैं जिस तरह आप Python function parameters घोषित करते हैं:

```python hl_lines="5"
{!./src/tutorial/query/code02.py!}
```

इस स्थिति में, **Django Ninja** हमेशा GET request में पास किए गए `q` parameter को validate करेगा, जबकि `offset` parameter एक optional पूर्णांक है।

### GET Parameter Type Conversion

आइए कई typed parameters घोषित करें:
```python hl_lines="5"
{!./src/tutorial/query/code03.py!}
```
`str` type as-is पास किया जाता है।

`bool` type के लिए, निम्नलिखित सभी:
```
http://localhost:8000/api/example?b=1
http://localhost:8000/api/example?b=True
http://localhost:8000/api/example?b=true
http://localhost:8000/api/example?b=on
http://localhost:8000/api/example?b=yes
```
या कोई अन्य case variation (uppercase, capitalized, आदि), आपके function को यह दिखाई देगा
कि parameter `b` का `bool` मान `True` है, अन्यथा `False`।

Dates date strings और पूर्णांक (Unix timestamps) हो सकते हैं:

<pre style="font-size: .85em; background-color:rgb(245, 245, 245);">
http://localhost:8000/api/example?d=<strong>1577836800</strong>  # equivalent to 2020-01-01
http://localhost:8000/api/example?d=<strong>2020-01-01</strong>
</pre>


### Schema का उपयोग करना

GET parameters को समाहित करने के लिए आप एक schema भी उपयोग कर सकते हैं:

```python hl_lines="1 2  5 6 7 8"
{!./src/tutorial/query/code010.py!}
```

अधिक जटिल filtering परिदृश्यों के लिए, [Filtering](./filtering.md) देखें।

!!! done

    अगले अध्याय पर जाएँ! **[Request Body](body.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
