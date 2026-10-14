---
comments: true
---
## Introduction
J'avais entendu parler de JWT il y a longtemps, mais je ne l'avais jamais réellement utilisé. Récemment, en étudiant le protocole d'upload reprenable tus, je suis arrivé au niveau des hooks-http, dans le but de m'authentifier pendant l'upload de fichiers. Naturellement, j'ai pensé au paquet `django-ninja-jwt`. Je pensais que ce serait simple, mais après avoir lu la [documentation chinoise](https://django-ninja.cn/django-ninja-jwt/), j'ai découvert que ce n'était pas seulement simple — c'était épuré à un degré étonnant.

## Premiers pas

Selon le guide, il suffit d'installer `dango-ninja-jwt` et `django-ninja-extra`, puis de remplacer `NinjaAPI` par `njaExtraAPI`, et il ne faut qu'une seule ligne.

```python
api.register_controllers(NinjaJWTDefaultController)
```

C'est honnêtement déroutant.

Attendez — regardons d'abord la documentation. Trois nouveaux endpoints apparaissent : `pair`, `refresh` et `verify`.
![JWT swagger UI token](../img/jwt-token.png)
Notez l'icône de cadenas en haut à droite — elle nous servira plus tard. Elle n'apparaît que lorsque vous utilisez la fonction `JWTAuth`.

### pair
Le premier est l'endpoint `pair`. Cela signifie qu'après avoir fourni un nom d'utilisateur et un mot de passe, il renvoie des jetons d'authentification et des jetons de rafraîchissement.
Le format du corps de la requête est le suivant :
```json
{
  "password": "string",
  "username": "string"
}
```
Remarque : Ici, `username` apparaît en dessous, ce qui est un peu différent de ce que vous pourriez supposer.
Après avoir cliqué sur Execute, vous obtiendrez quelque chose comme ceci :
```json
{
  "data": {
    "username": "lyq",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzE0NzU2NCwiaWF0IjoxNzQyNTQyNzY0LCJqdGkiOiI4MTZmMzg2YWYwNmY0NmVhOWY1YzlkMDJjYzQxZjFkOCIsInVzZXJfaWQiOjF9.G-mTefGtP-cTXWVrxAsqXGGKnZ1442jw67ilvTY5gcQ",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNjI5MTY0LCJpYXQiOjE3NDI1NDI3NjQsImp0aSI6IjdiMGY1Y2Y5NTVlZDRiMzQ5M2M3MmY4NzJmNDdkMzUxIiwidXNlcl9pZCI6MX0.JO9PxVA-rX6TPo9Db00eOuOorThjgX3nTjBT-CuOh90"
  }
}
```
### refresh
Le jeton `access` ci-dessus peut être utilisé pour l'authentification, mais sa durée de vie est limitée par défaut. Le jeton `refresh` a une durée de vie plus longue que `access` et sert à obtenir un nouveau jeton `access` après l'expiration du précédent.
Une fois rafraîchi, le jeton `access` précédent devient invalide.

À ce stade, vous pouvez copier `access` dans l'icône de cadenas en haut à droite. Ainsi, chaque endpoint de la page actuelle peut l'utiliser, ce qui est pratique pour le débogage.
### verify
Vous pouvez aller au troisième endpoint, `verify`, pour vérifier si le jeton `access` est valide.

Dans l'ensemble, `django-ninja-jwt` construit simplement trois endpoints pour vous, rendant pratique l'obtention, le rafraîchissement et le test des jetons.

## Personnalisation
Ces trois endpoints seuls ne suffisent pas — au minimum, nous devons ajouter l'authentification à nos propres endpoints spécifiques.
Ce dont vous avez besoin ici, c'est de `JWTAuth` ; c'est seulement après l'avoir utilisé que l'icône de cadenas apparaîtra.
```python
from ninja_jwt.authentication import JWTAuth
@route.get('/some', auth=JWTAuth())
def some_endpoint(request):
    """Convenient for showing the auth button on the docs page"""
    return request.auth.username
```
Et sur l'endpoint `some`, il y a aussi une icône de cadenas autonome.
![JWT swagger UI token custom](../img/jwt-token-custom.png)
Pour l'endpoint `some` ci-dessus, si l'authentification réussit, il répond avec le nom d'utilisateur de l'utilisateur actuellement connecté. En cas d'échec, il renvoie une réponse 401.
Les développeurs backend doivent demander à l'équipe frontend d'envoyer cette valeur — laissez-les aller à la section [pair](#pair) pour l'obtenir, et périodiquement à [refresh](#refresh) pour le rafraîchir.

### Configurer la durée de vie des jetons

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Access token lifetime
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh token lifetime
    'AUTH_HEADER_TYPES': ('Bearer',),
}

```
### Personnalisation poussée
Si l'utilisation de `@route.get('/some', auth=JWTAuth())` dans votre route ninja ne répond pas à vos besoins, vous pouvez appeler `authenticate` à l'intérieur de la fonction.

```python
@route.get('/some')
def some_endpoint(request):
    auth = JWTAuth()
    # If it fails, a 401 is raised internally
    if auth.authenticate(request, token):
        return request.auth.username

```
Le `token` ci-dessus doit être extrait de l'objet `request` par vous-même.
