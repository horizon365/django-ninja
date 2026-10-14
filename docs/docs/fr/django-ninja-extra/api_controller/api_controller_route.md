**Décorateurs de route du contrôleur d'API**
===================

  
La classe `route` est un décorateur de fonction utilisé pour annoter les fonctions de classe de contrôleur comme des endpoints avec une méthode HTTP spécifique.

Par exemple :

    from ninja_extra import route, api_controller
    
    @api_controller
    class MyController:
        @route.get('/test')
        def test(self):
            return {'message': 'test'}
    

  
`route` fournit des méthodes prédéfinies qui simplifient la création de diverses opérations, et leurs noms correspondent aux méthodes HTTP correspondantes :

*   GET : `route.get`
*   POST : `route.post`
*   PUT : `route.put`
*   DELETE : `route.delete`
*   PATCH : `route.patch`
*     
    Generic - utilisé pour les combinaisons d'opérations, par exemple, `route.generic(methods=['POST', 'PATCH'])`

**  
Paramètres d'initialisation**
------------

  
Voici une description d'ensemble des paramètres de la classe `route` dans NinjaExtra :

*     
    `path` : La chaîne de chemin d'endpoint unique requise.
    
*     
    `methods` : La collection de méthodes HTTP requises pour l'endpoint, par exemple, `['POST', 'PUT']`.
    
*     
    `auth` : Définit la méthode d'authentification pour l'endpoint. Défaut : `NOT_SET`
    
*     
    `response` : Définit le format de réponse comme `dict[status_code, schema]` ou `Schema`. Utilisé pour valider la réponse retournée. Défaut : `NOT_SET`
    
*     
    `operation_id` : Un identifiant unique optionnel utilisé pour distinguer les opérations dans les vues de chemins. Défaut : `NOT_SET`
    
*     
    `summary` : Un résumé optionnel utilisé pour décrire l'endpoint. Défaut : `None`
    
*     
    `description` : Une description optionnelle fournissant des détails supplémentaires sur l'endpoint. Défaut : `None`
    
*     
    `tags` : Une liste de chaînes utilisée pour regrouper les endpoints à des fins de documentation. Défaut : `None`
    
*     
    `deprecated` : Un paramètre booléen optionnel indiquant si l'endpoint est obsolète. Défaut : `None`
    
*     
    `by_alias` : Un paramètre optionnel utilisé pour filtrer l'objet schéma `response`. Défaut : `False`
    
*     
    `exclude_unset` : Un paramètre optionnel utilisé pour filtrer l'objet schéma `response`. Défaut : `False`
    
*     
    `exclude_defaults` : Un paramètre optionnel utilisé pour filtrer l'objet schéma `response`. Défaut : `False`
    
*     
    `exclude_none` : Un paramètre optionnel utilisé pour filtrer l'objet schéma `response`. Défaut : `False`
    
*     
    `include_in_schema` : Indique si l'endpoint doit apparaître dans la documentation Swagger. Défaut : `True`
    
*     
    `url_name` : Fournit un nom pour l'endpoint qui peut être résolu à l'aide de la fonction `reverse` dans Django. Défaut : `None`
    
*     
    `permissions` : Définit la collection de classes de permissions de route pour l'endpoint. Défaut : `None`
    

  
Ces paramètres fonctionnent de manière similaire à ceux utilisés lors de la création d'endpoints dans Django-Ninja, mais ont été abstraits pour fonctionner avec des classes de contrôleur dans NinjaExtra.

**Définition de routes asynchrones**
-----------

  
Dans Django-Ninja-Extra, la classe `route` prend en charge la définition d'endpoints asynchrones, de manière similaire à Django-Ninja. Cette fonctionnalité est disponible pour les versions de Django supérieures à 3.0.

Par exemple :

    import asyncio
    from ninja_extra import http_get, api_controller
    
    @api_controller
    class MyController:
        @http_get("/say-after")
        async def say_after(self, delay: int, word: str):
            await asyncio.sleep(delay)
            return {'saying': word}
    

  
Dans cette illustration, l'endpoint `say_after` est défini comme une fonction asynchrone à l'aide du mot-clé `async`, permettant des opérations asynchrones au sein de l'endpoint.

  
!!! info En savoir plus sur la prise en charge de l'async dans Django-Ninja

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
