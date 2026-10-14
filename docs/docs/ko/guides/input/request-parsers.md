---
comments: true
---
# Request Parsers

대부분의 경우 REST API의 기본 content type은 JSON이지만, 다른 content type(예: YAML, XML, CSV)을 처리하거나 더 빠른 JSON 파서를 사용해야 하는 경우 **Django Ninja**가 `parser` 설정을 제공합니다.

```python
api = NinjaAPI(parser=MyYamlParser())
```

자신만의 파서를 만들려면 `ninja.parser.Parser` 클래스를 확장하고 `parse_body` 메서드를 오버라이드해야 합니다.


## YAML 파서 예제

커스텀 YAML 파서를 만들어 보겠습니다:

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

이제 다음과 같이 YAML을 request body로 보내면:

```YAML
ints:
 - 0
 - 1
string: hello
f: 3.14
```

올바르게 파싱되며 다음과 같은 JSON 출력을 얻을 수 있습니다:


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


## ORJSON 파서 예제

[orjson](https://github.com/ijl/orjson#orjson)은 Python을 위한 빠르고 정확한 JSON 라이브러리입니다. 벤치마크에서 가장 빠른 Python JSON 라이브러리이며, 표준 `json` 라이브러리나 다른 서드파티 라이브러리보다 정확합니다.

```
pip install orjson
```

파서 코드:

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

    다음 챕터로 계속 진행하세요! **[필터링](filtering.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
