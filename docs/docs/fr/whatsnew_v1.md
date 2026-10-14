---
comments: true
---
# Bienvenue dans Django Ninja 1.0


Pour commencer, installez la dernière version à l'aide de la commande suivante :
```
pip install -U django-ninja
```

django-ninja v1 est compatible avec Python 3.7 et supérieur.


La série Django Ninja 0.x reste prise en charge, mais ne recevra plus que des mises à jour de sécurité et des corrections de bugs critiques.


✨ Quoi de neuf dans Django Ninja 1.0

## Prise en charge de Pydantic2

Pydantic version 2 est réécrit en Rust et apporte de nombreuses améliorations et fonctionnalités, telles que :

 - Des types plus sûrs.
 - Une meilleure extensibilité.
 - De meilleures performances.

D'après nos tests, un projet moyen peut gagner environ 10 % de performances en moyenne, tandis que dans certains scénarios limites de parsing/sérialisation, vous pouvez obtenir un gain d'un facteur 4.
En revanche, cela introduit des changements incompatibles — pydantic 1 et 2 ne sont pas totalement compatibles — mais nous avons essayé de rendre cette transition aussi simple que possible.
Ainsi, si vous utilisiez la classe 'Schema', la migration vers ninja v1 devrait être directe. Sinon, veuillez suivre le [guide de migration pydantic](https://pydantic.com.cn/migration/)


Quelques nouvelles fonctionnalités fournies par pydantic2

### Contexte pydantic

Pydantic prend désormais en charge un contexte pendant la validation et la sérialisation, et Django Ninja transmet l'objet "request" lors du traitement des requêtes et des réponses.
```Python hl_lines="6 7"
class Payload(Schema):
    id: int
    name: str
    request_path: str

    @staticmethod
    def resolve_request_path(data, context):
        request = context["request"]
        return request.get_full_path()

```

Pendant la phase de réponse, "response_code" est également transmis au contexte.

## Schema.Meta

Pydantic a désormais déprécié la classe BaseModel.Config. Cependant, pour rester cohérent avec toutes les autres parties de Django, nous avons introduit une classe "Meta" pour ModelSchema — elle fonctionne de manière similaire aux ModelForms de Django :
```Python hl_lines="2 4"
class TxItem(ModelSchema):
    class Meta:
        model = Transaction
        fields = ["id", "account", "amount", "timestamp"]

```

(La classe "Config" reste prise en charge, mais est désormais dépréciée)


## Syntaxe de paramètres plus courte/plus propre

```python
@api.post('/some')
def some_form(request, username: Form[str], password: Form[str]):
    return True
```

au lieu de

```python
@api.post('/some')
def some_form(request, username: str = Form(...), password: str = Form(...)):
    return True
```

ou

```python
@api.post('/some')
def some_form(request, data: Form[AuthSchema]):
    return True
```


au lieu de

```python
@api.post('/some')
def some_form(request, data: AuthSchema = Form(...)):
    return True
```



ainsi que toutes les fonctionnalités d'autocomplétion dans votre éditeur.


En revanche, **l'ancienne syntaxe reste prise en charge**, vous pouvez donc porter votre projet vers la dernière version de django-ninja sans effort.


#### + Annotated

typing.Annotated est également désormais pris en charge :

```Python
@api.get("/annotated")
def annotated(request, data: Annotated[SomeData, Form()]):
    return {"data": data.dict()}

```


## Prise en charge de l'authentification asynchrone

Les authentificateurs asynchrones sont enfin pris en charge. Il vous suffit d'ajouter `async` à votre méthode `authenticate` :

```Python
class Auth(HttpBearer):
    async def authenticate(self, request, token):
        await asyncio.sleep(1)
        if token == "secret":
            return token

```


## Comportement CSRF modifié


`csrf=True` n'est plus requis si vous utilisez une authentification basée sur les cookies. À la place, la protection CSRF est activée automatiquement. Cela vous permet également de mélanger des authentificateurs protégés par CSRF avec d'autres méthodes qui n'exigent pas de cookies :

```Python
api = NinjaAPI(auth=[django_auth, Auth()])
```


## Documentation

Le visualiseur de documentation est désormais configurable et pluggable. Par défaut, django-ninja est livré avec Swagger et Redoc :
```Python
from ninja import NinjaAPI, Redoc, Swagger


# use redoc
api = NinjaAPI(docs=Redoc()))

# use swagger:
api = NinjaAPI(docs=Swagger())

# set configuration for swagger:
api = NinjaAPI(docs=Swagger({"persistAuthorization": True}))
```

Les utilisateurs peuvent désormais créer des visualiseurs de documentation personnalisés en dérivant de la classe `DocsBase`.

## Router

add_router prend en charge les chemins sous forme de chaînes de caractères :

```Python
api = NinjaAPI()


api.add_router('/app1', 'myproject.app1.router')
api.add_router('/app2', 'myproject.app2.router')
api.add_router('/app3', 'myproject.app3.router')
api.add_router('/app4', 'myproject.app4.router')
api.add_router('/app5', 'myproject.app5.router')
```


## Décorateurs

Lorsque django-ninja décore une vue avec .get/.post etc., il encapsule le résultat de la fonction (dans la plupart des cas non pas une HttpResponse - mais un objet sérialisable), il est donc peu probable que cela fonctionne avec certains décorateurs intégrés ou tiers, tels que :
```python hl_lines="4"
from django.views.decorators.cache import cache_page

@api.get("/test")
@cache_page(5) # <----- will not work!
def test_view(request):
    return {"some": "Complex data"}
```
Cet exemple ne fonctionnera pas.

Désormais, django-ninja introduit un décorateur decorate_view qui permet d'injecter des décorateurs fonctionnant avec des réponses http :
```python hl_lines="1 4"
from ninja.decorators import decorate_view

@api.get("/test")
@decorate_view(cache_page(5))
def test_view(request):
    return str(datetime.now())
```


## Pagination

La méthode `paginate_queryset` accepte désormais l'objet `request`


#### Éléments incompatibles avec les versions antérieures
 - resolve_xxx(self, ...) - la prise en charge de la résolution (self) est dépréciée au profit de la fonctionnalité intégrée de pydantic.
 - pydantic v1 n'est plus pris en charge
 - python 3.6 n'est plus pris en charge

Au passage - si vous aimez ce projet et que vous ne lui avez pas encore donné d'étoile GitHub - faites-le ! [github star](img/github-star.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
