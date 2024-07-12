---
comments: true
---
# 教程 - 解析传入的参数

## 来自查询字符串的传参

让我们将操作修改为从 URL 的查询字符串中接受一个名称。为此，只需在我们的函数中添加一个 `name` 参数。

```python
@api.get("/hello")
def hello(request, name):
    return f"Hello {name}"
```

当我们提供命名参数时，我们会得到预期的 (HTTP 200) 响应。

<a href="http://localhost:8000/api/hello?name=you"
target="_blank">localhost:8000/api/hello?name=you</a>:

```json
"Hello you"
```

### 默认值

如果不提供该参数，将返回 HTTP 422 错误响应。

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

我们可以为 `name` 参数指定一个默认值，以防没有提供：

```python hl_lines="2"
@api.get("/hello")
def hello(request, name="world"):
    return f"Hello {name}"
```

## 输入类型

**Django Ninja** 使用标准的 [Python type hints](https://docs.python.org/3/library/typing.html) 来格式化输入类型。如果没有提供类型，则假定为字符串 (但为所有参数提供类型提示是最佳实践)。

让我们添加第二个操作，用整数进行一些基本的数学运算。

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

## 通过路径字符串传参

你可以使用与 Python 格式化字符串相同的语法来声明路径“参数”。

在路径字符串中找到的任何参数将作为参数传递给你的函数，而不是从查询字符串中获得它们。

```python hl_lines="1"
@api.get("/math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

现在我们通过 <a href="http://localhost:8000/api/math/2and3"
target="_blank">localhost:8000/api/math/2and3</a> 来访问数学操作。


## 通过请求体传参

我们将把 `hello` 操作改为使用 HTTP `POST` 请求， 并从请求体中获取参数。

为了指定参数来自请求体，我们需要声明一个模式。

*[Schema]: An extension of a Pydantic "Model"

```python hl_lines="1 5-6 8-10"
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class HelloSchema(Schema):
    name: str = "world"

@api.post("/hello")
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"
```

### 自文档化的 API

现在访问 <a href="http://localhost:8000/api/hello" target="_blank">localhost:8000/api/hello</a> 会导致 HTTP 405 错误响应，因为我们需要将向此 URL 发起的请求改为 POST 类型。

*[HTTP 405]: Method Not Allowed

一种简单的方法是使用自动为我们创建的 Swagger 文档，在默认的“/docs”URL（附加到我们的 API 网址根）。

1. 访问 <a href="http://localhost:8000/api/docs" target="_blank">localhost:8000/api/docs</a> 查看我们创建的操作
1. 打开 `/api/hello` 操作
2. 点击 "Try it out"
3. 更改请求体
4. 点击 "Execute"

!!! 大功告成

    继续下一章节 **[处理响应](step3.md)**
<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
