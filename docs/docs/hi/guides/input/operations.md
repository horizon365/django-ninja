---
comments: true
---
# HTTP Methods

## Operations को परिभाषित करना

एक `operation` [HTTP methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) में से कोई एक हो सकता है:

- GET (retrieve)
- POST (submit)
- PUT (update)
- DELETE (delete)
- PATCH (partial update)

**Django Ninja** में प्रत्येक operation के लिए एक decorator है:

```python hl_lines="1 5 9 13 17"
@api.get("/path")
def get_operation(request):
    ...

@api.post("/path")
def post_operation(request):
    ...

@api.put("/path")
def put_operation(request):
    ...

@api.delete("/path")
def delete_operation(request):
    ...

@api.patch("/path")
def patch_operation(request):
    ...
```

इनमें से किसी भी decorator को क्या पास किया जा सकता है, इसकी जानकारी के लिए [Operation Parameters](../../reference/operations-parameters.md) reference दस्तावेज़ीकरण देखें।

## कई Methods को संभालना

यदि आपको किसी दिए गए path के लिए एक ही function से कई methods संभालने हैं, तो आप `api_operation` decorator का उपयोग कर सकते हैं:

```python hl_lines="1"
@api.api_operation(["POST", "PATCH"], "/path")
def mixed_operation(request):
    ...
```

इस सुविधा का उपयोग अन्य ऐसे HTTP methods को implement करने के लिए भी किया जा सकता है जिनके लिए **Django Ninja** का कोई method नहीं है, जैसे `HEAD` या `OPTIONS`।

```python hl_lines="1"
@api.api_operation(["HEAD", "OPTIONS"], "/path")
def mixed_operation(request):
    ...
```

!!! done

    अगले अध्याय पर जाएँ! **[Path Parameters](path-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
