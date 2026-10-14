---
comments: true
---
# Response Renderers

Untuk REST API, jenis response yang paling umum biasanya adalah JSON.
**Django Ninja** juga mendukung pendefinisian renderer kustom Anda sendiri, yang memberi Anda fleksibilitas untuk merancang media types Anda sendiri.

## Membuat Renderer

Untuk membuat renderer Anda sendiri, Anda perlu mewarisi dari `ninja.renderers.BaseRenderer` dan meng-override method `render`. Kemudian Anda dapat meneruskan instance class Anda sebagai argumen `renderer` ke `NinjaAPI`:

```python hl_lines="5 8 9"
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer


class MyRenderer(BaseRenderer):
    media_type = "text/plain"

    def render(self, request, data, *, response_status):
        return ... # your serialization here

api = NinjaAPI(renderer=MyRenderer())
```

Method `render` menerima argumen-argumen berikut:

 - request -> objek HttpRequest 
 - data -> objek yang perlu diserialisasi
 - response_status -> sebuah `int` yang merepresentasikan HTTP status code yang akan dikembalikan ke client

Anda juga perlu mendefinisikan atribut `media_type` pada class untuk menyetel header content-type response.


## Contoh ORJSON Renderer:

[orjson](https://github.com/ijl/orjson#orjson) adalah library JSON yang cepat dan akurat untuk Python.
Library ini adalah library JSON Python tercepat dalam benchmark, dan lebih akurat daripada library `json` standar atau library pihak ketiga lainnya. 
Library ini juga dapat menampilkan serialisasi native untuk dataclasses, datetimes, numpy, dan instance UUID.

Berikut adalah contoh class renderer yang menggunakan `orjson`:


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



## Contoh XML Renderer:


Berikut adalah cara membuat renderer yang mengeluarkan semua response dalam bentuk XML:

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
*(Kredit: kode ini pada dasarnya disalin dari [DRF-xml](https://jpadilla.github.io/django-rest-framework-xml/))*

!!! done

    Seri penanganan response telah selesai! Lanjutkan ke bagian berikutnya **[Memecah API dengan Routers](../routers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
