---
comments: true
---
# Tutorial - Input parameters को handle करना

## Query string से parameters pass करना

आइए operation को बदलें ताकि वह URL query string से एक name accept कर सके। ऐसा करने के लिए, बस अपने function में एक `name` argument जोड़ें।

```python
@api.get("/hello")
def hello(request, name):
    return f"Hello {name}"
```

जब हम named argument provide करते हैं, तो हमें अपेक्षित (HTTP 200) response मिलता है।

<a href="http://localhost:8000/api/hello?name=you"
target="_blank">localhost:8000/api/hello?name=you</a>:

```json
"Hello you"
```

### Default values

अगर आप parameter provide नहीं करते, तो एक HTTP 422 error response return होता है।

*[HTTP 422]: Unprocessable Entity

<a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a>:

```json
{
  "detail": [
    {
      "loc": ["query", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

हम `name` argument के लिए एक default value specify कर सकते हैं, ताकि अगर वह न दिया गया हो तो भी काम चले:

```python hl_lines="2"
@api.get("/hello")
def hello(request, name="world"):
    return f"Hello {name}"
```

## Input types

**Django Ninja** input types को format करने के लिए standard [Python type hints](https://docs.python.org/3/library/typing.html) का इस्तेमाल करता है। अगर कोई type नहीं दिया गया है, तो string मान लिया जाता है (लेकिन सभी arguments के लिए type hints देना best practice है)।

आइए एक दूसरा operation जोड़ें जो integers के साथ कुछ बुनियादी math करता है।

```python hl_lines="5-7"
@api.get("/hello")
def hello(request, name: str = "world"):
    return f"Hello {name}"

@api.get("/math")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

<a href="http://localhost:8000/api/math?a=2&b=3"
target="_blank">localhost:8000/api/math?a=2&b=3</a>:

```json
{
  "add": 5,
  "multiply": 6
}
```

## Path strings के ज़रिए parameters pass करना

आप Python format strings के समान syntax का इस्तेमाल करके path "parameters" declare कर सकते हैं।

Path string में मिला कोई भी parameter query string से लिए जाने की बजाय आपके function को एक argument के रूप में pass किया जाएगा।

```python hl_lines="1"
@api.get("/math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

अब हम <a href="http://localhost:8000/api/math/2and3"
target="_blank">localhost:8000/api/math/2and3</a> के ज़रिए math operation को access करते हैं।


## Request body के ज़रिए parameters pass करना

हम `hello` operation को बदलकर एक HTTP `POST` request का इस्तेमाल करने वाला बनाएँगे, और parameters को request body से लेंगे।

यह specify करने के लिए कि parameters request body से आते हैं, हमें एक schema declare करना होगा।

*[Schema]: Pydantic "Model" का एक extension

```python hl_lines="1 5-6 8-10"
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class HelloSchema(Schema):
    name: str = "world"

@api.post("/hello")
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"
```

### Self-documenting API

अब <a href="http://localhost:8000/api/hello" target="_blank">localhost:8000/api/hello</a> पर जाने पर एक HTTP 405 error response मिलेगा, क्योंकि हमें इस URL पर किए जाने वाले request को POST type में बदलना है।

*[HTTP 405]: Method Not Allowed

ऐसा करने का एक आसान तरीका है Swagger documentation का इस्तेमाल करना जो हमारे लिए automatically बन जाती है, default "/docs" URL पर (हमारे API URL root के आगे जुड़ा हुआ)।

1. <a href="http://localhost:8000/api/docs" target="_blank">localhost:8000/api/docs</a> पर जाएँ और उन operations को देखें जो हमने बनाए
1. `/api/hello` operation खोलें
2. "Try it out" पर click करें
3. Request body को modify करें
4. "Execute" पर click करें

!!! success

    अगले chapter **[Responses को handle करना](step3.md)** पर बढ़ें।
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
