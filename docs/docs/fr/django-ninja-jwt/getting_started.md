
#### Prérequis
- Python >= 3.6
- Django >= 2.1
- Django-Ninja >= 0.16.1
- Django-Ninja-Extra >= 0.11.0

Ce sont les versions de Python et des packages officiellement prises en charge. D'autres versions peuvent également fonctionner. Vous êtes libre de modifier la configuration tox pour voir ce qui est possible.

## Installation

Ninja JWT peut être installé via pip :

    pip install django-ninja-jwt

De plus, vous devez enregistrer le contrôleur `NinjaJWTDefaultController` auprès de votre API Django-Ninja.

```python
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

```
`NinjaJWTDefaultController` est livré avec trois routes : `obtain_token`, `refresh_token` et `verify_token`.
Il s'agit d'une combinaison de deux sous-classes, `TokenVerificationController` et `TokenObtainPairController`.
Si vous souhaitez personnaliser ces routes, vous pouvez hériter de ces contrôleurs et modifier leur implémentation.

```python
from ninja_extra import api_controller
from ninja_jwt.controller import TokenObtainPairController

@api_controller('token', tags=['Auth'])
class MyCustomController(TokenObtainPairController):
    """Only obtain token and refresh token"""
...
api.register_controllers(MyCustomController)
```

Si vous souhaitez utiliser la localisation/traduction, ajoutez simplement `ninja_jwt` à `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    ...
    'ninja_jwt',
    ...
]
```

## Utilisation

Pour vérifier que Ninja JWT fonctionne, vous pouvez effectuer quelques requêtes de test avec curl :

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "davidattenborough", "password": "boatymcboatface"}' \
  http://localhost:8000/api/token/pair

...
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}
```

Vous pouvez utiliser l'access token renvoyé pour prouver l'authentification auprès des vues protégées :

``` {.sourceCode .bash}
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
  http://localhost:8000/api/some-protected-view/
```

Lorsque cet access token de courte durée expire, vous pouvez utiliser le refresh token, qui a une durée de vie plus longue, pour obtenir un nouvel access token :

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"}' \
  http://localhost:8000/api/token/refresh/

...
{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXN...", "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVm..."}
```

Dépendances cryptographiques (Optionnel)
-------------------------------------

Si vous prévoyez d'encoder ou de décoder des tokens à l'aide de certains algorithmes de signature numérique (c'est-à-dire RSA et ECDSA ; voir PyJWT pour les autres algorithmes),
vous devrez installer la bibliothèque cryptography_. Elle peut être installée explicitement, ou en tant qu'élément requis des dépendances de `django-ninja-jwt` :

    pip install django-ninja-jwt[crypto]

Lors de l'utilisation du fichier de requirements du projet `Ninja JWT`, le format `django-ninja-jwt[crypto]` est recommandé,
car une ligne de requirement `cryptography` distincte pourrait ultérieurement être considérée à tort comme un requirement inutilisé et être supprimée.
[cryptography](https://cryptography.io)

!!! success

    Poursuivez avec le chapitre suivant **[Authentification des routes](auth_integration.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
