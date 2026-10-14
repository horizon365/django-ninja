---
comments: true
---
# Analyseurs de requête

Dans la plupart des cas, le type de contenu par défaut d'une API REST est JSON, mais si vous devez gérer d'autres types de contenu (tels que YAML, XML, CSV) ou utiliser un analyseur JSON plus rapide, **Django Ninja** fournit une configuration `parser`.

```python
api = NinjaAPI(parser=MyYamlParser())
```

Pour créer votre propre analyseur, vous devez étendre la classe `ninja.parser.Parser` et redéfinir la méthode `parse_body`.


## Exemple d'analyseur YAML

Créons notre analyseur YAML personnalisé :

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

Si vous envoyez maintenant du YAML comme corps de requête comme ceci :

```YAML
ints:
 - 0
 - 1
string: hello
f: 3.14
```

Il sera analysé correctement, et vous devriez obtenir une sortie JSON comme celle-ci :


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


## Exemple d'analyseur ORJSON

[orjson](https://github.com/ijl/orjson#orjson) est une bibliothèque JSON rapide et précise pour Python. C'est la bibliothèque JSON Python la plus rapide dans les benchmarks, et plus précise que la bibliothèque `json` standard ou les autres bibliothèques tierces.

```
pip install orjson
```

Le code de l'analyseur :

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

    Poursuivez avec le chapitre suivant ! **[Filtrage](filtering.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
