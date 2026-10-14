**Modelcontroller**
=======================

  
De modelcontroller genereert dynamisch CRUD-bewerkingen (Create, Read, Update, Delete) voor een Django ORM-model binnen een controller, op basis van de opgegeven configuratie.

  
De modelcontroller breidt de klasse `ControllerBase` uit en introduceert twee configuratievariabelen, namelijk `model_config` en `model_service`.

*     
    `model_config` is verantwoordelijk voor het definiëren van de configuratie met betrekking tot route- en schemageneratie.
*     
    `model_service` verwijst naar de klasse die wordt gebruikt om de CRUD-bewerkingen (Create, Read, Update, Delete) voor het opgegeven model te beheren.

  
Overweeg bijvoorbeeld een model `Event` dat in Django is gedefinieerd:

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
    

  
Laten we nu een `ModelController` maken voor het model `Event`. In het bestand `api.py` definiëren we een `EventModelController`:

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
    

  
Merk op dat de modelcontroller afhankelijk is van het pakket `ninja-schema` voor automatische schemageneratie. Gebruik het volgende commando om het pakket te installeren:

    pip install ninja-schema
    

  
Na installatie kun je de automatisch gegenereerde API-documentatie bekijken via http://localhost:8000/api/docs.

  
Dit document geeft een gedetailleerd overzicht van de routes, schema's en functies die de `EventModelController` blootlegt voor het model `Event`.

**Modelconfiguratie**
-----------------------

  
`ModelConfig` is een Pydantic-schema dat wordt gebruikt om het gedrag van de modelcontroller te valideren en te configureren. Belangrijke configuratieopties zijn onder andere:

*     
    Model: een verplicht veld dat het Django-modeltype vertegenwoordigt dat aan de Model Controller is gekoppeld.
*     
    async_routes: geeft aan of de controllerroutes moeten worden aangemaakt als `asynchrone` routefuncties.
*     
    allowed_routes: een lijst die de toegestane API-operaties specificeert die in de Model Controller moeten worden gegenereerd. De standaardwaarde is `["create", "find_one", "update", "patch", "delete", "list"]`.
*     
    create_schema: een optioneel Pydantic-schema dat het invoergegevenstype schetst voor de operatie `create` of `POST` in de modelcontroller. Standaardwaarde is `None`. Als het niet wordt opgegeven, genereert de `ModelController` een nieuw schema op basis van de optie `schema_config`.
*     
    update_schema: een optioneel Pydantic-schema dat het invoergegevenstype beschrijft voor de operatie `update` of `PUT` in de modelcontroller. Standaardwaarde is `None`. Als het niet wordt opgegeven, wordt `create_schema` gebruikt indien beschikbaar, anders wordt een nieuw schema gegenereerd op basis van de optie `schema_config`.
*     
    retrieve_schema: een optionele Pydantic-schema-uitvoer die het uitvoergegevenstype definieert voor verschillende operaties. Standaardwaarde is `None`. Als het niet wordt opgegeven, genereert de `ModelController` een schema op basis van de optie `schema_config`.
*     
    patch_schema: een optionele Pydantic-schema-uitvoer die het invoergegevenstype specificeert voor de operatie `patch/PATCH`. Standaardwaarde is `None`. Als het niet wordt opgegeven, genereert de `ModelController` een schema met alle velden optioneel.
