---
comments: true
---
# リクエストパーサー

ほとんどの場合、REST API のデフォルトのコンテンツタイプは JSON ですが、他のコンテンツタイプ（YAML、XML、CSV など）を処理したり、より高速な JSON パーサーを使用したりする必要がある場合は、**Django Ninja** が `parser` 設定を提供しています。

```python
api = NinjaAPI(parser=MyYamlParser())
```

独自のパーサーを作成するには、`ninja.parser.Parser` クラスを継承し、`parse_body` メソッドをオーバーライドする必要があります。


## YAML パーサーの例

独自の YAML パーサーを作成してみましょう:

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

次のような YAML をリクエストボディとして送信すると:

```YAML
ints:
 - 0
 - 1
string: hello
f: 3.14
```

正しくパースされ、次のような JSON 出力が得られるはずです:


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


## ORJSON パーサーの例

[orjson](https://github.com/ijl/orjson#orjson) は、Python 向けの高速で正確な JSON ライブラリです。ベンチマークにおいて最速の Python JSON ライブラリであり、標準の `json` ライブラリや他のサードパーティライブラリよりも正確です。

```
pip install orjson
```

パーサーのコード:

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

    次の章に進みましょう！ **[フィルタリング](filtering.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
