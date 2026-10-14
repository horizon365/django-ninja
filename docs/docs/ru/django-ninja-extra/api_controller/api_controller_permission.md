**Разрешения API Controller**
================

  
Концепция системы разрешений взята из Django DRF.

  
Проверки разрешений всегда выполняются в начале функции маршрута, прежде чем какой-либо другой код сможет продолжить выполнение. Проверки разрешений обычно используют информацию аутентификации в атрибутах `request.user` и `request.auth`, чтобы определить, следует ли разрешить входящий запрос.

  
Разрешения используются для предоставления или запрета доступа к различным частям API для разных категорий пользователей.

  
Простейший стиль разрешений — разрешать доступ любому аутентифицированному пользователю и запрещать доступ любому неаутентифицированному пользователю. Этому соответствует класс `IsAuthenticated` в Django Ninja Extra.

  
Чуть менее строгий стиль разрешений — предоставлять аутентифицированным пользователям полный доступ и разрешать неаутентифицированным пользователям доступ только для чтения. Этому соответствует класс `IsAuthenticatedOrReadOnly` в Django Ninja Extra.

### **Ограничения разрешений на уровне объектов**

  
При обработке запроса метод `has_permission` автоматически вызывается для всех разрешений, указанных в списке разрешений функции маршрута. Однако, поскольку `has_object_permission` требует объект для проверки разрешений, он не срабатывает. Поэтому при использовании методов `get_object_or_exception` или `get_object_or_none` в контроллере для получения объекта будет вызван метод разрешений `has_object_permission`.

**Кастомные разрешения**
----------

  
Чтобы реализовать кастомное разрешение, переопределите `BasePermission` и реализуйте один или оба из следующих методов:

    .has_permission(self, request: HttpRequest, controller: "APIController")
    .has_object_permission(self, request: HttpRequest, controller: "APIController", obj: Any)
    

Пример

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
Поддерживаемые операторы разрешений**
---------------

*   & (and) например: `permissions.IsAuthenticated & ReadOnly`
*   | (or) например: `permissions.IsAuthenticated | ReadOnly`
*   ~ (not) например: `~(permissions.IsAuthenticated & ReadOnly)`

**  
Использование объектов разрешений в контроллерах**
------------------

  
Система разрешений Ninja-Extra обеспечивает гибкость при определении разрешений, позволяя задавать разрешения как в виде экземпляров, так и в виде типов классов разрешений.

  
В приведённом ниже примере класс `ReadOnly` определён как подкласс `permissions.BasePermission`, и его экземпляр затем передаётся в параметр `permissions` декоратора `api_controller`.

    from ninja_extra import permissions, api_controller, ControllerBase
    
    class ReadOnly(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.method in permissions.SAFE_METHODS
    
    @api_controller(permissions=[permissions.IsAuthenticated | ReadOnly()])
    class SampleController(ControllerBase):
        pass
    

  
В приведённом примере класс `UserWithPermission` используется для проверки различных разрешений для разных контроллеров или функций маршрутов.

Например:

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
    

  
В этом случае класс `UserWithPermission` используется для проверки того, есть ли у пользователя разрешение `blog.add` для доступа к действию `add_blog` и разрешение `blog.delete` для доступа к действию `delete_blog`. Разрешения явно настраиваются для каждой функции маршрута, что обеспечивает точный контроль доступа пользователей на основе конкретных разрешений.

**AllowAny**
------------

  
Класс разрешений `AllowAny` предоставляет неограниченный доступ, независимо от того, аутентифицирован запрос или нет. Хотя это не обязательно, использование этого класса разрешений необязательно, поскольку того же результата можно достичь, установив permissions в пустой список или кортеж. Однако указание класса `AllowAny` может быть полезным, поскольку он явно сообщает о намерении разрешить неограниченный доступ.

**IsAuthenticated**
-------------

  
Класс разрешений `IsAuthenticated` запрещает разрешения неаутентифицированным пользователям и предоставляет разрешения аутентифицированным пользователям.

  
Если вы намерены ограничить доступ к API только зарегистрированными пользователями, это разрешение подходит.

**IsAdminUser**
---------------

  
Класс разрешений `IsAdminUser` запрещает разрешения любому пользователю, если только `user.is_staff` не равно `True` — в этом случае разрешение предоставляется.

  
Если вы намерены ограничить доступ к API конкретной группой доверенных администраторов, это разрешение подходит.

**  
IsAuthenticatedOrReadOnly**
---------------

  
Класс разрешений `IsAuthenticatedOrReadOnly` позволяет аутентифицированным пользователям выполнять любые запросы. Для неаутентифицированных пользователей запрос разрешается только тогда, когда метод является одним из «безопасных» методов (т.е. GET, HEAD или OPTIONS).

  
Если вы хотите, чтобы ваш API предоставлял разрешения на чтение анонимным пользователям, ограничивая разрешения на запись аутентифицированными пользователями, это разрешение подходит.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
