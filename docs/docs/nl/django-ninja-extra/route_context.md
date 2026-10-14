  
Django Ninja Extra biedt het object RouteContext, dat beschikbaar is tijdens de gehele levenscyclus van het request. Dit object bevat belangrijke attributen voor de route-handler die het request zal verwerken. Deze attributen omvatten het Django `HttpRequest`-object, de lijst met machtigingsklassen voor de route-handler, het tijdelijke response-object dat Django-Ninja gebruikt om de uiteindelijke response op te bouwen, en de kwargs en args die nodig zijn om de routefunctie aan te roepen.

  
Merk op dat deze attributen niet aan het begin van het request worden ingesteld, maar beschikbaar komen naarmate het request verschillende fasen doorloopt, voordat de uitvoering van de routefunctie wordt bereikt.

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
    

Toegang krijgen tot `RouteContext`
--------------------

  
In Django Ninja Extra kan het object `RouteContext` worden benaderd in controllerklassen via het attribuut `self.context`. Dit attribuut is beschikbaar op instantieniveau van de controllerklasse, waardoor het gemakkelijk is om de attributen en methoden van het object `RouteContext` te benaderen.

Bijvoorbeeld.

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
    

  
In dit voorbeeld kunnen we het geauthenticeerde `user`-object benaderen via het attribuut `self.context` van het requestobject, dat beschikbaar is in de controllerklasse. Zo kunnen we eenvoudig de informatie van de geauthenticeerde gebruiker benaderen.

###   
RouteContext gebruiken om response-headers te wijzigen

  
Het object `RouteContext` biedt je de attributen en methoden die nodig zijn om de responsgegevens te manipuleren voordat deze aan de client wordt teruggegeven. Via het object RouteContext kun je eenvoudig de headers, status of cookie-gegevens in de response wijzigen die voor een specifiek request wordt teruggegeven.

  
Laten we bijvoorbeeld extra `header`-informatie toevoegen in een nieuw endpoint, zoals hieronder getoond.

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
    

`RouteContext` gebruiken in schema's
----------------------

  
Tijdens schemavalidatie kunnen situaties ontstaan waarin je het requestobject moet benaderen. Django Ninja Extra maakt dit eenvoudig door een manier te bieden om het object `RouteContext` tijdens het request op te lossen, waarna het kan worden gebruikt om het requestobject en eventuele andere noodzakelijke attributen te benaderen. Zo kan de context van het request worden gebruikt tijdens het validatieproces, wat het flexibeler en krachtiger maakt.

Bijvoorbeeld:

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
    

  
In het bovenstaande voorbeeld hebben we `service_resolver` gebruikt, een hulpfunctie voor dependency injection, om het object `RouteContext` op te lossen. Zo kunnen we het requestobject benaderen, dat we gebruiken om de volledige URL voor de winkeldetails op te bouwen. Door `service_resolver` te gebruiken om de routecontext te benaderen, kunnen we gemakkelijk het requestobject benaderen en het gebruiken om tijdens het validatieproces alle nodige informatie te verzamelen.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
