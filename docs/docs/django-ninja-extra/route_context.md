  
Django Ninja 额外提供了 RouteContext 对象，该对象在整个请求生命周期中都是可用的。该对象为将处理请求的路由处理程序持有重要属性。这些属性包括 Django `HttpRequest` 对象、路由处理程序的权限类列表、Django-Ninja 用于构建最终响应的临时响应对象以及调用路由函数所需的 kwargs 和 args。

  
需要注意的是，这些属性不是在请求开始时设置的，而是随着请求在不同阶段的推进，在到达路由函数执行之前变得可用。

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
    

如何访问 `RouteContext`
--------------------

  
在 Django Ninja Extra 中，可以使用 `self.context` 属性在控制器类中访问 `RouteContext` 对象。该属性在控制器类的实例级别可用，因此可以轻松访问 `RouteContext` 对象的属性和方法。

For example.

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
    

  
在该示例中，我们可以从请求对象的 `self.context` 属性中访问经过身份验证的 `user` 对象，该对象在控制器类中可用。这使我们可以轻松访问经过身份验证的用户的信息。

###   
使用 RouteContext 修改响应标头

  
`RouteContext` 对象为你提供了在响应数据返回给客户端之前进行操作所需的属性和方法。通过 RouteContext 对象，你可以轻松地修改特定请求返回的响应中的标头、状态或 cookie 数据。

  
例如，让我们在新的端点中添加额外的 `header` 信息，如下所示。

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
    

在架构中使用 `RouteContext`
----------------------

  
在模式验证期间，可能会出现需要访问请求对象的情况。Django Ninja Extra 通过提供一种在请求期间解析 `RouteContext` 对象的方法，使这变得容易，然后可以使用该对象来访问请求对象和任何其他必要的属性。这允许在验证过程中使用请求的上下文，从而使其更灵活和强大。

For example:

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
    

  
在上面的示例中，我们使用了 `service_resolver` ，一个依赖注入实用函数，来解析 `RouteContext` 对象。这使我们能够访问请求对象，我们使用它来构建存储详细信息的完整 URL。通过使用 `service_resolver` 访问路由上下文，我们可以轻松地访问请求对象，并在验证过程中使用它收集任何必要的信息。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
