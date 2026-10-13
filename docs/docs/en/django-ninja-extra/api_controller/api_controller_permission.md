**API Controller Permissions**
================

  
The concept of the permission system is derived from Django DRF.

  
Permission checks always run at the beginning of the route function, before any other code is allowed to continue. Permission checks will typically use the authentication information in the `request.user` and `request.auth` attributes to determine whether the incoming request should be permitted.

  
Permissions are used to grant or deny access to different parts of the API for different classes of users.

  
The simplest permission style is to allow access to any authenticated user and deny access to any unauthenticated user. This corresponds to the `IsAuthenticated` class in Django Ninja Extra.

  
A slightly less strict permission style is to allow authenticated users full access and allow unauthenticated users read-only access. This corresponds to the `IsAuthenticatedOrReadOnly` class in Django Ninja Extra.

### **Limitations of Object-Level Permissions**

  
When handling a request, the `has_permission` method is automatically called for all permissions specified in the route function's permission list. However, since `has_object_permission` requires an object for permission validation, it is not triggered. Therefore, when using the `get_object_or_exception` or `get_object_or_none` methods in a controller to retrieve an object, the `has_object_permission` permission method will be called.

**Custom Permissions**
----------

  
To implement a custom permission, override `BasePermission` and implement one or both of the following methods:

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
Supported Permission Operators**
---------------

*   & (and) eg: `permissions.IsAuthenticated & ReadOnly`
*   | (or) eg: `permissions.IsAuthenticated | ReadOnly`
*   ~ (not) eg: `~(permissions.IsAuthenticated & ReadOnly)`

**  
Using Permission Objects in Controllers**
------------------

  
The Ninja-Extra permission system provides flexibility when defining permissions, allowing permissions to be defined as either instances or types of permission classes.

  
In the example below, the `ReadOnly` class is defined as a subclass of `permissions.BasePermission`, and its instance is then passed to the `permissions` parameter in the `api_controller` decorator.

    from ninja_extra import permissions, api_controller, ControllerBase
    
    class ReadOnly(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.method in permissions.SAFE_METHODS
    
    @api_controller(permissions=[permissions.IsAuthenticated | ReadOnly()])
    class SampleController(ControllerBase):
        pass
    

  
In the provided example, the `UserWithPermission` class is used to evaluate different permissions for different controllers or route functions.

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
    

  
In this case, the `UserWithPermission` class is used to verify whether the user has the `blog.add` permission to access the `add_blog` action and the `blog.delete` permission to access the `delete_blog` action. Permissions are explicitly configured for each route function to enable fine-grained control over user access based on specific permissions.

**AllowAny**
------------

  
The `AllowAny` permission class grants unrestricted access, regardless of whether the request is authenticated. While not required, using this permission class is optional since you can achieve the same result by setting permissions to an empty list or tuple. However, specifying the `AllowAny` class can be helpful because it clearly communicates the intent to allow unrestricted access.

**IsAuthenticated**
-------------

  
The `IsAuthenticated` permission class denies permissions to unauthenticated users and grants permissions to authenticated users.

  
If you intend to restrict API access to registered users only, this permission is appropriate.

**IsAdminUser**
---------------

  
The `IsAdminUser` permission class denies permissions to any user unless `user.is_staff` is `True`, in which case permission is granted.

  
If you intend to restrict API access to a specific subset of trusted administrators, this permission is appropriate.

**  
IsAuthenticatedOrReadOnly**
---------------

  
The `IsAuthenticatedOrReadOnly` permission class allows authenticated users to make any request. For unauthenticated users, the request is only permitted when the method is one of the "safe" methods (i.e., GET, HEAD, or OPTIONS).

  
If you want your API to grant read permissions to anonymous users while restricting write permissions to authenticated users, this permission is appropriate.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
