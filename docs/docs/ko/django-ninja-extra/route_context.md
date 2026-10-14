  
Django Ninja Extra는 요청 생명주기 전반에 걸쳐 사용할 수 있는 RouteContext 객체를 제공합니다. 이 객체는 요청을 처리할 라우트 핸들러에 대한 중요한 속성을 보유합니다. 이러한 속성에는 Django `HttpRequest` 객체, 라우트 핸들러의 권한 클래스 목록, Django-Ninja가 최종 응답을 구축하는 데 사용하는 임시 응답 객체, 그리고 라우트 함수를 호출하는 데 필요한 kwargs와 args가 포함됩니다.

  
이러한 속성은 요청 시작 시 설정되는 것이 아니라, 라우트 함수 실행에 도달하기 전에 요청이 여러 단계를 거치면서 사용 가능해진다는 점에 유의하세요.

    from pydantic import BaseModel as PydanticModel, Field
    
    class RouteContext(PydanticModel):
        """
        APIController Context which will be available to the class instance when handling request
        """
    
        class Config:
            arbitrary_types_allowed = True
    
        permission_classes: PermissionType = Field([])
        request: Union[Any, HttpRequest, None] = None
        response: Union[Any, HttpResponse, None] = None
        args: List[Any] = Field([])
        kwargs: DictStrAny = Field({})
    

`RouteContext`에 액세스하는 방법
--------------------

  
Django Ninja Extra에서 `RouteContext` 객체는 컨트롤러 클래스에서 `self.context` 속성을 사용하여 액세스할 수 있습니다. 이 속성은 컨트롤러 클래스의 인스턴스 수준에서 사용할 수 있어 `RouteContext` 객체의 속성과 메서드에 쉽게 액세스할 수 있습니다.

예를 들어.

    from ninja_extra import ControllerBase, api_controller, route
    from django.db import transaction
    from ninja_extra.permissions import IsAuthenticated
    from ninja_jwt.authentication import JWTAuth
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    
    @api_controller("/books", auth=JWTAuth(), permissions=[IsAuthenticated])
    class StoryBookSubscribeController(ControllerBase):
        @route.get(
            "/context",
            url_name="subscribe",
        )
        @transaction.atomic
        def subscribe(self):
            user = self.context.request.user
            return {'message': 'Authenticated User From context', 'email': user.email}
        
        @route.post(
            "/context",
            url_name="subscribe",
        )
        @transaction.atomic
        def subscribe_with_response_change(self):
            res = self.context.response
            res.headers.setdefault('x-custom-header', 'welcome to custom header in response')
            return {'message': 'Authenticated User From context and Response header modified', 'email': self.context.request.user.email}
    

  
이 예시에서 우리는 컨트롤러 클래스에서 사용 가능한 요청 객체의 `self.context` 속성에서 인증된 `user` 객체에 액세스할 수 있습니다. 이를 통해 인증된 사용자의 정보에 쉽게 액세스할 수 있습니다.

###   
RouteContext를 사용하여 응답 헤더 수정하기

  
`RouteContext` 객체는 응답이 클라이언트에 반환되기 전에 응답 데이터를 조작하는 데 필요한 속성과 메서드를 제공합니다. RouteContext 객체를 통해 특정 요청에 대해 반환되는 응답의 헤더, 상태 또는 쿠키 데이터를 쉽게 수정할 수 있습니다.

  
예를 들어, 아래와 같이 새 엔드포인트에 추가 `header` 정보를 추가해 봅시다.

    from ninja_extra import ControllerBase, api_controller, route
    from django.db import transaction
    from ninja_extra.permissions import IsAuthenticated
    from ninja_jwt.authentication import JWTAuth
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    
    @api_controller("/books", auth=JWTAuth(), permissions=[IsAuthenticated])
    class StoryBookSubscribeController(ControllerBase):
        @route.post(
            "/context-response",
            url_name="response",
        )
        @transaction.atomic
        def subscribe_with_response_change(self):
            res = self.context.response
            res.headers['x-custom-header'] = 'welcome to custom header in response'
            return {'message': 'Authenticated User From context and Response header modified', 'email': self.context.request.user.email}
    

스키마에서 `RouteContext` 사용하기
----------------------

  
스키마 검증 중에 요청 객체에 액세스해야 하는 상황이 발생할 수 있습니다. Django Ninja Extra는 요청 중에 `RouteContext` 객체를 해석하는 방법을 제공하여 이를 쉽게 만들며, 이를 통해 요청 객체와 기타 필요한 속성에 액세스할 수 있습니다. 이를 통해 검증 프로세스 중에 요청의 컨텍스트를 사용할 수 있어 더 유연하고 강력해집니다.

예를 들어:

    from typing import Optional
    from django.urls import reverse
    from ninja_extra import service_resolver
    from ninja_extra.controllers import RouteContext
    from ninja import ModelSchema
    from pydantic import AnyHttpUrl, validator
    
    
    class StoreBookSchema(ModelSchema):
        borrowed_by: Optional[UserRetrieveSchema]
        store: AnyHttpUrl
        book: BookSchema
    
        class Config:
            model = StoreBook
            model_fields = ['borrowed_by', 'store', 'book']
    
        @validator("store", pre=True, check_fields=False)
        def store_validate(cls, value_data):
            context: RouteContext = service_resolver(RouteContext)
            value = reverse("store:detail", kwargs=dict(store_id=value_data.id))
            return context.request.build_absolute_uri(value)
    

  
위 예시에서 우리는 의존성 주입 유틸리티 함수인 `service_resolver`를 사용하여 `RouteContext` 객체를 해석했습니다. 이를 통해 요청 객체에 액세스할 수 있으며, 이를 사용하여 스토어 세부 정보에 대한 전체 URL을 구축합니다. `service_resolver`를 사용하여 라우트 컨텍스트에 액세스함으로써 요청 객체에 쉽게 액세스하고 검증 프로세스 중에 필요한 정보를 수집하는 데 사용할 수 있습니다.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
