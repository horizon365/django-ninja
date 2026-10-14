---
comments: true
---
# Рендереры ответов

Для REST API наиболее распространённым типом ответа обычно является JSON.
**Django Ninja** также поддерживает определение собственных пользовательских рендереров, что даёт вам гибкость для создания собственных медиа-типов.

## Создание рендерера

Чтобы создать свой собственный рендерер, нужно унаследоваться от `ninja.renderers.BaseRenderer` и переопределить метод `render`. Затем вы можете передать экземпляр вашего класса в качестве аргумента `renderer` в `NinjaAPI`:

```python hl_lines="5 8 9"
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer


class MyRenderer(BaseRenderer):
    media_type = "text/plain"

    def render(self, request, data, *, response_status):
        return ... # your serialization here

api = NinjaAPI(renderer=MyRenderer())
```

Метод `render` принимает следующие аргументы:

 - request -> объект HttpRequest 
 - data -> объект, который нужно сериализовать
 - response_status -> `int`, представляющий код HTTP-статуса, который будет возвращён клиенту

Вам также нужно определить атрибут `media_type` в классе, чтобы задать заголовок content-type ответа.


## Пример рендерера ORJSON:

[orjson](https://github.com/ijl/orjson#orjson) — это быстрая и точная JSON-библиотека для Python.
Она является самой быстрой JSON-библиотекой Python в бенчмарках и точнее, чем стандартная библиотека `json` или другие сторонние библиотеки. 
Она также может нативно сериализовать dataclass'ы, datetime, numpy и экземпляры UUID.

Вот пример класса рендерера, использующего `orjson`:


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



## Пример рендерера XML:


Вот как можно создать рендерер, который выводит все ответы в виде XML:

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
*(Благодарность: этот код в основном скопирован из [DRF-xml](https://jpadilla.github.io/django-rest-framework-xml/))*

!!! done

    Серия про обработку ответов завершена! Переходите к следующему разделу **[Разделение API с помощью роутеров](../routers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
