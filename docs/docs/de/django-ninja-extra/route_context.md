  
Django Ninja Extra stellt das Objekt RouteContext bereit, das während des gesamten Lebenszyklus einer Anfrage verfügbar ist. Dieses Objekt enthält wichtige Attribute für den Route-Handler, der die Anfrage verarbeitet. Zu diesen Attributen gehören das Django-`HttpRequest`-Objekt, die Liste der Berechtigungsklassen für den Route-Handler, das temporäre Response-Objekt, das Django-Ninja zum Erstellen der endgültigen Antwort verwendet, sowie die kwargs und args, die für den Aufruf der Routen-Funktion benötigt werden.

  
Beachten Sie, dass diese Attribute nicht zu Beginn der Anfrage gesetzt werden, sondern im Verlauf der Anfrage in verschiedenen Phasen verfügbar werden, bevor die Ausführung der Routen-Funktion erreicht ist.

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
    

Zugriff auf `RouteContext`
--------------------

  
In Django Ninja Extra kann auf das Objekt `RouteContext` in Controller-Klassen über das Attribut `self.context` zugegriffen werden. Dieses Attribut ist auf Instanzebene der Controller-Klasse verfügbar, was den Zugriff auf die Attribute und Methoden des `RouteContext`-Objekts erleichtert.

Zum Beispiel.

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
    

  
In diesem Beispiel können wir auf das authentifizierte `user`-Objekt über das Attribut `self.context` des request-Objekts zugreifen, das in der Controller-Klasse verfügbar ist. Dies ermöglicht es uns, einfach auf die Informationen des authentifizierten Benutzers zuzugreifen.

###   
Verwendung von RouteContext zum Ändern von Response-Headern

  
Das Objekt `RouteContext` stellt Ihnen die Attribute und Methoden zur Verfügung, die benötigt werden, um die Response-Daten zu manipulieren, bevor sie an den Client zurückgegeben werden. Über das RouteContext-Objekt können Sie die Header, den Status oder die Cookie-Daten in der Antwort auf eine bestimmte Anfrage mühelos ändern.

  
Fügen wir zum Beispiel in einem neuen Endpunkt zusätzliche `header`-Informationen hinzu, wie unten gezeigt.

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
    

Verwendung von `RouteContext` in Schemas
----------------------

  
Während der Schemavalidierung kann es Situationen geben, in denen Sie auf das request-Objekt zugreifen müssen. Django Ninja Extra erleichtert dies, indem es eine Möglichkeit bietet, das `RouteContext`-Objekt während der Anfrage aufzulösen, das dann verwendet werden kann, um auf das request-Objekt und alle anderen benötigten Attribute zuzugreifen. Dies erlaubt es, den Kontext der Anfrage während des Validierungsprozesses zu verwenden, was diesen flexibler und leistungsfähiger macht.

Zum Beispiel:

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
    

  
Im obigen Beispiel haben wir `service_resolver` verwendet, eine Hilfsfunktion für Dependency Injection, um das `RouteContext`-Objekt aufzulösen. Dies erlaubt es uns, auf das request-Objekt zuzugreifen, mit dem wir die vollständige URL für die Store-Details erstellen. Durch den Zugriff auf den Route-Kontext über `service_resolver` können wir leicht auf das request-Objekt zugreifen und es verwenden, um während des Validierungsprozesses alle benötigten Informationen zusammenzutragen.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
