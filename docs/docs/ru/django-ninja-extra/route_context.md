  
Django Ninja Extra предоставляет объект RouteContext, который доступен на протяжении всего жизненного цикла запроса. Этот объект хранит важные атрибуты для обработчика маршрута, который будет обрабатывать запрос. Эти атрибуты включают объект `HttpRequest` Django, список классов разрешений для обработчика маршрута, временный объект ответа, используемый Django-Ninja для построения финального ответа, а также kwargs и args, необходимые для вызова функции маршрута.

  
Обратите внимание, что эти атрибуты не устанавливаются в начале запроса, а становятся доступными по мере прохождения запросом различных этапов, прежде чем достигнет выполнения функции маршрута.

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
    

Как получить доступ к `RouteContext`
--------------------

  
В Django Ninja Extra объект `RouteContext` можно получить в классах контроллеров с помощью атрибута `self.context`. Этот атрибут доступен на уровне экземпляра класса контроллера, что упрощает доступ к атрибутам и методам объекта `RouteContext`.

Например.

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
    

  
В этом примере мы можем получить доступ к аутентифицированному объекту `user` через атрибут `self.context` объекта запроса, который доступен в классе контроллера. Это позволяет нам легко получать информацию об аутентифицированном пользователе.

###   
Использование RouteContext для изменения заголовков ответа

  
Объект `RouteContext` предоставляет вам атрибуты и методы, необходимые для манипуляции данными ответа перед их возвратом клиенту. Через объект RouteContext вы можете легко изменять заголовки, статус или данные cookie в ответе, возвращаемом для конкретного запроса.

  
Например, давайте добавим дополнительную информацию в `header` в новом эндпоинте, как показано ниже.

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
    

Использование `RouteContext` в схемах
----------------------

  
Во время валидации схемы могут возникнуть ситуации, когда вам необходим доступ к объекту запроса. Django Ninja Extra упрощает это, предоставляя способ разрешения объекта `RouteContext` во время запроса, который затем можно использовать для доступа к объекту запроса и любым другим необходимым атрибутам. Это позволяет использовать контекст запроса в процессе валидации, делая его более гибким и мощным.

Например:

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
    

  
В приведённом выше примере мы использовали `service_resolver` — служебную функцию внедрения зависимостей — для разрешения объекта `RouteContext`. Это позволяет нам получить доступ к объекту запроса, который мы используем для построения полного URL страницы деталей магазина. Используя `service_resolver` для доступа к контексту маршрута, мы можем легко получить объект запроса и использовать его для сбора любой необходимой информации в процессе валидации.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
