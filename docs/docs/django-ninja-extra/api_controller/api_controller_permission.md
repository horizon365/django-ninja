**API 控制器权限**
================

  
该权限系统的概念来源于 Django DRF。

  
权限检查始终在路由函数的开头运行，即在允许任何其他代码继续之前运行。权限检查通常将使用 `request.user` 和 `request.auth` 属性中的身份验证信息来确定传入的请求是否应该被允许。

  
权限用于授予或拒绝不同类别的用户对 API 的不同部分的访问权限。

  
最简单的权限样式是允许任何经过身份验证的用户访问，并拒绝任何未经身份验证的用户访问。这对应于 Django Ninja Extra 中的 `IsAuthenticated` 类。

  
一种稍微不那么严格的权限风格是允许经过身份验证的用户完全访问，而允许未经身份验证的用户只读访问。这对应于 Django Ninja Extra 中的 `IsAuthenticatedOrReadOnly` 类。

### **对象级权限的限制**

  
在处理请求时，将自动为路由函数的权限列表中指定的所有权限调用 `has_permission` 方法。但是，由于 `has_object_permission` 需要对象进行权限验证，因此不会触发。因此，在控制器中使用 `get_object_or_exception` 或 `get_object_or_none` 方法检索对象时，将调用 `has_object_permission` 权限方法。

**自定义权限**
----------

  
要实现自定义权限，请重写 `BasePermission` 并实现以下方法之一或两者：

    .has_permission(self, request: HttpRequest, controller: "APIController")
    .has_object_permission(self, request: HttpRequest, controller: "APIController", obj: Any)
    

Example

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
支持的权限操作符**
---------------

*   & (and) eg: `permissions.IsAuthenticated & ReadOnly`
*   | (or) eg: `permissions.IsAuthenticated | ReadOnly`
*   ~ (not) eg: `~(permissions.IsAuthenticated & ReadOnly)`

**  
在控制器中使用权限对象**
------------------

  
Ninja-Extra 权限系统提供了在定义权限时的灵活性，可以将权限定义为权限类的实例或类型。

  
在下面的示例中， `ReadOnly` 类被定义为 `permissions.BasePermission` 的子类，然后将其实例传递给 `api_controller` 装饰器中的 `permissions` 参数。

    from ninja_extra import permissions, api_controller, ControllerBase
    
    class ReadOnly(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.method in permissions.SAFE_METHODS
    
    @api_controller(permissions=[permissions.IsAuthenticated | ReadOnly()])
    class SampleController(ControllerBase):
        pass
    

  
在提供的示例中，使用了 `UserWithPermission` 类来评估不同控制器或路由函数的不同权限。

For instance:

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
    

  
在这种情况下，使用 `UserWithPermission` 类来验证用户是否拥有访问 `add_blog` 操作的 `blog.add` 权限以及访问 `delete_blog` 操作的 `blog.delete` 权限。对于每个路由函数都明确配置了权限，以便根据特定权限对用户访问进行精细控制。

**AllowAny**
------------

  
`AllowAny` 权限类授予无限制的访问权限，无论请求是否经过身份验证。虽然不是必需的，但使用此权限类是可选的，因为您可以通过为空列表或元组设置权限来实现相同的结果。但是，指定 `AllowAny` 类可能会有所帮助，因为它明确传达了允许无限制访问的意图。

**是否经过身份验证**
-------------

  
`IsAuthenticated` 权限类拒绝未经身份验证的用户的权限，并授予经过身份验证的用户的权限。

  
如果您打算仅将 API 访问权限限制给注册用户，那么此权限是合适的。

**IsAdminUser**
---------------

  
`IsAdminUser` 权限类拒绝向任何用户授予权限，除非 `user.is_staff` 是 `True` ，在这种情况下授予权限。

  
如果您打算将 API 访问权限限制为特定的受信任管理员子集，那么此权限很合适。

**  
是否已验证或只读**
---------------

  
`IsAuthenticatedOrReadOnly` 权限类允许经过身份验证的用户执行任何请求。对于未经身份验证的用户，只有当方法是“安全”方法之一时（即 GET、HEAD 或 OPTIONS），请求才会被允许。

  
如果您希望 API 向匿名用户授予读取权限，同时限制经过身份验证的用户的写入权限，那么此权限是合适的。
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
