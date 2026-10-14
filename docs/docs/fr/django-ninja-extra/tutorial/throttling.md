---
comments: true
---
# **Throttling / Contrôle de débit**

Le throttling peut être considéré comme une permission qui détermine si une requête doit être autorisée.
Il représente un état temporaire utilisé pour contrôler le débit auquel les clients peuvent effectuer des requêtes vers l'API.

```python
from ninja_extra import NinjaExtraAPI, throttle
api = NinjaExtraAPI()

@api.get('/users')
@throttle  # This will apply the default throttle classes [UserRateThrottle, AnonRateThrottle]
def my_throttled_endpoint(request):
    return 'foo'
```

!!! note
    L'exemple ci-dessus ne sera pas soumis au throttling, car la portée par défaut de `UserRateThrottle` et `AnonRateThrottle` est `none`

## **Throttling multiple**
Le throttling de Django-ninja-extra prend en charge plusieurs throttles, ce qui est utile pour appliquer différentes contraintes sur une API,
comme des taux de throttling en rafale ou des taux de throttling soutenus.
Par exemple, vous pourriez vouloir limiter les utilisateurs à un maximum de 60 requêtes par minute et 1000 requêtes par jour.

```python
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import UserRateThrottle
api = NinjaExtraAPI()

class User60MinRateThrottle(UserRateThrottle):
    rate = "60/min"
    scope = "minutes"


class User1000PerDayRateThrottle(UserRateThrottle):
    rate = "1000/day"
    scope = "days"

@api.get('/users')
@throttle(User60MinRateThrottle, User1000PerDayRateThrottle)
def my_throttled_endpoint(request):
    return 'foo'

```
## **Paramètres de la politique de throttling**
Vous pouvez définir globalement les classes et les taux de throttling par défaut dans le fichier `settings.py` de votre projet en redéfinissant les clés suivantes :
```python
# django settings.py
NINJA_EXTRA = {
    'THROTTLE_CLASSES': [
        "ninja_extra.throttling.AnonRateThrottle",
        "ninja_extra.throttling.UserRateThrottle",
    ],
    'THROTTLE_RATES': {
        'user': '1000/day',
        'anon': '100/day',
    },
    'NUM_PROXIES': None
}
```
Les descriptions de taux utilisées dans `THROTTLE_RATES` peuvent inclure `second`, `minute`, `hour` ou `day` comme période de throttling.

```python
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import UserRateThrottle

api = NinjaExtraAPI()

@api.get('/users')
@throttle(UserRateThrottle)
def my_throttled_endpoint(request):
    return 'foo'
```

## **Identification du client**
Les clients sont identifiés via l'en-tête HTTP X-Forwarded-For et la variable WSGI REMOTE_ADDR.
Ce sont les identifiants uniques utilisés pour déterminer l'adresse IP du client à des fins de throttling.
`X-Forwarded-For` a la priorité sur `REMOTE_ADDR` et est utilisé en tant que tel.

