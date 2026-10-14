**Model Controller**
=======================

  
Model controller एक Django ORM model के लिए controller के भीतर CRUD (Create, Read, Update, Delete) operations को निर्दिष्ट configuration के आधार पर dynamically generate करता है।

  
Model controller `ControllerBase` class को extend करता है और दो configuration variables पेश करता है, अर्थात `model_config` और `model_service`।

*     
    `model_config` route और schema generation से संबंधित configuration को परिभाषित करने के लिए जिम्मेदार है।
*     
    `model_service` उस class को संदर्भित करता है जिसका उपयोग निर्दिष्ट model के लिए CRUD (Create, Read, Update, Delete) operations manage करने के लिए किया जाता है।

  
उदाहरण के लिए, Django में परिभाषित एक `Event` model पर विचार करें:

    from django.db import models
    
    class Category(models.Model):
        title = models.CharField(max_length=100)
    
    class Event(models.Model):
        title = models.CharField(max_length=100)
        category = models.OneToOneField(
            Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='events'
        )
        start_date = models.DateField()
        end_date = models.DateField()
    
        def __str__(self):
            return self.title
    

  
अब, चलिए `Event` model के लिए एक `ModelController` बनाते हैं। `api.py` फ़ाइल में, हम एक `EventModelController` परिभाषित करते हैं:

    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
        NinjaExtraAPI
    )
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
        
    api = NinjaExtraAPI()
    api.register_controllers(EventModelController)
    

  
ध्यान दें कि model controller automatic schema generation के लिए `ninja-schema` package पर निर्भर करता है। Package को install करने के लिए, निम्नलिखित command का उपयोग करें:

    pip install ninja-schema
    

  
Installation के बाद, आप http://localhost:8000/api/docs पर जाकर automatically generated API documentation तक पहुँच सकते हैं।

  
यह document `Event` model के लिए `EventModelController` द्वारा exposed routes, schemas, और features का एक विस्तृत अवलोकन प्रदान करता है।

**Model Configuration**
-----------------------

  
`ModelConfig` एक Pydantic schema है जिसका उपयोग model controller के व्यवहार को validate और configure करने के लिए किया जाता है। मुख्य configuration options में शामिल हैं:

*     
    Model: एक आवश्यक field जो Model Controller से जुड़े Django model type का प्रतिनिधित्व करता है।
*     
    async_routes: दर्शाता है कि controller routes को `asynchronous` route functions के रूप में बनाया जाना चाहिए या नहीं।
*     
    allowed_routes: Model Controller में generate किए जाने वाले अनुमत API operations निर्दिष्ट करने वाली एक list। डिफ़ॉल्ट मान `["create", "find_one", "update", "patch", "delete", "list"]` है।
*     
    create_schema: एक वैकल्पिक Pydantic schema जो model controller में `create` या `POST` operation के लिए data input type का रूपरेखा देता है। डिफ़ॉल्ट मान `None` है। यदि प्रदान नहीं किया गया है, तो `ModelController` `schema_config` option के आधार पर एक नया schema generate करेगा।
*     
    update_schema: एक वैकल्पिक Pydantic schema जो model controller में `update` या `PUT` operation के लिए data input type का विवरण देता है। डिफ़ॉल्ट मान `None` है। यदि प्रदान नहीं किया गया है, तो `create_schema` का उपयोग किया जाएगा (यदि उपलब्ध हो), अन्यथा `schema_config` option के आधार पर एक नया schema generate किया जाएगा।
*     
    retrieve_schema: एक वैकल्पिक Pydantic schema output जो विभिन्न operations के लिए data output type परिभाषित करता है। डिफ़ॉल्ट मान `None` है। यदि प्रदान नहीं किया गया है, तो `ModelController` `schema_config` option के आधार पर एक schema generate करेगा।
*     
    patch_schema: एक वैकल्पिक Pydantic schema output जो `patch/PATCH` operation के लिए input data type निर्दिष्ट करता है। डिफ़ॉल्ट मान `None` है। यदि प्रदान नहीं किया गया है, तो `ModelController` सभी fields को optional के रूप में रखते हुए एक schema generate करेगा।
