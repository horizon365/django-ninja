---
comments: true
---
# Request Parsers

Dalam kebanyakan kasus, content type default untuk REST API adalah JSON, tetapi jika Anda perlu menangani content type lain (seperti YAML, XML, CSV) atau menggunakan JSON parser yang lebih cepat, **Django Ninja** menyediakan konfigurasi `parser`.

```python
api = NinjaAPI(parser=MyYamlParser())
```

Untuk membuat parser Anda sendiri, Anda perlu mewarisi class `ninja.parser.Parser` dan meng-override method `parse_body`.


## Contoh YAML Parser

Mari kita buat YAML parser kustom kita:

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

Jika sekarang Anda mengirim YAML sebagai request body seperti ini:

```YAML
ints:
 - 0
 - 1
string: hello
f: 3.14
```

YAML tersebut akan di-parsing dengan benar, dan Anda akan mendapatkan output JSON seperti ini:


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


## Contoh ORJSON Parser

[orjson](https://github.com/ijl/orjson#orjson) adalah library JSON yang cepat dan akurat untuk Python. Library ini adalah library JSON Python tercepat dalam benchmark, dan lebih akurat daripada library `json` standar atau library pihak ketiga lainnya.

```
pip install orjson
```

Kode parser-nya:

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

    Lanjutkan ke bab berikutnya! **[Filtering](filtering.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
