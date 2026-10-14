---
comments: true
---
# Authentification

## Introduction

**Django Ninja** fournit plusieurs outils pour vous aider à gérer l'authentification et l'autorisation facilement, rapidement et de manière standard, sans avoir à étudier et apprendre <a href="https://swagger.io/docs/specification/authentication/" target="_blank">toutes les spécifications de sécurité</a>.

L'idée centrale est que, lorsque vous décrivez une opération d'API, vous pouvez définir un objet d'authentification.
```python hl_lines="2 7"
{!./src/tutorial/authentication/code001.py!}
```

Dans cet exemple, le client ne pourra appeler la méthode `pets` que s'il utilise l'authentification par session Django (basée sur les cookies par défaut), sinon une erreur HTTP-401 sera renvoyée.
Si vous souhaitez uniquement autoriser les superusers, vous pouvez utiliser `from ninja.security import django_auth_superuser` à la place.
## Schéma OpenAPI automatique

Voici un exemple où le client doit transmettre un en-tête pour s'authentifier :

`Authorization: Bearer supersecret`

```python hl_lines="4 5 6 7 10"
{!./src/tutorial/authentication/bearer01.py!}
```

Allez maintenant sur la documentation <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a>.


![Swagger UI Auth](../img/auth-swagger-ui.png)

Maintenant, lorsque vous cliquez sur le bouton **Authorize**, il vous sera demandé de saisir votre jeton d'authentification.

![Swagger UI Auth](../img/auth-swagger-ui-prompt.png)

Lorsque vous effectuez un appel de test, chaque requête transmettra l'en-tête d'autorisation.

## Authentification globale

Si vous devez protéger **toutes** les méthodes de votre API, vous pouvez passer l'argument `auth` au constructeur `NinjaAPI` :


```python hl_lines="11 19"
from ninja import NinjaAPI, Form
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaAPI(auth=GlobalAuth())

# @api.get(...)
# def ...

# @api.post(...)
# def ...
```

Et, si vous devez remplacer certaines des méthodes, vous pouvez le faire à nouveau au niveau de l'opération en passant l'argument `auth`. Dans cet exemple, l'authentification sera désactivée pour l'opération `/token` :
```python hl_lines="19"
{!./src/tutorial/authentication/global01.py!}
```

## Options d'authentification disponibles

### Fonction personnalisée


L'argument « `auth=` » accepte n'importe quel appelable (callable). **NinjaAPI** n'appliquera l'authentification que si l'appelable renvoie une valeur **truthy** (convertible en booléen `True`). Cette valeur de retour sera assignée à l'attribut `request.auth`.

```python hl_lines="1 2 3 6"
{!./src/tutorial/authentication/code002.py!}
```


### Clés API

Certaines API utilisent des clés API pour l'autorisation. Une clé API est un jeton qu'un client fournit lors d'un appel d'API pour s'identifier. La clé peut être envoyée dans la chaîne de requête :
```
GET /something?api_key=abcdef12345
```

Ou dans un en-tête de requête :

```
GET /something HTTP/1.1
X-API-Key: abcdef12345
```

Ou dans un cookie :

```
GET /something HTTP/1.1
Cookie: X-API-KEY=abcdef12345
```

**Django Ninja** est livré avec des classes intégrées pour vous aider à gérer ces situations.


#### Dans la requête (Query)

```python hl_lines="1 2 5 6 7 8 9 10 11 12"
{!./src/tutorial/authentication/apikey01.py!}
```

Dans cet exemple, nous récupérons un jeton depuis `GET['api_key']` et trouvons le `Client` correspondant dans la base de données. L'instance Client sera définie comme attribut `request.auth`.

Remarque : **`param_name`** est le nom du paramètre GET qui sera vérifié. S'il n'est pas défini, la valeur par défaut `"key"` est utilisée.


#### Dans l'en-tête (Header)

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey02.py!}
```

#### Dans le cookie (Cookie)

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey03.py!}
```



### HTTP Bearer

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/bearer01.py!}
```

### Authentification HTTP Basic

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/basic01.py!}
```


## Multiples authentificateurs

L'argument **`auth`** vous permet également de passer plusieurs authentificateurs :

```python hl_lines="18"
{!./src/tutorial/authentication/multiple01.py!}
```

Dans ce cas, **Django Ninja** vérifiera d'abord la clé API depuis `GET`, et si elle n'est pas définie ou invalide, il vérifiera la clé `header`.
Si les deux sont invalides, une erreur d'authentification sera levée dans la réponse.


## Authentification au niveau du routeur

Utilisez l'argument `auth` sur un routeur pour appliquer un authentificateur à toutes les opérations déclarées dans celui-ci :

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

Ou en utilisant le constructeur du routeur
```python
router = Router(auth=BasicAuth())
```


## Exceptions personnalisées

Lever une exception qui possède un gestionnaire d'exceptions renverra la réponse de ce gestionnaire de la même manière que pour une opération :

```python hl_lines="1 4"
{!./src/tutorial/authentication/bearer02.py!}
```


## Authentification asynchrone

**Django Ninja** prend en charge de manière basique l'authentification asynchrone. Bien que les classes d'authentification par défaut ne soient pas compatibles async, vous pouvez toujours définir votre appelable d'authentification asynchrone personnalisé et le passer avec `auth`.

```python
async def async_auth(request):
    ...


@api.get("/pets", auth=async_auth)
def pets(request):
    ...
```


Pour plus d'informations, consultez [la gestion des erreurs](errors.md) .

!!! success

    Poursuivez avec la section suivante **[Test](testing.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
