---
comments: true
---
# Request Parsers

In most cases, the default content type for a REST API is JSON, but if you need to handle other content types (such as YAML, XML, CSV) or use a faster JSON parser, **Django Ninja** provides a `parser` configuration.

```python
api = NinjaAPI(parser=MyYamlParser())
```

To create your own parser, you need to extend the `ninja.parser.Parser` class and override the `parse_body` method.


## Example YAML Parser

Let's create our custom YAML parser:

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

If you now send YAML as the request body like this:

```YAML
ints:
 - 0
 - 1
string: hello
f: 3.14
```

It will be parsed correctly, and you should get JSON output like this:


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


## Example ORJSON Parser

[orjson](https://github.com/ijl/orjson#orjson) is a fast, accurate JSON library for Python. It is the fastest Python JSON library in benchmarks, and more accurate than the standard `json` library or other third-party libraries.

```
pip install orjson
```

The parser code:

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

    Continue to the next chapter! **[Filtering](filtering.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