*     
    schema_config: एक अन्य आवश्यक field जो Model Controller operations के लिए आवश्यक schema generation method का वर्णन करता है। Configuration options में शामिल हैं:
    *     
        `include`: शामिल करने के लिए fields की एक list। डिफ़ॉल्ट `__all__` है।
        
    *     
        `exclude`: बाहर रखने के लिए fields की एक list। डिफ़ॉल्ट मान `[]` है।
        
    *     
        `optional`: fields की एक list जिन्हें बलपूर्वक optional किया जाना है। डिफ़ॉल्ट मान `[pk]` है।
        
    *     
        `depth`: nested schemas generate करने की गहराई।
        
    *     
        `read_only_fields`: create, update, और patch operations के लिए input schemas generate करते समय बाहर रखने के लिए fields की एक list।
        
    *     
        `write_only_fields`: find_one और list operations के लिए output schemas generate करते समय बाहर रखने के लिए fields की एक list।
        
    *     
        pagination: model `list/GET` operation के लिए एक आवश्यकता जो एक request में एक साथ `100_000` items भेजने से रोकती है। Pagination configuration के लिए एक `ModelPagination` Pydantic schema object सेट करने की आवश्यकता होती है। Options में शामिल हैं:
        
        *     
            `klass`: `PaginationBase` type की एक pagination class। डिफ़ॉल्ट मान `PageNumberPaginationExtra` है।
        *     
            `paginator_kwargs`: `PaginationBase` initialization के लिए Dictionary values। डिफ़ॉल्ट मान None है।
        *     
            `pagination_schema`: एक Pydantic generic schema जो `list/GET` operation के लिए response schema generate करने के लिए `retrieve_schema` के साथ combine होता है।
        
          
        उदाहरण के लिए, यदि `LimitOffsetPagination` जैसी एक `ninja` pagination चुनी जाती है:
        
            from ninja.pagination import LimitOffsetPagination
            from ninja_extra.schemas import NinjaPaginationResponseSchema
            from ninja_extra import (
                ModelConfig,
                ModelControllerBase,
                api_controller,
                ModelPagination
            )
            
            @api_controller("/events")
            class EventModelController(ModelControllerBase):
                model_config = ModelConfig(
                    model=Event,
                    pagination=ModelPagination(
                        klass=LimitOffsetPagination, 
                        pagination_schema=NinjaPaginationResponseSchema
                    ),
                )
            
        

**  
Model Controller Operations के बारे में अधिक**
------------------

  
NinjaExtra model controllers में, controller के व्यवहार को `model_config` option में `allowed_routes` list की सामग्री के माध्यम से नियंत्रित किया जा सकता है।

  
उदाहरण के लिए, आप इस तरह एक read-only controller बना सकते हैं:

    from ninja_extra import api_controller, ModelControllerBase, ModelConfig, ModelSchemaConfig
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            allowed_routes=['find_one', 'list'],
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    

  
यह केवल listing के लिए `GET/{id}` और `GET/` routes बनाएगा।

  
आप किसी मौजूदा `EventModelController` में अधिक endpoints भी जोड़ सकते हैं। उदाहरण के लिए:

    from ninja_extra import api_controller, http_get, ModelControllerBase, ModelConfig, ModelSchemaConfig
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            allowed_routes=['find_one', 'list'],
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    
        @http_get('/subtract',)
        def subtract(self, a: int, b: int):
            """Subtracts a from b"""
            return {"result": a - b}
    

**Model Service**
-----------------

  
प्रत्येक model controller runtime पर model और controller के बीच बातचीत को manage करने के लिए एक `ModelService` instance बनाता है। आमतौर पर, ये model service operations model controller का हिस्सा होते, लेकिन उन्हें एक अधिक dynamic approach की अनुमति देने के लिए एक service में abstract किया गया है।

    class ModelService(ModelServiceBase):
        """
        Model Service for Model Controller model CRUD operations with simple logic for simple models.
    
        It's advised to override this class if you have a complex model.
        """
        def __init__(self, model: Type[DjangoModel]) -> None:
            self.model = model
    
        # ... (other CRUD methods)
    

  
इन operations को model controller पर वर्तमान operation या model controller द्वारा process की जा रही request के आधार पर call किया जाता है।

### **Custom Model Service का उपयोग करना**

  
Model controller में `ModelService` को override करना route operations को override करने से अधिक महत्वपूर्ण है। Model controllers में उपयोग की जाने वाली डिफ़ॉल्ट `ModelService` simple Django models के लिए डिज़ाइन की गई है। यदि model जटिल है, तो `ModelService` को override करने की सलाह दी जाती है।

  
उदाहरण के लिए, यदि आप बदलना चाहते हैं कि `Event` model कैसे saved होता है:

    from ninja_extra import ModelService
    
    class EventModelService(ModelService):
        def create(self, schema: PydanticModel, **kwargs: Any) -> Any:
            data = schema.dict(by_alias=True)
            data.update(kwargs)
            
            instance = self.model._default_manager.create(**data)
            return instance
    
            
    

  
