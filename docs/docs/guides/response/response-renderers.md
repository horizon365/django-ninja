# 响应渲染器

对于一个 REST API 来说，最常见的响应类型通常是 JSON。
**Django Ninja** 也支持定义你自己的自定义渲染器，这给了你设计自己的媒体类型的灵活性。

## 创建一个渲染器

要创建你自己的渲染器，你需要继承 `ninja.renderers.BaseRenderer` 并覆盖 `render` 方法。 然后你可以将你的类的一个实例作为 `renderer` 参数传递给 `NinjaAPI` :

```python hl_lines="5 8 9"
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer


class MyRenderer(BaseRenderer):
    media_type = "text/plain"

    def render(self, request, data, *, response_status):
        return ... # your serialization here

api = NinjaAPI(renderer=MyRenderer())
```

`render` 方法接受以下参数：

 - request -> HttpRequest 对象 
 - data ->  需要被序列化的对象
 -  作为 `int` 整数的 response_status -> 将返回给客户端的 HTTP 状态码

你还需要在类上定义 `media_type` 属性来设置响应的内容类型头部。


## ORJSON 渲染器示例:

[orjson](https://github.com/ijl/orjson#orjson) 是一个用于 Python 的快速、准确的 JSON 库。
它在基准测试中是最快的 Python JSON 库，并且比标准的 `json` 库或其他第三方库更准确。 
它还能原生地序列化数据类、日期时间、numpy 和 UUID 实例。

这是一个使用 `orjson` 的示例渲染器类:


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



## XML 渲染器示例:


这是你如何创建一个将所有响应输出为 XML 的渲染器：

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
*(版权说明：这段代码基本上是从 [DRF-xml](https://jpadilla.github.io/django-rest-framework-xml/))复制的*
