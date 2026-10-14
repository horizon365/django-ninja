**Permissions du contrôleur d'API**
================

  
Le concept du système de permissions est dérivé de Django DRF.

  
Les vérifications de permissions s'exécutent toujours au début de la fonction de route, avant que tout autre code ne soit autorisé à continuer. Les vérifications de permissions utiliseront généralement les informations d'authentification dans les attributs `request.user` et `request.auth` pour déterminer si la requête entrante doit être autorisée.

  
Les permissions sont utilisées pour accorder ou refuser l'accès à différentes parties de l'API pour différentes classes d'utilisateurs.

  
Le style de permission le plus simple consiste à autoriser l'accès à tout utilisateur authentifié et à refuser l'accès à tout utilisateur non authentifié. Cela correspond à la classe `IsAuthenticated` dans Django Ninja Extra.

  
Un style de permission légèrement moins strict consiste à accorder aux utilisateurs authentifiés un accès complet et à autoriser aux utilisateurs non authentifiés un accès en lecture seule. Cela correspond à la classe `IsAuthenticatedOrReadOnly` dans Django Ninja Extra.

### **Limitations des permissions au niveau objet**

  
Lors du traitement d'une requête, la méthode `has_permission` est automatiquement appelée pour toutes les permissions spécifiées dans la liste de permissions de la fonction de route. Cependant, comme `has_object_permission` nécessite un objet pour la validation des permissions, elle n'est pas déclenchée. Par conséquent, lors de l'utilisation des méthodes `get_object_or_exception` ou `get_object_or_none` dans un contrôleur pour récupérer un objet, la méthode de permission `has_object_permission` sera appelée.

**Permissions personnalisées**
----------

  
Pour implémenter une permission personnalisée, héritez de `BasePermission` et implémentez une ou les deux méthodes suivantes :

    .has_permission(self, request: HttpRequest, controller: "APIController")
    .has_object_permission(self, request: HttpRequest, controller: "APIController", obj: Any)
    

Exemple

    from ninja_extra import permissions, api_controller, http_get
    
    class ReadOnly(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.method in permissions.SAFE_METHODS
    
    @api_controller(permissions=[permissions.IsAuthenticated | ReadOnly])
    class PermissionController:
        @http_get('/must_be_authenticated', permissions=[permissions.IsAuthenticated])
        def must_be_authenticated(self, word: str):
            return dict(says=word)
    

**  
Opérateurs de permissions pris en charge**
---------------

*   & (et) ex : `permissions.IsAuthenticated & ReadOnly`
*   | (ou) ex : `permissions.IsAuthenticated | ReadOnly`
*   ~ (non) ex : `~(permissions.IsAuthenticated & ReadOnly)`

**  
Utilisation d'objets de permission dans les contrôleurs**
------------------

  
Le système de permissions de Ninja-Extra offre de la flexibilité lors de la définition des permissions, permettant de les définir soit comme des instances, soit comme des types de classes de permission.

  
Dans l'exemple ci-dessous, la classe `ReadOnly` est définie comme une sous-classe de `permissions.BasePermission`, et son instance est ensuite passée au paramètre `permissions` dans le décorateur `api_controller`.

    from ninja_extra import permissions, api_controller, ControllerBase
    
    class ReadOnly(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.method in permissions.SAFE_METHODS
    
    @api_controller(permissions=[permissions.IsAuthenticated | ReadOnly()])
    class SampleController(ControllerBase):
        pass
    

  
Dans l'exemple fourni, la classe `UserWithPermission` est utilisée pour évaluer différentes permissions pour différents contrôleurs ou fonctions de route.

Par exemple :

    from ninja_extra import permissions, api_controller, ControllerBase, http_post, http_delete
    
    class UserWithPermission(permissions.BasePermission):
        def __init__(self, permission: str) -> None:
            self._permission = permission
        
        def has_permission(self, request, view):
            return request.user.has_perm(self._permission)
    
    
    @api_controller('/blog')
    class BlogController(ControllerBase):
        @http_post('/', permissions=[permissions.IsAuthenticated & UserWithPermission('blog.add')])
        def add_blog(self):
            pass
        
        @http_delete('/', permissions=[permissions.IsAuthenticated & UserWithPermission('blog.delete')])
        def delete_blog(self):
            pass
    

  
Dans ce cas, la classe `UserWithPermission` est utilisée pour vérifier si l'utilisateur possède la permission `blog.add` pour accéder à l'action `add_blog` et la permission `blog.delete` pour accéder à l'action `delete_blog`. Les permissions sont explicitement configurées pour chaque fonction de route afin de permettre un contrôle fin de l'accès des utilisateurs en fonction de permissions spécifiques.

**AllowAny**
------------

  
La classe de permission `AllowAny` accorde un accès sans restriction, que la requête soit authentifiée ou non. Bien que non obligatoire, l'utilisation de cette classe de permission est optionnelle puisque vous pouvez obtenir le même résultat en définissant les permissions sur une liste ou un tuple vide. Cependant, spécifier la classe `AllowAny` peut être utile car elle communique clairement l'intention d'autoriser un accès sans restriction.

**IsAuthenticated**
-------------

  
La classe de permission `IsAuthenticated` refuse les permissions aux utilisateurs non authentifiés et accorde les permissions aux utilisateurs authentifiés.

  
Si vous avez l'intention de restreindre l'accès à l'API aux seuls utilisateurs enregistrés, cette permission est appropriée.

**IsAdminUser**
---------------

  
La classe de permission `IsAdminUser` refuse les permissions à tout utilisateur, sauf si `user.is_staff` est `True`, auquel cas la permission est accordée.

  
Si vous avez l'intention de restreindre l'accès à l'API à un sous-ensemble spécifique d'administrateurs de confiance, cette permission est appropriée.

**  
IsAuthenticatedOrReadOnly**
---------------

  
La classe de permission `IsAuthenticatedOrReadOnly` permet aux utilisateurs authentifiés d'effectuer n'importe quelle requête. Pour les utilisateurs non authentifiés, la requête n'est autorisée que lorsque la méthode est l'une des méthodes « sûres » (c'est-à-dire GET, HEAD ou OPTIONS).

  
Si vous souhaitez que votre API accorde des permissions de lecture aux utilisateurs anonymes tout en restreignant les permissions d'écriture aux utilisateurs authentifiés, cette permission est appropriée.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