फिर `api.py` में

    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
    )
    from .service import EventModelService
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        service = EventModelService(model=Event)
        model_config = ModelConfig(
            model=Event,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    

### **Async Routes सक्षम करें**

  
`model_config` में, `async_routes` को `True` सेट करें

    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
    )
    from .service import EventModelService
    from .models import Event
    
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        service = EventModelService(model=Event)
        model_config = ModelConfig(
            model=Event,
            async_routes=True,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    

  
`model_config` में `async_routes` parameter को `True` सेट करके, `ModelController` configuration के आधार पर async या sync endpoints generate करने के लिए `ModelAsyncEndpointFactory` और `ModelEndpointFactory` के बीच dynamically switch करता है।

### **Model Controller और Model Service एक साथ**

  
यदि आवश्यक हो, तो controller और model service को एक साथ merge भी किया जा सकता है:

  
उदाहरण के लिए, हाल ही में बनाए गए `EventModelService` का उपयोग करते हुए

    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
    )
    from .service import EventModelService
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase, EventModelService):
        model_config = ModelConfig(
            model=Event,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
        
        def __init__(self):
            EventModelService.__init__(self, model=Event)
            self.service = self  # This will expose the functions to the service attribute
    

**Model Endpoint Factory**
-----------

  
`ModelEndpointFactory` एक factory class है जिसका उपयोग model controller द्वारा endpoints को seamlessly generate करने के लिए किया जाता है। इसे किसी भी NinjaExtra controller में उसी उद्देश्य के लिए सीधे भी उपयोग किया जा सकता है।

  
उदाहरण के लिए, यदि हम एक नई `Category` में एक `Event` जोड़ना चाहते हैं, तो इसे इस प्रकार किया जा सकता है:

    from typing import Any
    from pydantic import BaseModel
    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
        ModelEndpointFactory
    )
    from .models import Event, Category
    
    class CreateCategorySchema(BaseModel):
        title: str
    
    class CategorySchema(BaseModel):
        id: str
        title: str
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    
        add_event_to_new_category = ModelEndpointFactory.create(
            path="/{int:event_id}/new-category",
            schema_in=CreateCategorySchema,
            schema_out=CategorySchema,
            custom_handler=lambda self, data, **kw: self.handle_add_event_to_new_category(data, **kw)
        )
    
        def handle_add_event_to_new_category(self, data: CreateCategorySchema, **kw: Any) -> Category:
            event = self.service.get_one(pk=kw['event_id'])
            category = Category.objects.create(title=data.title)
            event.category = category
            event.save()
            return category
    

  
ऊपर दिए गए उदाहरण में, हमने एक endpoint `POST /{int:event_id}/new-category` बनाने के लिए `ModelEndpointFactory.create` का उपयोग किया, input और output schemas के साथ एक custom handler पास किया। `custom_handler` पास करके, generated route function अपने handling operation को `service.create` को call करने के बजाय प्रदान किए गए `custom_handler` को delegate करता है।

**  
Async Model Endpoint Factory**
---------------

  
`ModelAsyncEndpointFactory` का API interface `ModelEndpointFactory` के समान है, लेकिन यह विशेष रूप से async endpoints generate करने के लिए डिज़ाइन किया गया है।

  
हम `ModelEndpointFactory` की तरह वही उदाहरण बना सकते हैं

उदाहरण के लिए:

    from typing import Any
    from pydantic import BaseModel
    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
        ModelAsyncEndpointFactory
    )
    from .models import Event, Category
    
    class CreateCategorySchema(BaseModel):
        title: str
    
    class CategorySchema(BaseModel):
        id: str
        title: str
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    
        add_event_to_new_category = ModelAsyncEndpointFactory.create(
            path="/{int:event_id}/new-category",
            schema_in=CreateCategorySchema,
            schema_out=CategorySchema,
            custom_handler=lambda self, data, **kw: self.handle_add_event_to_new_category(data, **kw)
        )
    
        async def handle_add_event_to_new_category(self, data: CreateCategorySchema, **kw: Any) -> Category:
            event = await self.service.get_one_async(pk=kw['event_id'])
            category = Category.objects.create(title=data.title)
            event.category = category
            event.save()
            return category
    

  
