---
comments: true
---
# Renderers de réponse

Pour une API REST, le type de réponse le plus courant est généralement JSON.
**Django Ninja** prend également en charge la définition de vos propres renderers personnalisés, ce qui vous donne la flexibilité de concevoir vos propres types de médias.

## Création d'un Renderer

Pour créer votre propre renderer, vous devez hériter de `ninja.renderers.BaseRenderer` et redéfinir la méthode `render`. Vous pouvez ensuite passer une instance de votre classe comme argument `renderer` à `NinjaAPI` :

```python hl_lines="5 8 9"
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer


class MyRenderer(BaseRenderer):
    media_type = "text/plain"

    def render(self, request, data, *, response_status):
        return ... # your serialization here

api = NinjaAPI(renderer=MyRenderer())
```

La méthode `render` accepte les arguments suivants :

 - request -> l'objet HttpRequest
 - data -> l'objet qui doit être sérialisé
 - response_status -> un `int` représentant le code de statut HTTP qui sera renvoyé au client

Vous devez également définir l'attribut `media_type` sur la classe pour définir l'en-tête content-type de la réponse.


## Exemple de renderer ORJSON :

[orjson](https://github.com/ijl/orjson#orjson) est une bibliothèque JSON rapide et précise pour Python.
C'est la bibliothèque JSON Python la plus rapide dans les benchmarks, et plus précise que la bibliothèque `json` standard ou les autres bibliothèques tierces.
Elle peut également sérialiser nativement les dataclasses, les datetimes, numpy et les instances UUID.

Voici un exemple de classe renderer utilisant `orjson` :


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



## Exemple de renderer XML :


Voici comment créer un renderer qui affiche toutes les réponses en XML :

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
*(Crédit : ce code est pour l'essentiel copié de [DRF-xml](https://jpadilla.github.io/django-rest-framework-xml/))*

!!! done

    La série sur la gestion des réponses est terminée ! Poursuivez avec la section suivante **[Fractionnement des API via les Routers](../routers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
