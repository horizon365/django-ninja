  
Django Ninja Extra provides the RouteContext object, which is available throughout the request lifecycle. This object holds important attributes for the route handler that will process the request. These attributes include the Django `HttpRequest` object, the list of permission classes for the route handler, the temporary response object used by Django-Ninja to build the final response, and the kwargs and args needed to call the route function.

  
Note that these attributes are not set at the start of the request, but become available as the request progresses through different stages, before reaching route function execution.

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
    

How to Access `RouteContext`
--------------------

  
In Django Ninja Extra, the `RouteContext` object can be accessed in controller classes using the `self.context` attribute. This attribute is available at the instance level of the controller class, making it easy to access the attributes and methods of the `RouteContext` object.

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
    

  
In this example, we can access the authenticated `user` object from the `self.context` attribute of the request object, which is available in the controller class. This allows us to easily access the authenticated user's information.

###   
Using RouteContext to Modify Response Headers

  
The `RouteContext` object provides you with the attributes and methods needed to manipulate the response data before it is returned to the client. Through the RouteContext object, you can easily modify the headers, status, or cookie data in the response returned for a specific request.

  
For example, let's add additional `header` information in a new endpoint, as shown below.

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
    

Using `RouteContext` in Schemas
----------------------

  
During schema validation, situations may arise where you need to access the request object. Django Ninja Extra makes this easy by providing a way to resolve the `RouteContext` object during the request, which can then be used to access the request object and any other necessary attributes. This allows the request's context to be used during the validation process, making it more flexible and powerful.

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
    

  
In the above example, we used `service_resolver`, a dependency injection utility function, to resolve the `RouteContext` object. This allows us to access the request object, which we use to build the full URL for the store details. By using `service_resolver` to access the route context, we can easily access the request object and use it to gather any necessary information during the validation process.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