ऊपर दी गई illustration में, हमने `add_event_to_new_category` को एक async function के रूप में बनाया और `handle_add_event_to_new_category` को भी एक async function में बदल दिया।

**QueryGetter और ObjectGetter**
--------------------------------

  
`ModelEndpointFactory` एक model object या queryset filter प्राप्त करने का एक अधिक लचीला तरीका expose करता है, क्रमशः `ModelEndpointFactory.find_one` और `ModelEndpointFactory.list` के मामले में।

  
उदाहरण के लिए, एक event की category प्राप्त करना (व्यावहारिक नहीं, लेकिन illustration के लिए):

    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
        ModelEndpointFactory
    )
    from .models import Event, Category
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    
        get_event_category = ModelEndpointFactory.find_one(
            path="/{int:event_id}/category",
            schema_out=CategorySchema,
            lookup_param='event_id',
            object_getter=lambda self, pk, **kw: self.service.get_one(pk=pk).category
        )
    

  
ऊपर दिए गए उदाहरण में, हमने एक `get_event_category` endpoint बनाने के लिए `ModelEndpointFactory.find_one` का उपयोग किया और `event_id` के आधार पर model प्राप्त करने के लिए एक callback के रूप में `object_getter` प्रदान किया। `lookup_param` `kwargs` में उस key को दर्शाता है जिसका उपयोग object model प्राप्त करने के लिए pk value परिभाषित करने के लिए किया जाता है, यदि कोई `object_getter` handler implement नहीं किया गया है।

  
दूसरी ओर, आप एक ऐसी स्थिति का सामना कर सकते हैं जहाँ आपको `category_id` द्वारा events की list चाहिए:

    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
        ModelEndpointFactory
    )
    from .models import Event, Category
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    
        get_events_by_category = ModelEndpointFactory.list(
            path="/category/{int:category_id}/",
            schema_out=model_config.retrieve_schema,
            lookup_param='category_id',
            queryset_getter=lambda self, **kw: Category.objects.filter(pk=kw['category_id']).first().events.all()
        )
    

  
`queryset_getter` के साथ `ModelEndpointFactory.list` का उपयोग करके, आप जल्दी से एक list endpoint सेट अप कर सकते हैं जो किसी category से संबंधित events return करता है। ध्यान दें कि यदि कोई invalid ID प्रदान की जाती है, तो हमारी `queryset_getter` विफल हो सकती है क्योंकि यह केवल एक उदाहरण है।

  
इसके अलावा, ध्यान रखें कि ModelConfig के instantiate होने के बाद, `model_config` जैसी settings का उपयोग अभी भी किया जा सकता है, जैसे `create_schema`, `retrieve_schema`, `patch_schema`, और `update_schema`।

**  
Path और Query Parameters**
--------------

  
`ModelEndpointFactory` में, `path` और `query` parameters की पहचान करने के लिए path parameters को parse किया जाता है। इन parameters को फिर Ninja input schema में fields के रूप में बनाया जाता है और request के दौरान parse किया जाता है, उन्हें kwargs के रूप में handler को पास करते हुए।

उदाहरण के लिए,

    list_post_tags = ModelEndpointFactory.list(
        path="/{int:id}/tags/{post_id}?query=int&query1=int",
        schema_out=model_config.retrieve_schema,
        queryset_getter=lambda self, **kw: self.list_post_tags_query(**kw)
    )
    
    def list_post_tags_query(self, **kwargs):
        assert kwargs['id']
        assert kwargs['query']
        assert kwargs['query1']
        post_id = kwargs['post_id']
        return Post.objects.filter(id=post_id).first().tags.all()
    

  
इस उदाहरण में, path `/{int:id}/tags/{post_id}?query=int&query1=int` दो path parameters `['id:int', 'post_id:str']` और दो query parameters `['query:int', 'query1:int']` generate करता है। इन parameters को Ninja input schema में pack किया जाता है और request के दौरान parse किया जाता है, उन्हें kwargs के रूप में route handler को पास करते हुए।

  
ध्यान दें कि जब `path` और `query` parameters परिभाषित किए जाते हैं, तो उन्हें ninja schema input में आवश्यक (required) fields के रूप में जोड़ा जाता है, optional के रूप में नहीं। इसके अलावा, path और query data types Django URL converters के साथ compatible होने चाहिए।

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
