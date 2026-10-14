**Contrôleur**
==============

  
Le contrôleur d'API de Ninja-Extra est responsable du traitement des requêtes entrantes et du renvoi des réponses au client.

  
Dans Ninja-Extra, il existe plusieurs composants principaux pour créer un modèle de contrôleur :

*   ControllerBase
*   Décorateur APIController

ControllerBase
--------------

  
La classe `ControllerBase` est la classe de base de tous les contrôleurs dans Django Ninja Extra. Elle fournit la fonctionnalité essentielle pour traiter les requêtes, valider les entrées et renvoyer les réponses de manière basée sur les classes.

  
Cette classe inclut des attributs et des méthodes communs à tous les contrôleurs, tels que l'objet `request`, `permission_classes` et l'objet `response`, qui font partie du `RouteContext`. L'objet request contient des informations sur la requête entrante, telles que les en-têtes, les paramètres de requête et les données du corps. L'attribut permission_classes est utilisé pour définir les permissions requises pour accéder aux routes du contrôleur, tandis que l'objet response est utilisé pour construire la réponse finale renvoyée au client.

  
En plus des attributs essentiels, la classe `ControllerBase` contient également des méthodes utilitaires qui peuvent être utilisées pour gérer des tâches courantes telles que les vérifications de permissions d'objet (`check_object_permission`), la création de réponses rapides (`create_response`) et la récupération de données depuis la base de données (`get_object_or_exception`). Ces méthodes peuvent être surchargées dans les sous-classes pour fournir un comportement personnalisé.

  
La classe de base du contrôleur inclut également un système d'injection de dépendances qui permet un accès facile aux autres services et objets de l'application, tels que les services de dépôt.

    from ninja_extra import ControllerBase, api_controller
    
    @api_controller('/users')
    class UserControllerBase(ControllerBase):
        ...
    

Décorateur APIController
------------------

  
Le décorateur `api_controller` est utilisé pour définir des contrôleurs basés sur des classes dans Django Ninja Extra. Il est appliqué aux classes ControllerBase et accepte plusieurs paramètres pour configurer le routage et les fonctionnalités du contrôleur.

  
Le premier paramètre, `prefix_or_class`, est soit une chaîne de préfixe pour toutes les routes enregistrées sous le contrôleur groupé, soit l'objet de classe auquel le décorateur est appliqué.

  
Le second paramètre, `auth`, est une liste de toutes les classes Auth de Django Ninja qui doivent être appliquées aux routes du contrôleur.

  
Le troisième paramètre, `tags`, est une liste de chaînes utilisée à des fins de balisage OPENAPI.

  
Le quatrième paramètre, `permissions`, est une liste de toutes les permissions qui doivent être appliquées aux routes du contrôleur.

  
Le cinquième paramètre, `auto_import`, vaut true par défaut et ajoute automatiquement votre contrôleur à la liste d'import automatique.

par exemple :

    import typing
    from ninja_extra import api_controller, ControllerBase, permissions, route
    from django.contrib.auth.models import User
    from ninja.security import APIKeyQuery
    from ninja import ModelSchema
    
    
    class UserSchema(ModelSchema):
        class Config:
            model = User
            model_fields = ['username', 'email', 'first_name']
    
    
    @api_controller('users/', auth=[APIKeyQuery()], permissions=[permissions.IsAuthenticated])
    class UsersController(ControllerBase):
        @route.get('', response={200: typing.List[UserSchema]})
        def get_users(self):
            # Logic to handle GET request to the /users endpoint
            users = User.objects.all()
            return users
    
        @route.post('create/', response={200: UserSchema})
        def create_user(self, payload: UserSchema):
            # Logic to handle POST request to the /users endpoint
            new_user = User.objects.create(
                username=payload.username,
                email=payload.email,
                first_name=payload.first_name,
            )
            new_user.set_password('password')
            return new_user
    

  
