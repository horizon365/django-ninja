---
comments: true
---
# Учебник — Обработка входных параметров

## Передача параметров из строки запроса (query string)

Давайте изменим операцию так, чтобы она принимала имя из строки запроса URL. Для этого просто добавьте аргумент `name` в нашу функцию.

```python
@api.get("/hello")
def hello(request, name):
    return f"Hello {name}"
```

Когда мы передаём именованный аргумент, мы получаем ожидаемый (HTTP 200) ответ.

<a href="http://localhost:8000/api/hello?name=you"
target="_blank">localhost:8000/api/hello?name=you</a>:

```json
"Hello you"
```

### Значения по умолчанию

Если вы не передадите параметр, будет возвращён ответ с ошибкой HTTP 422.

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

Мы можем указать значение по умолчанию для аргумента `name` на случай, если он не передан:

```python hl_lines="2"
@api.get("/hello")
def hello(request, name="world"):
    return f"Hello {name}"
```

## Типы входных данных

**Django Ninja** использует стандартные [подсказки типов Python](https://docs.python.org/3/library/typing.html) для определения типов входных данных. Если тип не указан, предполагается строка (но указывать подсказки типов для всех аргументов — лучшая практика).

Давайте добавим вторую операцию, выполняющую базовые вычисления с целыми числами.

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

## Передача параметров через строки пути (path)

Вы можете объявлять «параметры» пути, используя тот же синтаксис, что и строки форматирования Python.

Любой параметр, найденный в строке пути, будет передан в вашу функцию как аргумент, а не взят из строки запроса.

```python hl_lines="1"
@api.get("/math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

Теперь мы обращаемся к операции math через <a href="http://localhost:8000/api/math/2and3"
target="_blank">localhost:8000/api/math/2and3</a>.


## Передача параметров через тело запроса

Мы изменим операцию `hello` так, чтобы она использовала HTTP-запрос `POST`, и получала параметры из тела запроса.

Чтобы указать, что параметры приходят из тела запроса, нужно объявить схему.

*[Schema]: Расширение «Model» из Pydantic

```python hl_lines="1 5-6 8-10"
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class HelloSchema(Schema):
    name: str = "world"

@api.post("/hello")
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"
```

### Самодокументирующееся API

Теперь обращение к <a href="http://localhost:8000/api/hello" target="_blank">localhost:8000/api/hello</a> приведёт к ответу с ошибкой HTTP 405, потому что нам нужно изменить тип запроса к этому URL на POST.

*[HTTP 405]: Method Not Allowed

Простой способ сделать это — использовать документацию Swagger, которая автоматически создаётся для нас, по URL «/docs» по умолчанию (добавляемому к корню нашего API URL).

1. Откройте <a href="http://localhost:8000/api/docs" target="_blank">localhost:8000/api/docs</a>, чтобы увидеть созданные нами операции
1. Откройте операцию `/api/hello`
2. Нажмите «Try it out»
3. Измените тело запроса
4. Нажмите «Execute»

!!! success

    Продолжайте со следующей главы **[Обработка ответов](step3.md)**
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
