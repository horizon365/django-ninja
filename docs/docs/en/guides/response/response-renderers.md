---
comments: true
---
# Response Renderers

For a REST API, the most common response type is usually JSON.
**Django Ninja** also supports defining your own custom renderers, which gives you the flexibility to design your own media types.

## Creating a Renderer

To create your own renderer, you need to inherit from `ninja.renderers.BaseRenderer` and override the `render` method. Then you can pass an instance of your class as the `renderer` argument to `NinjaAPI`:

```python hl_lines="5 8 9"
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer


class MyRenderer(BaseRenderer):
    media_type = "text/plain"

    def render(self, request, data, *, response_status):
        return ... # your serialization here

api = NinjaAPI(renderer=MyRenderer())
```

The `render` method accepts the following arguments:

 - request -> the HttpRequest object 
 - data -> the object that needs to be serialized
 - response_status -> an `int` representing the HTTP status code that will be returned to the client

You also need to define the `media_type` attribute on the class to set the response's content-type header.


## ORJSON Renderer Example:

[orjson](https://github.com/ijl/orjson#orjson) is a fast, accurate JSON library for Python.
It is the fastest Python JSON library in benchmarks, and more accurate than the standard `json` library or other third-party libraries. 
It can also natively serialize dataclasses, datetimes, numpy, and UUID instances.

Here is an example renderer class using `orjson`:


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



## XML Renderer Example:


Here is how you can create a renderer that outputs all responses as XML:

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

    The handling response series is complete! Continue to the next section **[Splitting APIs via Routers](../routers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
