---
comments: true
---
# 튜토리얼 - 입력 파라미터 처리하기

## Query string에서 파라미터 전달받기

URL query string에서 name을 받아들이도록 operation을 수정해 보겠습니다. 이를 위해서는 함수에 `name` 인자를 추가하기만 하면 됩니다.

```python
@api.get("/hello")
def hello(request, name):
    return f"Hello {name}"
```

이름이 지정된 인자를 제공하면 기대했던 (HTTP 200) 응답을 받습니다.

<a href="http://localhost:8000/api/hello?name=you"
target="_blank">localhost:8000/api/hello?name=you</a>:

```json
"Hello you"
```

### 기본값

파라미터를 제공하지 않으면 HTTP 422 에러 응답이 반환됩니다.

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

`name` 인자가 제공되지 않는 경우를 대비해 기본값을 지정할 수 있습니다:

```python hl_lines="2"
@api.get("/hello")
def hello(request, name="world"):
    return f"Hello {name}"
```

## 입력 타입

**Django Ninja**는 표준 [Python type hints](https://docs.python.org/3/library/typing.html)를 사용하여 입력 타입을 형식화합니다. 타입이 제공되지 않으면 문자열로 가정합니다 (하지만 모든 인자에 타입 힌트를 제공하는 것이 best practice입니다).

정수로 기본적인 수학 연산을 수행하는 두 번째 operation을 추가해 보겠습니다.

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

## Path string으로 파라미터 전달하기

Python format string과 동일한 문법을 사용하여 path "파라미터"를 선언할 수 있습니다.

path string에서 발견된 파라미터는 query string에서 가져오는 대신, 함수의 인자로 전달됩니다.

```python hl_lines="1"
@api.get("/math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

이제 <a href="http://localhost:8000/api/math/2and3"
target="_blank">localhost:8000/api/math/2and3</a>를 통해 math operation에 접근합니다.


## Request body로 파라미터 전달하기

`hello` operation을 HTTP `POST` 요청을 사용하도록 변경하고, 파라미터를 request body에서 가져오도록 하겠습니다.

파라미터가 request body에서 온다는 것을 지정하려면 schema를 선언해야 합니다.

*[Schema]: Pydantic "Model"의 확장

```python hl_lines="1 5-6 8-10"
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class HelloSchema(Schema):
    name: str = "world"

@api.post("/hello")
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"
```

### 스스로 문서화되는 API

이제 <a href="http://localhost:8000/api/hello" target="_blank">localhost:8000/api/hello</a>에 접근하면 HTTP 405 에러 응답이 발생합니다. 이 URL로 보내는 요청을 POST 타입으로 변경해야 하기 때문입니다.

*[HTTP 405]: Method Not Allowed

이를 쉽게 하는 방법은, 기본 "/docs" URL(우리의 API URL 루트에 붙는)에서 자동으로 생성된 Swagger 문서를 사용하는 것입니다.

1. <a href="http://localhost:8000/api/docs" target="_blank">localhost:8000/api/docs</a>에 방문하여 생성한 operation들을 확인합니다
1. `/api/hello` operation을 엽니다
2. "Try it out"을 클릭합니다
3. Request body를 수정합니다
4. "Execute"를 클릭합니다

!!! success

    다음 장 **[응답 처리하기](step3.md)**로 계속 진행하세요.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
