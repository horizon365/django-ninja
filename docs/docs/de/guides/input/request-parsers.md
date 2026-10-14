---
comments: true
---
# Request-Parser

In den meisten Fällen ist der Standard-Content-Type einer REST-API JSON, aber wenn Sie andere Content-Types verarbeiten müssen (wie YAML, XML, CSV) oder einen schnelleren JSON-Parser verwenden möchten, bietet **Django Ninja** eine `parser`-Konfiguration.

```python
api = NinjaAPI(parser=MyYamlParser())
```

Um Ihren eigenen Parser zu erstellen, müssen Sie die Klasse `ninja.parser.Parser` erweitern und die Methode `parse_body` überschreiben.


## Beispiel: YAML-Parser

Erstellen wir unseren eigenen YAML-Parser:

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

Wenn Sie nun YAML als Request Body wie folgt senden:

```YAML
ints:
 - 0
 - 1
string: hello
f: 3.14
```

Wird es korrekt geparst, und Sie sollten eine JSON-Ausgabe wie diese erhalten:


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


## Beispiel: ORJSON-Parser

[orjson](https://github.com/ijl/orjson#orjson) ist eine schnelle und präzise JSON-Bibliothek für Python. Sie ist in Benchmarks die schnellste Python-JSON-Bibliothek und genauer als die Standardbibliothek `json` oder andere Bibliotheken von Drittanbietern.

```
pip install orjson
```

Der Parser-Code:

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

    Weiter zum nächsten Kapitel! **[Filterung](filtering.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
