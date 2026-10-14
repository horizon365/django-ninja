---
comments: true
---
# Response Renderers

Voor een REST API is het meest voorkomende response type doorgaans JSON.
**Django Ninja** ondersteunt ook het definiëren van je eigen aangepaste renderers, wat je de flexibiliteit geeft om je eigen media types te ontwerpen.

## Een Renderer Maken

Om je eigen renderer te maken, moet je overerven van `ninja.renderers.BaseRenderer` en de methode `render` overriden. Daarna kun je een instantie van je class als argument `renderer` doorgeven aan `NinjaAPI`:

```python hl_lines="5 8 9"
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer


class MyRenderer(BaseRenderer):
    media_type = "text/plain"

    def render(self, request, data, *, response_status):
        return ... # your serialization here

api = NinjaAPI(renderer=MyRenderer())
```

De methode `render` accepteert de volgende argumenten:

 - request -> het HttpRequest object 
 - data -> het object dat geserialiseerd moet worden
 - response_status -> een `int` die de HTTP statuscode vertegenwoordigt die naar de client wordt teruggegeven

Je moet ook het attribuut `media_type` op de class definiëren om de content-type header van de response in te stellen.


## ORJSON Renderer Voorbeeld:

[orjson](https://github.com/ijl/orjson#orjson) is een snelle en nauwkeurige JSON library voor Python.
Het is de snelste Python JSON library in benchmarks, en nauwkeuriger dan de standaard `json` library of andere third-party libraries. 
Het kan ook native dataclasses, datetimes, numpy en UUID instanties serialiseren.

Hier is een voorbeeld renderer class met `orjson`:


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



## XML Renderer Voorbeeld:


Zo kun je een renderer maken die alle responses als XML uitvoert:

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
*(Credit: deze code is in wezen gekopieerd van [DRF-xml](https://jpadilla.github.io/django-rest-framework-xml/))*

!!! done

    De reeks over het verwerken van responses is compleet! Ga verder naar de volgende sectie **[API's Splitsen via Routers](../routers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
