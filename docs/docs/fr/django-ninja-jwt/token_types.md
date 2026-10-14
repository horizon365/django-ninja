
Ninja JWT fournit deux types de jetons différents qui peuvent être utilisés pour prouver une authentification.
Dans la charge utile d'un jeton, son type peut être identifié par la valeur de sa claim de type de jeton, qui par défaut est `token_type`.
Cependant, cette claim peut avoir la valeur `access`, `sliding` ou `refresh`,
mais actuellement les jetons refresh ne sont pas considérés comme des jetons d'authentification valides. Le nom de la claim utilisée pour stocker le type peut être personnalisé en modifiant le paramètre `TOKEN_TYPE_CLAIM`.

Par défaut, Ninja JWT attend un jeton `access` pour prouver l'authentification.
Les types de jetons d'authentification autorisés sont déterminés par la valeur du paramètre `AUTH_TOKEN_CLASSES`.
Ce paramètre contient une liste de chemins pointés (dotted paths) pointant vers des classes de jetons. Par défaut, il contient le chemin pointé `'ninja_jwt.tokens.AccessToken'`,
mais il peut également inclure le chemin pointé `'ninja_jwt.tokens.SlidingToken'`.
L'un ou l'autre de ces chemins pointés, ou les deux, peuvent apparaître dans la liste des classes de jetons d'authentification.
Si les deux sont présents, alors les deux types de jetons peuvent être utilisés pour prouver l'authentification.

Sliding Tokens
==============

Les jetons sliding (glissants) offrent une expérience plus pratique pour les utilisateurs de jetons, mais au prix d'une sécurité moindre et, lorsque l'application blacklist est utilisée, de performances moindres.
Un jeton sliding est un jeton qui contient à la fois une claim d'expiration et une claim d'expiration de rafraîchissement. Tant que l'horodatage de la claim d'expiration du jeton sliding n'est pas passé,
il peut être utilisé pour prouver l'authentification. En outre, tant que l'horodatage de sa claim d'expiration de rafraîchissement n'est pas passé,
il peut également être soumis à la vue de rafraîchissement pour obtenir une copie de lui-même avec une claim d'expiration mise à jour.

Si vous souhaitez utiliser des jetons sliding, modifiez le paramètre `AUTH_TOKEN_CLASSES` en `('ninja_jwt.tokens.SlidingToken',)`.
(Alternativement, si vous souhaitez autoriser les deux types de jetons pour l'authentification, le paramètre `AUTH_TOKEN_CLASSES` peut inclure des chemins pointés vers les classes de jetons `AccessToken` et `SlidingToken`
dans le module `ninja_jwt.tokens`)

En outre, enregistrez `NinjaJWTSlidingController` auprès de l'`api` :
```python
from ninja_jwt.controller import NinjaJWTSlidingController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTSlidingController)

```

Notez que si vous utilisez l'application blacklist, Ninja JWT validera tous les jetons sliding par rapport à la blacklist à chaque requête authentifiée.
Cela dégradera les performances des vues d'API authentifiées.

!!! success

    Poursuivez avec le chapitre suivant **[Blacklist App](blacklist_app.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