#### **Restriction des proxys clients**
Si vous devez identifier strictement les adresses IP uniques des clients, vous devez d'abord configurer le nombre de proxys applicatifs s'exécutant derrière l'API en définissant le paramètre `NUM_PROXIES`. Ce paramètre doit être un entier supérieur ou égal à zéro.
S'il est défini sur une valeur non nulle, alors une fois que les adresses IP des proxys applicatifs sont exclues en premier, l'IP du client sera identifiée comme la dernière adresse IP de l'en-tête X-Forwarded-For. S'il est défini sur zéro, la valeur de REMOTE_ADDR sera toujours utilisée comme adresse IP d'identification.
Il est important de comprendre que si vous configurez `NUM_PROXIES`, alors tous les clients situés derrière une même passerelle unique de [Network Address Translation (NAT)](https://en.wikipedia.org/wiki/Network_address_translation) seront traités comme un seul client.

!!! note
    Plus de contexte sur le fonctionnement de l'en-tête X-Forwarded-For et sur l'identification des adresses IP des clients distants est disponible ici.

## **Paramètres du cache du modèle de throttling**
Le modèle de throttling utilisé dans django-ninja-extra s'appuie sur le backend de cache de Django. Il utilise la valeur `default` de [`LocMemCache`]().
Pour plus de détails, veuillez consulter la [documentation sur le cache de Django](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache).

Si vous ne souhaitez pas utiliser le cache par défaut défini dans le modèle de throttling, voici un exemple montrant comment définir un cache différent pour le modèle de throttling :
```python

from django.core.cache import caches
from ninja_extra.throttling import AnonRateThrottle


class CustomAnonRateThrottle(AnonRateThrottle):
    cache = caches['alternate']
```
## **Référence de l'API**

## **Throttling de débit anonyme**
Le modèle `AnonRateThrottle` est utilisé pour la limitation de débit en utilisant l'adresse IP des utilisateurs non authentifiés comme clé.

Il convient pour limiter le débit des requêtes provenant de sources inconnues.

Les permissions de requête sont déterminées par :
- Le `rate` défini dans la classe dérivée
- La portée `anon` définie dans `THROTTLE_RATES` dans les paramètres `NINJA_EXTRA` de `settings.py`.

## **Throttling de débit utilisateur**
Le modèle `UserRateThrottle` est utilisé pour la limitation de débit en générant une clé à partir de l'ID utilisateur ou de la clé primaire des utilisateurs authentifiés.
Les requêtes non authentifiées reviendront à utiliser l'adresse IP de la requête entrante pour générer une clé unique à des fins de limitation de débit.

Les permissions de requête sont déterminées par :
- Le `rate` défini dans la classe dérivée
- La portée `user` définie dans `THROTTLE_RATES` dans les paramètres `NINJA_EXTRA` de `settings.py`.


Vous pouvez utiliser plusieurs taux de throttling utilisateur pour le modèle `UserRateThrottle`, par exemple :
```python
# example/throttles.py
from ninja_extra.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
```

```python
# django settings.py
NINJA_EXTRA = {
    'THROTTLE_CLASSES': [
        'example.throttles.BurstRateThrottle',
        'example.throttles.SustainedRateThrottle'
    ],
    'THROTTLE_RATES': {
        'burst': '60/min',
        'sustained': '1000/day'
    }
}
```
## **Throttling de débit dynamique**
Le modèle `DynamicRateThrottle` est utilisé pour soumettre au throttling les utilisateurs authentifiés et non authentifiés de manière similaire à `UserRateThrottle`.
Sa fonctionnalité clé est la possibilité de définir dynamiquement la `scope` lors de son utilisation.
Par exemple :
Nous pouvons définir une portée dans les settings.

```python
# django settings.py
NINJA_EXTRA = {
    'THROTTLE_RATES': {
        'burst': '60/min',
        'sustained': '1000/day'
    }
}
```

```python
# api.py
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import DynamicRateThrottle
api = NinjaExtraAPI()

@api.get('/users')
@throttle(DynamicRateThrottle, scope='burst')
def get_users(request):
    return 'foo'

@api.get('/users/<int:id>')
@throttle(DynamicRateThrottle, scope='sustained')
def get_user_by_id(request, id: int):
    return 'foo'
```
Ici, nous appliquons dynamiquement le taux `sustained` et le taux `burst` à `get_users` et `get_user_by_id` respectivement.


!!! note "New in v0.15.8"
    Vous pouvez soumettre au throttling toutes les opérations d'endpoint du contrôleur au niveau de la classe du contrôleur.

## **Throttling au niveau du contrôleur**

```python
# api.py
from ninja_extra import (
    NinjaExtraAPI, throttle, api_controller, ControllerBase,
    http_get
)
from ninja_extra.throttling import DynamicRateThrottle
api = NinjaExtraAPI()

@api_controller("/throttled-controller")
class ThrottlingControllerSample(ControllerBase):
    throttling_classes = [
        DynamicRateThrottle,
    ]
    throttling_init_kwargs = dict(scope="sustained")

    @http_get("/endpoint_1")
    @throttle(DynamicRateThrottle, scope='burst')
    def endpoint_1(self, request):
        # this will override the generally throttling applied at the controller
        return "foo"

    @http_get("/endpoint_2")
    def endpoint_2(self, request):
        return "foo"

    @http_get("/endpoint_3")
    def endpoint_3(self, request):
        return "foo"


api.register_controllers(ThrottlingControllerSample)
```
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
