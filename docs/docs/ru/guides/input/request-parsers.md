---
comments: true
---
# Парсеры запросов

В большинстве случаев тип содержимого по умолчанию для REST API — JSON, но если вам нужно обрабатывать другие типы содержимого (например, YAML, XML, CSV) или использовать более быстрый JSON-парсер, **Django Ninja** предоставляет конфигурацию `parser`.

```python
api = NinjaAPI(parser=MyYamlParser())
```

Чтобы создать свой собственный парсер, нужно унаследовать класс `ninja.parser.Parser` и переопределить метод `parse_body`.


## Пример парсера YAML

Создадим свой парсер YAML:

```python hl_lines="4 8 9"
import yaml
from typing import List
from ninja import NinjaAPI
from ninja.parser import Parser


class MyYamlParser(Parser):
    def parse_body(self, request):
        return yaml.safe_load(request.body)


api = NinjaAPI(parser=MyYamlParser())


class Payload(Schema):
    ints: List[int]
    string: str
    f: float


@api.post('/yaml')
def operation(request, payload: Payload):
    return payload.dict()


```

Если теперь отправить YAML в теле запроса, например так:

```YAML
ints:
 - 0
 - 1
string: hello
f: 3.14
```

Он будет разобран корректно, и вы получите JSON-вывод следующего вида:


```JSON
{
  "ints": [
    0,
    1
  ],
  "string": "hello",
  "f": 3.14
}
```


## Пример парсера ORJSON

[orjson](https://github.com/ijl/orjson#orjson) — это быстрая и точная JSON-библиотека для Python. Она является самой быстрой JSON-библиотекой Python в бенчмарках и точнее, чем стандартная библиотека `json` или другие сторонние библиотеки.

```
pip install orjson
```

Код парсера:

```python hl_lines="1 8 9"
import orjson
from ninja import NinjaAPI
from ninja.parser import Parser


class ORJSONParser(Parser):
    def parse_body(self, request):
        return orjson.loads(request.body)


api = NinjaAPI(parser=ORJSONParser())
```

!!! done

    Переходите к следующей главе! **[Фильтрация](filtering.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
