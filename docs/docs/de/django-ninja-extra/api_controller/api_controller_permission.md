**API-Controller-Berechtigungen**
================

  
Das Konzept des Berechtigungssystems stammt von Django DRF.

  
Berechtigungsprüfungen laufen immer am Anfang der Routen-Funktion, bevor ein anderer Code weiter ausgeführt werden darf. Berechtigungsprüfungen nutzen typischerweise die Authentifizierungsinformationen in den Attributen `request.user` und `request.auth`, um zu bestimmen, ob die eingehende Anfrage zulässig ist.

  
Berechtigungen werden verwendet, um verschiedenen Klassen von Benutzern den Zugriff auf verschiedene Teile der API zu gewähren oder zu verweigern.

  
Der einfachste Berechtigungsstil besteht darin, jedem authentifizierten Benutzer Zugriff zu gewähren und jedem nicht authentifizierten Benutzer den Zugriff zu verweigern. Dies entspricht der Klasse `IsAuthenticated` in Django Ninja Extra.

  
Ein etwas weniger strikter Berechtigungsstil besteht darin, authentifizierten Benutzern vollen Zugriff zu gewähren und nicht authentifizierten Benutzern nur Lesezugriff zu erlauben. Dies entspricht der Klasse `IsAuthenticatedOrReadOnly` in Django Ninja Extra.

### **Grenzen von Berechtigungen auf Objektebene**

  
Bei der Bearbeitung einer Anfrage wird die Methode `has_permission` automatisch für alle Berechtigungen aufgerufen, die in der Berechtigungsliste der Routen-Funktion angegeben sind. Da `has_object_permission` jedoch ein Objekt für die Berechtigungsvalidierung benötigt, wird sie nicht ausgelöst. Wenn Sie daher in einem Controller die Methoden `get_object_or_exception` oder `get_object_or_none` verwenden, um ein Objekt abzurufen, wird die Berechtigungsmethode `has_object_permission` aufgerufen.

**Benutzerdefinierte Berechtigungen**
----------

  
Um eine benutzerdefinierte Berechtigung zu implementieren, überschreiben Sie `BasePermission` und implementieren Sie eine oder beide der folgenden Methoden:

    .has_permission(self, request: HttpRequest, controller: "APIController")
    .has_object_permission(self, request: HttpRequest, controller: "APIController", obj: Any)
    

Beispiel

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
Unterstützte Berechtigungsoperatoren**
---------------

*   & (und) z. B.: `permissions.IsAuthenticated & ReadOnly`
*   | (oder) z. B.: `permissions.IsAuthenticated | ReadOnly`
*   ~ (nicht) z. B.: `~(permissions.IsAuthenticated & ReadOnly)`

**  
Verwendung von Berechtigungsobjekten in Controllern**
------------------

  
Das Berechtigungssystem von Ninja-Extra bietet Flexibilität bei der Definition von Berechtigungen und erlaubt es, Berechtigungen entweder als Instanzen oder als Typen von Berechtigungsklassen zu definieren.

  
Im folgenden Beispiel wird die Klasse `ReadOnly` als Unterklasse von `permissions.BasePermission` definiert, und ihre Instanz wird anschließend an den Parameter `permissions` im Decorator `api_controller` übergeben.

    from ninja_extra import permissions, api_controller, ControllerBase
    
    class ReadOnly(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.method in permissions.SAFE_METHODS
    
    @api_controller(permissions=[permissions.IsAuthenticated | ReadOnly()])
    class SampleController(ControllerBase):
        pass
    

  
Im bereitgestellten Beispiel wird die Klasse `UserWithPermission` verwendet, um unterschiedliche Berechtigungen für unterschiedliche Controller oder Routen-Funktionen auszuwerten.

Zum Beispiel:

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
    

  
In diesem Fall wird die Klasse `UserWithPermission` verwendet, um zu prüfen, ob der Benutzer die Berechtigung `blog.add` besitzt, um auf die Aktion `add_blog` zuzugreifen, und die Berechtigung `blog.delete`, um auf die Aktion `delete_blog` zuzugreifen. Berechtigungen werden für jede Routen-Funktion explizit konfiguriert, um eine feingranulare Kontrolle des Benutzerzugriffs auf der Grundlage spezifischer Berechtigungen zu ermöglichen.

**AllowAny**
------------

  
Die Berechtigungsklasse `AllowAny` gewährt uneingeschränkten Zugriff, unabhängig davon, ob die Anfrage authentifiziert ist. Die Verwendung dieser Berechtigungsklasse ist nicht erforderlich, sondern optional, da Sie dasselbe Ergebnis erzielen können, indem Sie Berechtigungen auf eine leere Liste oder ein leeres Tupel setzen. Die Angabe der Klasse `AllowAny` kann jedoch hilfreich sein, weil sie die Absicht, uneingeschränkten Zugriff zu erlauben, klar kommuniziert.

**IsAuthenticated**
-------------

  
Die Berechtigungsklasse `IsAuthenticated` verweigert nicht authentifizierten Benutzern die Berechtigungen und gewährt sie authentifizierten Benutzern.

  
Wenn Sie den API-Zugriff auf registrierte Benutzer beschränken möchten, ist diese Berechtigung angemessen.

**IsAdminUser**
---------------

  
Die Berechtigungsklasse `IsAdminUser` verweigert jedem Benutzer die Berechtigungen, es sei denn, `user.is_staff` ist `True`; in diesem Fall wird die Berechtigung gewährt.

  
Wenn Sie den API-Zugriff auf eine bestimmte Gruppe vertrauenswürdiger Administratoren beschränken möchten, ist diese Berechtigung angemessen.

**  
IsAuthenticatedOrReadOnly**
---------------

  
Die Berechtigungsklasse `IsAuthenticatedOrReadOnly` erlaubt authentifizierten Benutzern jede Anfrage. Für nicht authentifizierte Benutzer ist die Anfrage nur zulässig, wenn die Methode zu den „sicheren" Methoden gehört (d. h. GET, HEAD oder OPTIONS).

  
Wenn Ihre API anonymen Benutzern Leseberechtigungen gewähren und Schreibberechtigungen auf authentifizierte Benutzer beschränken soll, ist diese Berechtigung angemessen.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
