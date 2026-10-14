  
Django Ninja Extra RouteContext object प्रदान करता है, जो request lifecycle के दौरान उपलब्ध रहता है। यह object उस route handler के लिए महत्वपूर्ण attributes रखता है जो request को process करेगा। इन attributes में Django का `HttpRequest` object, route handler के लिए permission classes की list, वह अस्थायी response object जिसका उपयोग Django-Ninja अंतिम response बनाने के लिए करता है, और route function को call करने के लिए आवश्यक kwargs और args शामिल हैं।

  
ध्यान दें कि ये attributes request की शुरुआत में सेट नहीं होते, बल्कि request के विभिन्न चरणों से गुजरने के दौरान, route function execution तक पहुँचने से पहले उपलब्ध हो जाते हैं।

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
    

`RouteContext` तक कैसे पहुँचें
--------------------

  
Django Ninja Extra में, `RouteContext` object को controller classes में `self.context` attribute का उपयोग करके access किया जा सकता है। यह attribute controller class के instance level पर उपलब्ध है, जिससे `RouteContext` object के attributes और methods तक पहुँचना आसान हो जाता है।

उदाहरण के लिए।

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
    

  
इस उदाहरण में, हम controller class में उपलब्ध request object के `self.context` attribute से authenticated `user` object तक पहुँच सकते हैं। इससे हम authenticated user की जानकारी तक आसानी से पहुँच सकते हैं।

###   
RouteContext का उपयोग करके Response Headers को संशोधित करना

  
`RouteContext` object आपको वे attributes और methods प्रदान करता है जिनकी आवश्यकता response data को client को return किए जाने से पहले manipulate करने के लिए होती है। RouteContext object के माध्यम से, आप किसी specific request के लिए return किए गए response में headers, status, या cookie data को आसानी से संशोधित कर सकते हैं।

  
उदाहरण के लिए, चलिए एक नए endpoint में अतिरिक्त `header` जानकारी जोड़ते हैं, जैसा कि नीचे दिखाया गया है।

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
    

Schemas में `RouteContext` का उपयोग करना
----------------------

  
Schema validation के दौरान, ऐसी स्थितियाँ उत्पन्न हो सकती हैं जब आपको request object तक पहुँचने की आवश्यकता होती है। Django Ninja Extra इसे आसान बनाता है कि request के दौरान `RouteContext` object को resolve करने का एक तरीका प्रदान करके, जिसका उपयोग फिर request object और किसी अन्य आवश्यक attributes तक पहुँचने के लिए किया जा सकता है। इससे request के context को validation process के दौरान उपयोग किया जा सकता है, जिससे यह अधिक लचीला और शक्तिशाली बन जाता है।

उदाहरण के लिए:

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
    

  
ऊपर दिए गए उदाहरण में, हमने `service_resolver` का उपयोग किया, जो एक dependency injection utility function है, `RouteContext` object को resolve करने के लिए। इससे हम request object तक पहुँच सकते हैं, जिसका उपयोग हम store details के लिए पूर्ण URL बनाने के लिए करते हैं। Route context तक `service_resolver` द्वारा पहुँचकर, हम request object तक आसानी से पहुँच सकते हैं और validation process के दौरान किसी भी आवश्यक जानकारी को एकत्र करने के लिए इसका उपयोग कर सकते हैं।

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
