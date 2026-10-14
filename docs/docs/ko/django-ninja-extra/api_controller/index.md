**컨트롤러**
==============

  
Ninja-Extra API 컨트롤러는 들어오는 요청을 처리하고 클라이언트에 응답을 반환하는 역할을 합니다.

  
Ninja-Extra에는 컨트롤러 모델을 생성하기 위한 몇 가지 주요 구성 요소가 있습니다:

*   ControllerBase
*   APIController 데코레이터

ControllerBase
--------------

  
`ControllerBase` 클래스는 Django Ninja Extra의 모든 컨트롤러에 대한 기본 클래스입니다. 요청을 처리하고, 입력을 검증하고, 클래스 기반 방식으로 응답을 반환하기 위한 핵심 기능을 제공합니다.

  
이 클래스에는 `request` 객체, `permission_classes`, `response` 객체와 같이 모든 컨트롤러에 공통적인 속성과 메서드가 포함되어 있으며, 이들은 `RouteContext`의 일부입니다. request 객체에는 헤더, 쿼리 파라미터 및 본문 데이터와 같은 들어오는 요청에 대한 정보가 포함되어 있습니다. permission_classes 속성은 컨트롤러의 라우트에 액세스하는 데 필요한 권한을 정의하는 데 사용되며, response 객체는 클라이언트에 반환되는 최종 응답을 구축하는 데 사용됩니다.

  
핵심 속성 외에도 `ControllerBase` 클래스에는 객체 권한 검사(`check_object_permission`), 빠른 응답 생성(`create_response`), 데이터베이스에서 데이터 가져오기(`get_object_or_exception`)와 같은 일반적인 작업을 처리하는 데 사용할 수 있는 유틸리티 메서드도 포함되어 있습니다. 이러한 메서드는 서브클래스에서 오버라이드하여 커스텀 동작을 제공할 수 있습니다.

  
컨트롤러 기본 클래스에는 애플리케이션의 다른 서비스 및 객체(예: 리포지토리 서비스)에 쉽게 액세스할 수 있도록 하는 의존성 주입 시스템도 포함되어 있습니다.

    from ninja_extra import ControllerBase, api_controller
    
    @api_controller('/users')
    class UserControllerBase(ControllerBase):
        ...
    

APIController 데코레이터
------------------

  
`api_controller` 데코레이터는 Django Ninja Extra에서 클래스 기반 컨트롤러를 정의하는 데 사용됩니다. ControllerBase 클래스에 적용되며 컨트롤러의 라우팅 및 기능을 구성하기 위한 여러 파라미터를 받습니다.

  
첫 번째 파라미터인 `prefix_or_class`는 그룹화된 컨트롤러 아래에 등록된 모든 라우트의 접두사 문자열이거나 데코레이터가 적용되는 클래스 객체입니다.

  
두 번째 파라미터인 `auth`는 컨트롤러의 라우트에 적용되어야 하는 모든 Django Ninja Auth 클래스의 목록입니다.

  
세 번째 파라미터인 `tags`는 OPENAPI 태깅 목적으로 사용되는 문자열 목록입니다.

  
네 번째 파라미터인 `permissions`는 컨트롤러의 라우트에 적용되어야 하는 모든 권한의 목록입니다.

  
다섯 번째 파라미터인 `auto_import`는 기본값이 true이며 컨트롤러를 자동 임포트 목록에 자동으로 추가합니다.

예를 들어:

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
    

  
위 코드에서 우리는 `api_controller` 데코레이터를 사용하여 `UsersController`라는 컨트롤러를 정의했습니다. 데코레이터는 클래스에 적용되며 두 개의 인수, 즉 URL 엔드포인트 `/users`와 `auth` 및 `permission` 클래스를 받습니다. `get_users`와 `create_user`는 들어오는 GET `/users` 및 POST `/users/create` 요청을 처리하는 라우트 함수입니다.

  
!!!info ControllerBase 클래스에서 상속하면 더 많은 IDE IntelliSense 지원을 받을 수 있습니다.

빠른 예제
-------------

  
Django 사용자 모델을 적절히 관리하기 위한 APIController를 만들어 봅시다

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
    

  
위 예시에서 `UsersController` 클래스는 `create_user`, `update_user`, `delete_user`, `list_user`, `get_user_by_id`와 같은 서로 다른 HTTP 메서드에 해당하는 여러 메서드를 정의합니다. 이러한 메서드는 각각 `http_post`, `http_generic`, `http_delete`, `http_get` 데코레이터로 데코레이트됩니다.

  
`create_user` 메서드는 `http_post` 데코레이터를 사용하며 입력 데이터를 검증하고 직렬화하는 데 사용되는 `ModelSchema`인 `UserSchema` 타입의 user 파라미터를 받습니다. 이 메서드는 시스템에서 새 사용자를 생성하는 데 사용되며 사용자의 `ID`를 반환합니다.

  
`update_user` 메서드는 `http_generic` 데코레이터를 사용하며 int 타입의 `user_id` 파라미터를 받습니다. 데코레이터는 `PUT` 및 `PATCH` 메서드를 처리하도록 구성되며 사용자 객체를 직렬화하는 데 사용되는 `UserSchema` 타입의 응답 파라미터를 제공합니다.

  
`delete_user` 메서드는 `http_delete` 데코레이터를 사용하며 int 타입의 `user_id` 파라미터와 Detail 타입의 응답 파라미터를 받으며, 성공 시 빈 본문과 함께 204 상태 코드를 반환합니다.

  
`list_user` 메서드는 `http_get` 데코레이터를 사용하며 `pagination.paginate` 데코레이터로 데코레이트되어 있습니다. 이 데코레이터는 `PageNumberPaginationExtra` 클래스를 사용하여 메서드의 결과를 페이지당 50개의 결과로 페이지네이션합니다. 또한 메서드가 반환하는 사용자 목록을 직렬화하고 페이지네이션하는 데 사용될 `pagination.PaginatedResponseSchema[UserSchema]` 타입의 응답 파라미터도 제공합니다.

  
`get_user_by_id` 메서드는 `http_get` 데코레이터를 사용하며 int 타입의 `user_id` 파라미터와 UserSchema 타입의 응답 파라미터를 받으며, 이는 사용자 객체를 직렬화하는 데 사용됩니다.

  
사용자 컨트롤러는 또한 `self.get_object_or_exception(self.user_model, id=user_id)`를 사용하는데, 이는 사용자 객체를 찾을 수 없는 경우 예외를 발생시키는 헬퍼 메서드입니다.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
