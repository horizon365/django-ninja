**API Controller-machtigingen**
================

  
Het concept van het machtigingensysteem is afgeleid van Django DRF.

  
Machtigingscontroles worden altijd uitgevoerd aan het begin van de routefunctie, voordat andere code mag doorgaan. Machtigingscontroles gebruiken doorgaans de authenticatie-informatie in de attributen `request.user` en `request.auth` om te bepalen of het inkomende request moet worden toegestaan.

  
Machtigingen worden gebruikt om verschillende klassen van gebruikers toegang te verlenen tot verschillende delen van de API, of deze te ontzeggen.

  
De eenvoudigste machtigingsstijl is toegang verlenen aan elke geauthenticeerde gebruiker en toegang ontzeggen aan elke niet-geauthenticeerde gebruiker. Dit komt overeen met de klasse `IsAuthenticated` in Django Ninja Extra.

  
Een iets minder strenge machtigingsstijl is geauthenticeerde gebruikers volledige toegang geven en niet-geauthenticeerde gebruikers alleen-lezen toegang geven. Dit komt overeen met de klasse `IsAuthenticatedOrReadOnly` in Django Ninja Extra.

### **Beperkingen van machtigingen op objectniveau**

  
Bij het afhandelen van een request wordt de methode `has_permission` automatisch aangeroepen voor alle machtigingen die zijn opgegeven in de machtigingenlijst van de routefunctie. Aangezien `has_object_permission` echter een object vereist voor machtigingsvalidatie, wordt deze niet geactiveerd. Daarom wordt, wanneer je in een controller de methoden `get_object_or_exception` of `get_object_or_none` gebruikt om een object op te halen, de machtigingsmethode `has_object_permission` aangeroepen.

**Aangepaste machtigingen**
----------

  
Om een aangepaste machtiging te implementeren, overschrijf je `BasePermission` en implementeer je een of beide van de volgende methoden:

    .has_permission(self, request: HttpRequest, controller: "APIController")
    .has_object_permission(self, request: HttpRequest, controller: "APIController", obj: Any)
    

Voorbeeld

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
Ondersteunde machtigingsoperatoren**
---------------

*   & (and) bijv.: `permissions.IsAuthenticated & ReadOnly`
*   | (or) bijv.: `permissions.IsAuthenticated | ReadOnly`
*   ~ (not) bijv.: `~(permissions.IsAuthenticated & ReadOnly)`

**  
Machtigingsobjecten gebruiken in controllers**
------------------

  
Het machtigingensysteem van Ninja-Extra biedt flexibiliteit bij het definiëren van machtigingen, waarbij machtigingen kunnen worden gedefinieerd als instanties of als typen van machtigingsklassen.

  
In het onderstaande voorbeeld is de klasse `ReadOnly` gedefinieerd als een subklasse van `permissions.BasePermission`, en wordt vervolgens de instantie ervan doorgegeven aan de parameter `permissions` in de decorator `api_controller`.

    from ninja_extra import permissions, api_controller, ControllerBase
    
    class ReadOnly(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.method in permissions.SAFE_METHODS
    
    @api_controller(permissions=[permissions.IsAuthenticated | ReadOnly()])
    class SampleController(ControllerBase):
        pass
    

  
In het gegeven voorbeeld wordt de klasse `UserWithPermission` gebruikt om verschillende machtigingen voor verschillende controllers of routefuncties te evalueren.

Bijvoorbeeld:

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
    

  
In dit geval wordt de klasse `UserWithPermission` gebruikt om te verifiëren of de gebruiker de machtiging `blog.add` heeft om de actie `add_blog` te openen en de machtiging `blog.delete` om de actie `delete_blog` te openen. Machtigingen worden expliciet geconfigureerd per routefunctie om fijnmazige controle over gebruikerstoegang mogelijk te maken op basis van specifieke machtigingen.

**AllowAny**
------------

  
De machtigingsklasse `AllowAny` verleent onbeperkte toegang, ongeacht of het request is geauthenticeerd. Hoewel het niet vereist is, is het gebruik van deze machtigingsklasse optioneel, omdat je hetzelfde resultaat kunt bereiken door machtigingen in te stellen op een lege lijst of tuple. Het specificeren van de klasse `AllowAny` kan echter nuttig zijn, omdat het duidelijk de intentie communiceert om onbeperkte toegang toe te staan.

**IsAuthenticated**
-------------

  
De machtigingsklasse `IsAuthenticated` ontzegt machtigingen aan niet-geauthenticeerde gebruikers en verleent machtigingen aan geauthenticeerde gebruikers.

  
Als je API-toegang wilt beperken tot alleen geregistreerde gebruikers, is deze machtiging passend.

**IsAdminUser**
---------------

  
De machtigingsklasse `IsAdminUser` ontzegt machtigingen aan elke gebruiker, tenzij `user.is_staff` `True` is, in welk geval de machtiging wordt verleend.

  
Als je API-toegang wilt beperken tot een specifieke subset van vertrouwde beheerders, is deze machtiging passend.

**  
IsAuthenticatedOrReadOnly**
---------------

  
De machtigingsklasse `IsAuthenticatedOrReadOnly` staat geauthenticeerde gebruikers toe om elk request te doen. Voor niet-geauthenticeerde gebruikers wordt het request alleen toegestaan wanneer de methode een van de "veilige" methoden is (dus GET, HEAD of OPTIONS).

  
Als je API leesmachtigingen wilt verlenen aan anonieme gebruikers terwijl schrijfmachtigingen worden beperkt tot geauthenticeerde gebruikers, is deze machtiging passend.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
