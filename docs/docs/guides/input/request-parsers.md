---
comments: true
---
# 请求解析器

在大多数情况下，REST API 的默认内容类型是 JSON，但如果你需要处理其他内容类型（如 YAML、XML、CSV）或使用更快的 JSON 解析器，**Django Ninja** 提供了一个 `解析器` 配置。

```python
api = NinjaAPI(parser=MyYamlParser())
```

要创建你自己的解析器，你需要扩展 `ninja.parser.Parser` 类，并覆盖 `parse_body` 方法。


## 示例 YAML 解析器

让我们创建我们自定义的 YAML 解析器：

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

如果你现在像这样发送 YAML 作为请求主体：

```YAML
ints:
 - 0
 - 1
string: hello
f: 3.14
```

它将被正确解析，并且你应该有像这样的 JSON 输出：


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


## 示例 ORJSON 解析器

[orjson](https://github.com/ijl/orjson#orjson) 是一个用于 Python 的快速、准确的 JSON 库。它在基准测试中是最快的 Python JSON 库，并且比标准的 `json` 库或其他第三方库更准确。

```
pip install orjson
```

解析器代码：

```python hl_lines="1 8 9"
import orjson
from ninja import NinjaAPI
from ninja.parser import Parser


class ORJSONParser(Parser):
    def parse_body(self, request):
        return orjson.loads(request.body)


api = NinjaAPI(parser=ORJSONParser())
```

!!! 大功告成

    继续下一章节！ **[过滤](filtering.md)**

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
