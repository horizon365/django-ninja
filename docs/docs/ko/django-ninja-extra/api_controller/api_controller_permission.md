**API 컨트롤러 권한**
================

  
권한 시스템의 개념은 Django DRF에서 파생되었습니다.

  
권한 검사는 항상 라우트 함수의 시작 부분에서 실행되며, 다른 코드가 계속 진행되기 전에 실행됩니다. 권한 검사는 일반적으로 `request.user` 및 `request.auth` 속성의 인증 정보를 사용하여 들어오는 요청이 허용되어야 하는지 여부를 결정합니다.

  
권한은 서로 다른 클래스의 사용자에게 API의 서로 다른 부분에 대한 액세스를 부여하거나 거부하는 데 사용됩니다.

  
가장 간단한 권한 스타일은 인증된 모든 사용자에게 액세스를 허용하고 인증되지 않은 모든 사용자에게 액세스를 거부하는 것입니다. 이는 Django Ninja Extra의 `IsAuthenticated` 클래스에 해당합니다.

  
약간 덜 엄격한 권한 스타일은 인증된 사용자에게 전체 액세스를 허용하고 인증되지 않은 사용자에게 읽기 전용 액세스를 허용하는 것입니다. 이는 Django Ninja Extra의 `IsAuthenticatedOrReadOnly` 클래스에 해당합니다.

### **객체 수준 권한의 제한 사항**

  
요청을 처리할 때 라우트 함수의 권한 목록에 지정된 모든 권한에 대해 `has_permission` 메서드가 자동으로 호출됩니다. 그러나 `has_object_permission`은 권한 검증을 위해 객체가 필요하기 때문에 트리거되지 않습니다. 따라서 컨트롤러에서 `get_object_or_exception` 또는 `get_object_or_none` 메서드를 사용하여 객체를 검색할 때 `has_object_permission` 권한 메서드가 호출됩니다.

**커스텀 권한**
----------

  
커스텀 권한을 구현하려면 `BasePermission`을 오버라이드하고 다음 메서드 중 하나 또는 둘 다를 구현하세요:

    .has_permission(self, request: HttpRequest, controller: "APIController")
    .has_object_permission(self, request: HttpRequest, controller: "APIController", obj: Any)
    

예시

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
지원되는 권한 연산자**
---------------

*   & (and) 예: `permissions.IsAuthenticated & ReadOnly`
*   | (or) 예: `permissions.IsAuthenticated | ReadOnly`
*   ~ (not) 예: `~(permissions.IsAuthenticated & ReadOnly)`

**  
컨트롤러에서 권한 객체 사용하기**
------------------

  
Ninja-Extra 권한 시스템은 권한을 정의할 때 유연성을 제공하며, 권한을 권한 클래스의 인스턴스 또는 타입으로 정의할 수 있습니다.

  
아래 예시에서 `ReadOnly` 클래스는 `permissions.BasePermission`의 서브클래스로 정의되며, 그 인스턴스가 `api_controller` 데코레이터의 `permissions` 파라미터로 전달됩니다.

    from ninja_extra import permissions, api_controller, ControllerBase
    
    class ReadOnly(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.method in permissions.SAFE_METHODS
    
    @api_controller(permissions=[permissions.IsAuthenticated | ReadOnly()])
    class SampleController(ControllerBase):
        pass
    

  
제공된 예시에서 `UserWithPermission` 클래스는 서로 다른 컨트롤러 또는 라우트 함수에 대해 서로 다른 권한을 평가하는 데 사용됩니다.

예를 들어:

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
    

  
이 경우 `UserWithPermission` 클래스는 사용자가 `add_blog` 작업에 액세스하기 위한 `blog.add` 권한과 `delete_blog` 작업에 액세스하기 위한 `blog.delete` 권한을 보유하고 있는지 확인하는 데 사용됩니다. 권한은 특정 권한에 기반한 사용자 액세스에 대한 세분화된 제어를 가능하게 하기 위해 각 라우트 함수에 대해 명시적으로 구성됩니다.

**AllowAny**
------------

  
`AllowAny` 권한 클래스는 요청이 인증되었는지 여부에 관계없이 무제한 액세스를 부여합니다. 권한을 빈 리스트 또는 튜플로 설정하여 동일한 결과를 얻을 수 있기 때문에 이 권한 클래스를 사용하는 것은 필수는 아니며 선택 사항입니다. 그러나 `AllowAny` 클래스를 지정하면 무제한 액세스를 허용하려는 의도를 명확하게 전달하기 때문에 도움이 될 수 있습니다.

**IsAuthenticated**
-------------

  
`IsAuthenticated` 권한 클래스는 인증되지 않은 사용자에게 권한을 거부하고 인증된 사용자에게 권한을 부여합니다.

  
API 액세스를 등록된 사용자로만 제한하려는 경우 이 권한이 적합합니다.

**IsAdminUser**
---------------

  
`IsAdminUser` 권한 클래스는 `user.is_staff`가 `True`인 경우를 제외하고 모든 사용자에게 권한을 거부하며, `True`인 경우 권한이 부여됩니다.

  
API 액세스를 신뢰할 수 있는 관리자의 특정 하위 집합으로 제한하려는 경우 이 권한이 적합합니다.

**  
IsAuthenticatedOrReadOnly**
---------------

  
`IsAuthenticatedOrReadOnly` 권한 클래스는 인증된 사용자가 모든 요청을 할 수 있도록 허용합니다. 인증되지 않은 사용자의 경우 메서드가 "안전한" 메서드(즉, GET, HEAD 또는 OPTIONS) 중 하나인 경우에만 요청이 허용됩니다.

  
API가 익명 사용자에게 읽기 권한을 부여하면서 쓰기 권한을 인증된 사용자로 제한하려는 경우 이 권한이 적합합니다.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
