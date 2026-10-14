---
comments: true
---
# Response Renderer

REST API에서 가장 흔한 응답 타입은 보통 JSON입니다.
**Django Ninja**는 커스텀 renderer를 정의하는 것도 지원하므로, 자신만의 media type을 설계할 수 있는 유연성을 얻을 수 있습니다.

## Renderer 만들기

자신만의 renderer를 만들려면 `ninja.renderers.BaseRenderer`를 상속하고 `render` 메서드를 오버라이드해야 합니다. 그다음 클래스의 인스턴스를 `renderer` 인자로 `NinjaAPI`에 전달할 수 있습니다:

```python hl_lines="5 8 9"
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer


class MyRenderer(BaseRenderer):
    media_type = "text/plain"

    def render(self, request, data, *, response_status):
        return ... # your serialization here

api = NinjaAPI(renderer=MyRenderer())
```

`render` 메서드는 다음 인자를 받습니다:

 - request -> HttpRequest 객체 
 - data -> 직렬화가 필요한 객체
 - response_status -> 클라이언트에 반환될 HTTP 상태 코드를 나타내는 `int`

또한 응답의 content-type 헤더를 설정하기 위해 클래스에 `media_type` 속성을 정의해야 합니다.


## ORJSON Renderer 예제:

[orjson](https://github.com/ijl/orjson#orjson)은 Python을 위한 빠르고 정확한 JSON 라이브러리입니다.
벤치마크에서 가장 빠른 Python JSON 라이브러리이며, 표준 `json` 라이브러리나 다른 서드파티 라이브러리보다 정확합니다. 
dataclass, datetime, numpy, UUID 인스턴스도 네이티브로 직렬화할 수 있습니다.

`orjson`을 사용하는 renderer 클래스의 예제는 다음과 같습니다:


```python hl_lines="9 10"
import orjson
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer


class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data)

api = NinjaAPI(renderer=ORJSONRenderer())
```



## XML Renderer 예제:


모든 응답을 XML로 출력하는 renderer를 만드는 방법은 다음과 같습니다:

```python hl_lines="8 11"
from io import StringIO
from django.utils.encoding import force_str
from django.utils.xmlutils import SimplerXMLGenerator
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer


class XMLRenderer(BaseRenderer):
    media_type = "text/xml"

    def render(self, request, data, *, response_status):
        stream = StringIO()
        xml = SimplerXMLGenerator(stream, "utf-8")
        xml.startDocument()
        xml.startElement("data", {})
        self._to_xml(xml, data)
        xml.endElement("data")
        xml.endDocument()
        return stream.getvalue()

    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                xml.startElement("item", {})
                self._to_xml(xml, item)
                xml.endElement("item")

        elif isinstance(data, dict):
            for key, value in data.items():
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key)

        elif data is None:
            # Don't output any value
            pass

        else:
            xml.characters(force_str(data))


api = NinjaAPI(renderer=XMLRenderer())
```
*(Credit: this code is basically copied from [DRF-xml](https://jpadilla.github.io/django-rest-framework-xml/))*

!!! done

    응답 처리 시리즈가 완료되었습니다! 다음 섹션 **[라우터로 API 분할하기](../routers.md)**로 계속 진행하세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