Dans le code ci-dessus, nous avons défini un contrôleur nommé `UsersController` à l'aide du décorateur `api_controller`. Le décorateur est appliqué à la classe et accepte deux arguments, l'endpoint URL `/users` et les classes `auth` et `permission`. `get_users` et `create_user` sont des fonctions de route qui traitent les requêtes GET `/users` et POST `/users/create` entrantes.

  
!!!info Hériter de la classe ControllerBase vous offre davantage de support IntelliSense de l'IDE.

Exemple rapide
-------------

  
Créons un APIController pour gérer correctement le modèle utilisateur de Django

    import uuid
    from ninja import ModelSchema
    from ninja_extra import (
        http_get, http_post, http_generic, http_delete,
        api_controller, status, ControllerBase, pagination
    )
    from ninja_extra.controllers.response import Detail
    from django.contrib.auth import get_user_model
    
    
    class UserSchema(ModelSchema):
        class Config:
            model = get_user_model()
            model_fields = ['username', 'email', 'first_name']
    
    
    @api_controller('/users')
    class UsersController(ControllerBase):
        user_model = get_user_model()
    
        @http_post()
        def create_user(self, user: UserSchema):
            # just simulating created user
            return dict(id=uuid.uuid4())
    
        @http_generic('/{int:user_id}', methods=['put', 'patch'], response=UserSchema)
        def update_user(self, user_id: int):
            """ Django Ninja will serialize Django ORM model to schema provided as `response`"""
            user = self.get_object_or_exception(self.user_model, id=user_id)
            return user
    
        @http_delete('/{int:user_id}', response=Detail(status_code=status.HTTP_204_NO_CONTENT))
        def delete_user(self, user_id: int):
            user = self.get_object_or_exception(self.user_model, id=user_id)
            user.delete()
            return self.create_response('', status_code=status.HTTP_204_NO_CONTENT)
    
        @http_get("", response=pagination.PaginatedResponseSchema[UserSchema])
        @pagination.paginate(pagination.PageNumberPaginationExtra, page_size=50)
        def list_user(self):
            return self.user_model.objects.all()
    
        @http_get('/{user_id}', response=UserSchema)
        def get_user_by_id(self, user_id: int):
            user = self.get_object_or_exception(self.user_model, id=user_id)
            return user
    

  
Dans l'exemple ci-dessus, la classe `UsersController` définit plusieurs méthodes correspondant à différentes méthodes HTTP, telles que `create_user`, `update_user`, `delete_user`, `list_user` et `get_user_by_id`. Ces méthodes sont décorées respectivement avec les décorateurs `http_post`, `http_generic`, `http_delete` et `http_get`.

  
La méthode `create_user` utilise le décorateur `http_post` et accepte un paramètre user de type `UserSchema`, qui est un `ModelSchema` utilisé pour valider et sérialiser les données d'entrée. Cette méthode est utilisée pour créer un nouvel utilisateur dans le système et renvoie l'`ID` de l'utilisateur.

  
La méthode `update_user` utilise le décorateur `http_generic` et accepte un paramètre `user_id` de type int. Le décorateur est configuré pour traiter les méthodes `PUT` et `PATCH` et fournit un paramètre response de type `UserSchema` utilisé pour sérialiser l'objet utilisateur.

  
La méthode `delete_user` utilise le décorateur `http_delete` et accepte un paramètre `user_id` de type int et un paramètre response de type Detail, qui renverra un code d'état 204 avec un corps vide en cas de succès.

  
La méthode `list_user` utilise le décorateur `http_get` et est décorée avec le décorateur `pagination.paginate`, qui utilise la classe `PageNumberPaginationExtra` pour paginer les résultats de la méthode avec 50 résultats par page. Elle fournit également un paramètre response de type `pagination.PaginatedResponseSchema[UserSchema]`, qui sera utilisé pour sérialiser et paginer la liste des utilisateurs renvoyée par la méthode.

  
La méthode `get_user_by_id` utilise le décorateur `http_get` et accepte un paramètre `user_id` de type int et un paramètre response de type UserSchema, qui sera utilisé pour sérialiser l'objet utilisateur.

  
Le contrôleur utilisateur utilise également `self.get_object_or_exception(self.user_model, id=user_id)`, une méthode utilitaire qui lève une exception si l'objet utilisateur ne peut pas être trouvé.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
