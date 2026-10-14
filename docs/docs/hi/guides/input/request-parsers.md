---
comments: true
---
# Request Parsers

अधिकांश स्थितियों में, एक REST API के लिए डिफ़ॉल्ट content type JSON होता है, लेकिन यदि आपको अन्य content types संभालने हैं (जैसे YAML, XML, CSV) या एक तेज़ JSON parser का उपयोग करना है, तो **Django Ninja** एक `parser` configuration प्रदान करता है।

```python
api = NinjaAPI(parser=MyYamlParser())
```

अपना खुद का parser बनाने के लिए, आपको `ninja.parser.Parser` class को extend करना होगा और `parse_body` method को override करना होगा।


## YAML Parser उदाहरण

आइए अपना custom YAML parser बनाएँ:

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

यदि आप अब YAML को इस तरह request body के रूप में भेजते हैं:

```YAML
ints:
 - 0
 - 1
string: hello
f: 3.14
```

तो इसे सही ढंग से parse किया जाएगा, और आपको इस तरह का JSON आउटपुट मिलेगा:


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


## ORJSON Parser उदाहरण

[orjson](https://github.com/ijl/orjson#orjson) Python के लिए एक तेज़, सटीक JSON library है। यह benchmarks में सबसे तेज़ Python JSON library है, और standard `json` library या अन्य third-party libraries से अधिक सटीक है।

```
pip install orjson
```

Parser का code:

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

    अगले अध्याय पर जाएँ! **[Filtering](filtering.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
