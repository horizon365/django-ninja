  
Django Ninja Extra fournit l'objet RouteContext, qui est disponible tout au long du cycle de vie de la requête. Cet objet contient des attributs importants pour le gestionnaire de route qui traitera la requête. Ces attributs incluent l'objet `HttpRequest` de Django, la liste des classes de permissions pour le gestionnaire de route, l'objet de réponse temporaire utilisé par Django-Ninja pour construire la réponse finale, ainsi que les kwargs et args nécessaires à l'appel de la fonction de route.

  
Notez que ces attributs ne sont pas définis au début de la requête, mais deviennent disponibles à mesure que la requête progresse à travers les différentes étapes, avant d'atteindre l'exécution de la fonction de route.

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
    

Comment accéder à `RouteContext`
--------------------

  
Dans Django Ninja Extra, l'objet `RouteContext` est accessible dans les classes de contrôleur à l'aide de l'attribut `self.context`. Cet attribut est disponible au niveau de l'instance de la classe de contrôleur, ce qui facilite l'accès aux attributs et méthodes de l'objet `RouteContext`.

Par exemple.

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
    

  
Dans cet exemple, nous pouvons accéder à l'objet `user` authentifié à partir de l'attribut `self.context` de l'objet request, qui est disponible dans la classe de contrôleur. Cela nous permet d'accéder facilement aux informations de l'utilisateur authentifié.

###   
Utiliser RouteContext pour modifier les en-têtes de réponse

  
L'objet `RouteContext` vous fournit les attributs et méthodes nécessaires pour manipuler les données de réponse avant qu'elles ne soient renvoyées au client. Grâce à l'objet RouteContext, vous pouvez facilement modifier les en-têtes, le statut ou les données de cookie dans la réponse renvoyée pour une requête spécifique.

  
Par exemple, ajoutons des informations `header` supplémentaires dans un nouvel endpoint, comme illustré ci-dessous.

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
    

Utiliser `RouteContext` dans les schémas
----------------------

  
Pendant la validation du schéma, des situations peuvent survenir où vous devez accéder à l'objet request. Django Ninja Extra facilite cela en fournissant un moyen de résoudre l'objet `RouteContext` pendant la requête, qui peut ensuite être utilisé pour accéder à l'objet request et à tout autre attribut nécessaire. Cela permet d'utiliser le contexte de la requête pendant le processus de validation, le rendant plus flexible et puissant.

Par exemple :

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
    

  
Dans l'exemple ci-dessus, nous avons utilisé `service_resolver`, une fonction utilitaire d'injection de dépendances, pour résoudre l'objet `RouteContext`. Cela nous permet d'accéder à l'objet request, que nous utilisons pour construire l'URL complète des détails du magasin. En utilisant `service_resolver` pour accéder au contexte de route, nous pouvons facilement accéder à l'objet request et l'utiliser pour recueillir toute information nécessaire pendant le processus de validation.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
