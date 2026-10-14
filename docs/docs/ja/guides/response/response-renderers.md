---
comments: true
---
# レスポンスレンダラー

REST API では、最も一般的なレスポンスタイプは通常 JSON です。
**Django Ninja** は独自のカスタムレンダラーを定義することもサポートしており、これにより独自のメディアタイプを柔軟に設計できます。

## レンダラーの作成

独自のレンダラーを作成するには、`ninja.renderers.BaseRenderer` を継承し、`render` メソッドをオーバーライドする必要があります。その後、クラスのインスタンスを `renderer` 引数として `NinjaAPI` に渡せます:

```python hl_lines="5 8 9"
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer


class MyRenderer(BaseRenderer):
    media_type = "text/plain"

    def render(self, request, data, *, response_status):
        return ... # your serialization here

api = NinjaAPI(renderer=MyRenderer())
```

`render` メソッドは次の引数を受け取ります:

 - request -> HttpRequest オブジェクト
 - data -> シリアライズが必要なオブジェクト
 - response_status -> クライアントに返される HTTP ステータスコードを表す `int`

また、レスポンスの content-type ヘッダーを設定するために、クラスに `media_type` 属性を定義する必要があります。


## ORJSON レンダラーの例:

[orjson](https://github.com/ijl/orjson#orjson) は、Python 向けの高速で正確な JSON ライブラリです。
ベンチマークにおいて最速の Python JSON ライブラリであり、標準の `json` ライブラリや他のサードパーティライブラリよりも正確です。
また、dataclass、datetime、numpy、UUID のインスタンスをネイティブにシリアライズできます。

`orjson` を使用したレンダラークラスの例を示します:


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



## XML レンダラーの例:


すべてのレスポンスを XML として出力するレンダラーの作成方法を示します:

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
*（クレジット: このコードは基本的に [DRF-xml](https://jpadilla.github.io/django-rest-framework-xml/) からコピーしたものです）*

!!! done

    レスポンス処理のシリーズは完了です！ 次のセクション **[ルーターによる API の分割](../routers.md)** に進みましょう

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