*     
    schema_config: nog een verplicht veld dat de schemageneratiemethode beschrijft die vereist is voor de operaties van de Model Controller. Configuratieopties zijn onder andere:
    *     
        `include`: een lijst met op te nemen velden. Standaard is `__all__`.
        
    *     
        `exclude`: een lijst met uit te sluiten velden. Standaardwaarde is `[]`.
        
    *     
        `optional`: een lijst met velden die als optioneel worden afgedwongen. Standaardwaarde is `[pk]`.
        
    *     
        `depth`: de diepte voor het genereren van geneste schema's.
        
    *     
        `read_only_fields`: een lijst met velden die worden uitgesloten bij het genereren van invoerschema's voor de operaties create, update en patch.
        
    *     
        `write_only_fields`: een lijst met velden die worden uitgesloten bij het genereren van uitvoerschema's voor de operaties find_one en list.
        
    *     
        pagination: een vereiste voor de modeloperatie `list/GET` om te voorkomen dat er in één request `100_000` items tegelijk worden verstuurd. De pagineringsconfiguratie vereist het instellen van een Pydantic-schemaobject `ModelPagination`. Opties zijn onder andere:
        
        *     
            `klass`: een pagineringsklasse van het type `PaginationBase`. Standaardwaarde is `PageNumberPaginationExtra`.
        *     
            `paginator_kwargs`: woordenboekwaarden voor de initialisatie van `PaginationBase`. Standaardwaarde is None.
        *     
            `pagination_schema`: een Pydantic generiek schema dat wordt gecombineerd met `retrieve_schema` om het responschema te genereren voor de operatie `list/GET`.
        
          
        Kies je bijvoorbeeld een `ninja`-paginering zoals `LimitOffsetPagination`:
        
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
Meer over modelcontrolleroperaties**
------------------

  
In NinjaExtra-modelcontrollers kan het gedrag van de controller worden gestuurd via de inhoud van de lijst `allowed_routes` in de optie `model_config`.

  
Je kunt bijvoorbeeld een alleen-lezen controller maken zoals dit:

    from ninja_extra import api_controller, ModelControllerBase, ModelConfig, ModelSchemaConfig
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            allowed_routes=['find_one', 'list'],
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    

  
Dit maakt alleen de routes `GET/{id}` en `GET/` voor het weergeven van lijsten aan.

  
Je kunt ook meer endpoints toevoegen aan een bestaande `EventModelController`. Bijvoorbeeld:

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
    

**Modelservice**
-----------------

  
Elke modelcontroller maakt tijdens de uitvoering een `ModelService`-instantie aan om de interactie tussen het model en de controller te beheren. Normaal gesproken zouden deze modelservice-operaties deel hebben uitgemaakt van de modelcontroller, maar ze zijn geabstraheerd naar een service om een meer dynamische aanpak mogelijk te maken.

    class ModelService(ModelServiceBase):
        """
        Model Service for Model Controller model CRUD operations with simple logic for simple models.
    
        It's advised to override this class if you have a complex model.
        """
        def __init__(self, model: Type[DjangoModel]) -> None:
            self.model = model
    
        # ... (other CRUD methods)
    

  
Deze operaties worden aangeroepen op basis van de huidige operatie op de modelcontroller of het request dat de modelcontroller verwerkt.

### **Een aangepaste modelservice gebruiken**

  
Het overschrijven van de `ModelService` in een modelcontroller is belangrijker dan het overschrijven van route-operaties. De standaard `ModelService` die in modelcontrollers wordt gebruikt, is ontworpen voor eenvoudige Django-modellen. Als het model complex is, wordt aanbevolen de `ModelService` te overschrijven.

  
Als je bijvoorbeeld wilt veranderen hoe het model `Event` wordt opgeslagen:

    from ninja_extra import ModelService
    
    class EventModelService(ModelService):
        def create(self, schema: PydanticModel, **kwargs: Any) -> Any:
            data = schema.dict(by_alias=True)
            data.update(kwargs)
            
            instance = self.model._default_manager.create(**data)
            return instance
    
            
    

Dan in `api.py`

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
    

### **Asynchrone routes inschakelen**

  
Stel in `model_config` `async_routes` in op `True`

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
    

  
Door de parameter `async_routes` in `model_config` op `True` te zetten, schakelt de `ModelController` dynamisch tussen `ModelAsyncEndpointFactory` en `ModelEndpointFactory` op basis van de configuratie om async- of sync-endpoints te genereren.

