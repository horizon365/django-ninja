---
comments: true
---
# Gestion des erreurs

**Django Ninja** vous permet d'installer des gestionnaires d'exceptions personnalisés pour contrôler la manière dont les réponses sont renvoyées en cas d'erreurs ou d'exceptions gérées.

## Gestionnaires d'exceptions personnalisés

Supposons que vous construisez une API qui dépend d'un service externe conçu pour être indisponible à certains moments. Vous pouvez gérer cette erreur et renvoyer une réponse conviviale au client (lui demandant de revenir plus tard) au lieu de lever l'erreur 500 par défaut lorsque l'exception se produit.
Pour ce faire, vous devez :

 - 1) Créer une exception (ou en utiliser une existante)
 - 2) Utiliser le décorateur api.exception_handler


Exemple :


```python hl_lines="9 10"
api = NinjaAPI()

class ServiceUnavailableError(Exception):
    pass


# initializing handler

@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=503,
    )


# some logic that throws exception

@api.get("/service")
def some_operation(request):
    if random.choice([True, False]):
        raise ServiceUnavailableError()
    return {"message": "Hello"}

```

La fonction gestionnaire d'exceptions prend 2 arguments :

 - **request** - la requête HTTP de Django
 - **exc** - l'exception réelle

La fonction doit renvoyer une réponse HTTP

## Redéfinir les gestionnaires d'exceptions par défaut

Par défaut, **Django Ninja** initialise les gestionnaires d'exceptions suivants :


#### `ninja.errors.AuthenticationError`

Levée lorsque les données d'authentification sont invalides

#### `ninja.errors.ValidationError`

Levée lorsque les données de la requête échouent à la validation

#### `ninja.errors.HttpError`

Utilisée pour lever une erreur HTTP avec un code de statut depuis n'importe quel endroit du code
#### `django.http.Http404`

L'exception 404 par défaut de Django (peut être renvoyée, par exemple, à l'aide de get_object_or_404)
#### `Exception`

Toute autre exception non gérée par l'application.
Comportement par défaut

  - **Si `settings.DEBUG` est `True`** - renvoie une traceback en texte brut (utile lors du débogage dans la console ou dans Swagger UI)
  - **sinon** - utilise le mécanisme de gestion des exceptions par défaut de Django (journalisation des erreurs, envoi d'e-mails aux ADMINS)


### Redéfinir les gestionnaires par défaut

Si vous devez modifier la sortie par défaut des erreurs de validation - redéfinissez le gestionnaire d'exceptions ValidationError :

```python hl_lines="1 4"
from ninja.errors import ValidationError
...

@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return HttpResponse("Invalid input", status=422)
```


## Lever des réponses HTTP via des exceptions

Comme alternative à la création d'une exception personnalisée et à l'écriture d'un gestionnaire pour celle-ci - vous pouvez également lever une exception HTTP, ce qui aura pour résultat qu'une réponse HTTP avec le code souhaité soit renvoyée

```python
from ninja.errors import HttpError

@api.get("/some/resource")
def some_operation(request):
    if True:
        raise HttpError(503, "Service Unavailable. Please retry later.")

```
!!! success

    Poursuivez avec la section suivante **[Inversion des URL](urls.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
