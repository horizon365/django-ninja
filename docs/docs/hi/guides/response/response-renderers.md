---
comments: true
---
# Response Renderers

एक REST API के लिए, सबसे आम response type आमतौर पर JSON होता है।
**Django Ninja** अपने custom renderers परिभाषित करने का भी समर्थन करता है, जो आपको अपने खुद के media types डिज़ाइन करने की सुविधा देता है।

## एक Renderer बनाना

अपना खुद का renderer बनाने के लिए, आपको `ninja.renderers.BaseRenderer` से inherit करना होगा और `render` method को override करना होगा। फिर आप अपनी class का एक instance `renderer` argument के रूप में `NinjaAPI` को पास कर सकते हैं:

```python hl_lines="5 8 9"
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer


class MyRenderer(BaseRenderer):
    media_type = "text/plain"

    def render(self, request, data, *, response_status):
        return ... # your serialization here

api = NinjaAPI(renderer=MyRenderer())
```

`render` method निम्नलिखित arguments स्वीकार करता है:

 - request -> HttpRequest object
 - data -> वह object जिसे serialize करने की आवश्यकता है
 - response_status -> एक `int` जो client को लौटाए जाने वाले HTTP status code को दर्शाता है

आपको response की content-type header सेट करने के लिए class पर `media_type` attribute भी परिभाषित करना होगा।


## ORJSON Renderer उदाहरण:

[orjson](https://github.com/ijl/orjson#orjson) Python के लिए एक तेज़, सटीक JSON library है।
यह benchmarks में सबसे तेज़ Python JSON library है, और standard `json` library या अन्य third-party libraries से अधिक सटीक है।
यह dataclasses, datetimes, numpy, और UUID instances को natively serialize भी कर सकता है।

यहाँ `orjson` का उपयोग करने वाले एक renderer class का उदाहरण है:


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



## XML Renderer उदाहरण:


यहाँ बताया गया है कि आप सभी responses को XML के रूप में आउटपुट करने वाला एक renderer कैसे बना सकते हैं:

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
*(Credit: यह code मूल रूप से [DRF-xml](https://jpadilla.github.io/django-rest-framework-xml/) से लिया गया है)*

!!! done

    Handling response श्रृंखला पूरी हो गई है! अगले भाग पर जाएँ **[Splitting APIs via Routers](../routers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