### **Modelcontroller en modelservice samen**

  
Indien nodig kunnen de controller en de modelservice ook worden samengevoegd:

  
Bijvoorbeeld met de `EventModelService` die we hebben gemaakt

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

  
`ModelEndpointFactory` is een factory-klasse die door de modelcontroller wordt gebruikt om naadloos endpoints te genereren. Hij kan ook rechtstreeks in elke NinjaExtra-controller voor hetzelfde doel worden gebruikt.

  
Als we bijvoorbeeld een `Event` willen toevoegen aan een nieuwe `Category`, kan dat als volgt:

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
    

  
In het bovenstaande voorbeeld hebben we `ModelEndpointFactory.create` gebruikt om een endpoint `POST /{int:event_id}/new-category` te maken, waarbij de invoer- en uitvoerschema's samen met een aangepaste handler worden doorgegeven. Door `custom_handler` door te geven, delegeert de gegenereerde routefunctie zijn afhandelingsoperatie aan de opgegeven `custom_handler` in plaats van `service.create` aan te roepen.

**  
Async Model Endpoint Factory**
---------------

  
`ModelAsyncEndpointFactory` heeft dezelfde API-interface als `ModelEndpointFactory`, maar is specifiek ontworpen om async-endpoints te genereren.

  
We kunnen hetzelfde voorbeeld maken als met `ModelEndpointFactory`

Bijvoorbeeld:

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
    

  
In de illustratie hierboven hebben we `add_event_to_new_category` als async-functie aangemaakt en ook `handle_add_event_to_new_category` omgezet naar een async-functie.

**QueryGetter en ObjectGetter**
--------------------------------

  
`ModelEndpointFactory` legt een flexibelere manier bloot om een modelobject of een queryset-filter te verkrijgen, in het geval van respectievelijk `ModelEndpointFactory.find_one` en `ModelEndpointFactory.list`.

  
Bijvoorbeeld, het ophalen van de categorie van een event (niet praktisch, maar ter illustratie):

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
    

  
In het bovenstaande voorbeeld hebben we `ModelEndpointFactory.find_one` gebruikt om een endpoint `get_event_category` te maken en een `object_getter` als callback opgegeven om het model op te halen op basis van `event_id`. De `lookup_param` geeft de sleutel in `kwargs` aan die wordt gebruikt om de pk-waarde te definiëren voor het ophalen van het objectmodel, als er geen `object_getter`-handler is geïmplementeerd.

  
Aan de andere kant kun je in een situatie komen waarin je events op `category_id` wilt weergeven:

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
    

  
Door `ModelEndpointFactory.list` te gebruiken met `queryset_getter`, kun je snel een list-endpoint opzetten dat de events teruggeeft die bij een categorie horen. Merk op dat onze `queryset_getter` kan mislukken als een ongeldige ID wordt opgegeven, aangezien dit slechts een voorbeeld is.

  
Houd er bovendien rekening mee dat na de instantiatie van de ModelConfig instellingen zoals `model_config` nog steeds kunnen worden gebruikt, zoals `create_schema`, `retrieve_schema`, `patch_schema` en `update_schema`.

**  
Pad- en queryparameters**
--------------

  
In `ModelEndpointFactory` worden padparameters geparseerd om `path`- en `query`-parameters te identificeren. Deze parameters worden vervolgens aangemaakt als velden in het Ninja-invoerschema en geparseerd tijdens het request, waarbij ze als kwargs aan de handler worden doorgegeven.

Bijvoorbeeld,

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
    

  
In dit voorbeeld genereert het pad `/{int:id}/tags/{post_id}?query=int&query1=int` twee padparameters `['id:int', 'post_id:str']` en twee queryparameters `['query:int', 'query1:int']`. Deze parameters worden verpakt in het Ninja-invoerschema en geparseerd tijdens het request, waarbij ze als kwargs aan de route-handler worden doorgegeven.

  
Merk op dat wanneer `path`- en `query`-parameters zijn gedefinieerd, ze als verplichte velden aan de ninja-schema-invoer worden toegevoegd, niet als optioneel. Daarnaast moeten de gegevenstypen van pad en query compatibel zijn met de Django URL-converters.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
