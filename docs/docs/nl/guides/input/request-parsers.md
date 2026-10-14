---
comments: true
---
# Request Parsers

In de meeste gevallen is het standaard content type voor een REST API JSON, maar als je andere content types moet afhandelen (zoals YAML, XML, CSV) of een snellere JSON parser wilt gebruiken, biedt **Django Ninja** een `parser` configuratie.

```python
api = NinjaAPI(parser=MyYamlParser())
```

Om je eigen parser te maken, moet je de class `ninja.parser.Parser` uitbreiden en de methode `parse_body` overriden.


## Voorbeeld YAML Parser

Laten we onze eigen YAML parser maken:

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

Als je nu YAML als request body verstuurt zoals hieronder:

```YAML
ints:
 - 0
 - 1
string: hello
f: 3.14
```

Dan wordt het correct geparseerd en zou je JSON output moeten krijgen zoals deze:


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


## Voorbeeld ORJSON Parser

[orjson](https://github.com/ijl/orjson#orjson) is een snelle en nauwkeurige JSON library voor Python. Het is de snelste Python JSON library in benchmarks, en nauwkeuriger dan de standaard `json` library of andere third-party libraries.

```
pip install orjson
```

De parser code:

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

    Ga verder naar het volgende hoofdstuk! **[Filtering](filtering.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
