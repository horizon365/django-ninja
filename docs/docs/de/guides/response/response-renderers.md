---
comments: true
---
# Response-Renderer

Bei einer REST-API ist der häufigste Response-Typ in der Regel JSON.
**Django Ninja** unterstützt auch die Definition eigener, benutzerdefinierter Renderer, womit Sie flexibel Ihre eigenen Media-Types gestalten können.

## Einen Renderer erstellen

Um Ihren eigenen Renderer zu erstellen, müssen Sie von `ninja.renderers.BaseRenderer` erben und die Methode `render` überschreiben. Anschließend können Sie eine Instanz Ihrer Klasse als Argument `renderer` an `NinjaAPI` übergeben:

```python hl_lines="5 8 9"
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer


class MyRenderer(BaseRenderer):
    media_type = "text/plain"

    def render(self, request, data, *, response_status):
        return ... # your serialization here

api = NinjaAPI(renderer=MyRenderer())
```

Die Methode `render` nimmt die folgenden Argumente entgegen:

 - request -> das HttpRequest-Objekt 
 - data -> das Objekt, das serialisiert werden muss
 - response_status -> ein `int`, der den HTTP-Statuscode darstellt, der an den Client zurückgegeben wird

Sie müssen außerdem das Attribut `media_type` an der Klasse definieren, um den Content-Type-Header der Response zu setzen.


## Beispiel: ORJSON-Renderer

[orjson](https://github.com/ijl/orjson#orjson) ist eine schnelle und präzise JSON-Bibliothek für Python.
Sie ist in Benchmarks die schnellste Python-JSON-Bibliothek und genauer als die Standardbibliothek `json` oder andere Bibliotheken von Drittanbietern. 
Zudem kann sie Dataclasses, Datetimes, numpy- und UUID-Instanzen nativ serialisieren.

Hier ist eine Beispiel-Renderer-Klasse mit `orjson`:


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



## Beispiel: XML-Renderer


So erstellen Sie einen Renderer, der alle Responses als XML ausgibt:

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
*(Quelle: dieser Code wurde im Wesentlichen von [DRF-xml](https://jpadilla.github.io/django-rest-framework-xml/) übernommen)*

!!! done

    Die Reihe zur Response-Verarbeitung ist abgeschlossen! Fahren Sie mit dem nächsten Abschnitt fort: **[APIs über Router aufteilen](../routers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
