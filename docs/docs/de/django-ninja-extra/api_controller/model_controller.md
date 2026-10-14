**Model Controller**
=======================

  
Der Model Controller erzeugt dynamisch CRUD-Operationen (Create, Read, Update, Delete) für ein Django-ORM-Modell innerhalb eines Controllers, basierend auf der angegebenen Konfiguration.

  
Der Model Controller erweitert die Klasse `ControllerBase` und führt zwei Konfigurationsvariablen ein, nämlich `model_config` und `model_service`.

*     
    `model_config` ist für die Definition der Konfiguration im Zusammenhang mit Route- und Schema-Generierung zuständig.
*     
    `model_service` bezeichnet die Klasse, die zur Verwaltung der CRUD-Operationen (Create, Read, Update, Delete) für das angegebene Modell verwendet wird.

  
Betrachten wir zum Beispiel ein in Django definiertes `Event`-Modell:

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
    

  
Erstellen wir nun einen `ModelController` für das `Event`-Modell. In der Datei `api.py` definieren wir einen `EventModelController`:

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
    

  
Beachten Sie, dass der Model Controller für die automatische Schema-Generierung auf das Paket `ninja-schema` angewiesen ist. Verwenden Sie den folgenden Befehl, um das Paket zu installieren:

    pip install ninja-schema
    

  
Nach der Installation können Sie auf die automatisch generierte API-Dokumentation zugreifen, indem Sie http://localhost:8000/api/docs besuchen.

  
Dieses Dokument bietet einen detaillierten Überblick über die Routen, Schemas und Funktionen, die der `EventModelController` für das `Event`-Modell bereitstellt.

**Model-Konfiguration**
-----------------------

  
`ModelConfig` ist ein Pydantic-Schema, das zur Validierung und Konfiguration des Verhaltens des Model Controllers verwendet wird. Zu den wichtigsten Konfigurationsoptionen gehören:

*     
    Model: Ein Pflichtfeld, das den mit dem Model Controller verknüpften Django-Modelltyp darstellt.
*     
    async_routes: Gibt an, ob die Controller-Routen als `asynchrone` Routen-Funktionen erstellt werden sollen.
*     
    allowed_routes: Eine Liste, die die zulässigen API-Operationen angibt, die im Model Controller generiert werden sollen. Der Standardwert ist `["create", "find_one", "update", "patch", "delete", "list"]`.
*     
    create_schema: Ein optionales Pydantic-Schema, das den Dateneingabetyp für die Operation `create` bzw. `POST` im Model Controller beschreibt. Der Standardwert ist `None`. Wird es nicht angegeben, erzeugt der `ModelController` ein neues Schema basierend auf der Option `schema_config`.
*     
    update_schema: Ein optionales Pydantic-Schema, das den Dateneingabetyp für die Operation `update` bzw. `PUT` im Model Controller beschreibt. Der Standardwert ist `None`. Wird es nicht angegeben, wird das `create_schema` verwendet, falls vorhanden; andernfalls wird ein neues Schema basierend auf der Option `schema_config` generiert.
*     
    retrieve_schema: Ein optionales Pydantic-Schema als Ausgabe, das den Datenausgabetyp für verschiedene Operationen definiert. Der Standardwert ist `None`. Wird es nicht angegeben, erzeugt der `ModelController` ein Schema basierend auf der Option `schema_config`.
*     
    patch_schema: Ein optionales Pydantic-Schema als Ausgabe, das den Dateneingabetyp für die Operation `patch/PATCH` angibt. Der Standardwert ist `None`. Wird es nicht angegeben, erzeugt der `ModelController` ein Schema, in dem alle Felder optional sind.
*     
    schema_config: Ein weiteres Pflichtfeld, das die für die Model-Controller-Operationen erforderliche Methode der Schema-Generierung beschreibt. Zu den Konfigurationsoptionen gehören:
    *     
        `include`: Eine Liste der einzuschließenden Felder. Standard ist `__all__`.
        
    *     
        `exclude`: Eine Liste der auszuschließenden Felder. Der Standardwert ist `[]`.
        
    *     
        `optional`: Eine Liste der Felder, die zwangsweise als optional behandelt werden sollen. Der Standardwert ist `[pk]`.
        
    *     
        `depth`: Die Tiefe für die Generierung verschachtelter Schemas.
        
    *     
        `read_only_fields`: Eine Liste von Feldern, die beim Generieren von Eingabeschemata für create-, update- und patch-Operationen ausgeschlossen werden.
        
    *     
        `write_only_fields`: Eine Liste von Feldern, die beim Generieren von Ausgabeschemata für find_one- und list-Operationen ausgeschlossen werden.
        
    *     
        pagination: Eine Anforderung für die Operation `list/GET` des Modells, um zu verhindern, dass auf einmal `100_000` Elemente in einer Anfrage gesendet werden. Die Pagination-Konfiguration erfordert das Setzen eines Pydantic-Schemaobjekts `ModelPagination`. Zu den Optionen gehören:
        
        *     
            `klass`: Eine Pagination-Klasse vom Typ `PaginationBase`. Der Standardwert ist `PageNumberPaginationExtra`.
        *     
            `paginator_kwargs`: Wörterbuchwerte für die Initialisierung von `PaginationBase`. Der Standardwert ist None.
        *     
            `pagination_schema`: Ein generisches Pydantic-Schema, das mit `retrieve_schema` kombiniert wird, um das Response-Schema für die Operation `list/GET` zu erzeugen.
        
          
        Wenn Sie sich zum Beispiel für eine `ninja`-Pagination wie `LimitOffsetPagination` entscheiden:
        
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
Mehr zu den Model-Controller-Operationen**
------------------

  
In NinjaExtra-Model-Controllern kann das Verhalten des Controllers über die Inhalte der Liste `allowed_routes` in der Option `model_config` gesteuert werden.

  
Sie können zum Beispiel einen schreibgeschützten Controller wie folgt erstellen:

    from ninja_extra import api_controller, ModelControllerBase, ModelConfig, ModelSchemaConfig
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            allowed_routes=['find_one', 'list'],
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    

  
Damit werden nur die Routen `GET/{id}` und `GET/` zum Auflisten erstellt.

  
Sie können auch weitere Endpunkte zu einem bestehenden `EventModelController` hinzufügen. Zum Beispiel:

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

  
Jeder Model Controller erzeugt zur Laufzeit eine `ModelService`-Instanz, um die Interaktion zwischen dem Modell und dem Controller zu verwalten. Normalerweise wären diese Model-Service-Operationen Teil des Model Controllers gewesen, aber sie wurden in einen Service abstrahiert, um einen dynamischeren Ansatz zu ermöglichen.

    class ModelService(ModelServiceBase):
        """
        Model Service for Model Controller model CRUD operations with simple logic for simple models.
    
        It's advised to override this class if you have a complex model.
        """
        def __init__(self, model: Type[DjangoModel]) -> None:
            self.model = model
    
        # ... (other CRUD methods)
    

  
Diese Operationen werden auf der Grundlage der aktuellen Operation auf dem Model Controller bzw. der Anfrage, die der Model Controller verarbeitet, aufgerufen.

### **Verwendung eines benutzerdefinierten Model Service**

  
Das Überschreiben des `ModelService` in einem Model Controller ist wichtiger als das Überschreiben der Routen-Operationen. Der in Model Controllern verwendete Standard-`ModelService` ist für einfache Django-Modelle ausgelegt. Wenn das Modell komplex ist, wird das Überschreiben des `ModelService` empfohlen.

  
Wenn Sie zum Beispiel ändern möchten, wie das `Event`-Modell gespeichert wird:

    from ninja_extra import ModelService
    
    class EventModelService(ModelService):
        def create(self, schema: PydanticModel, **kwargs: Any) -> Any:
            data = schema.dict(by_alias=True)
            data.update(kwargs)
            
            instance = self.model._default_manager.create(**data)
            return instance
    
            
    

  
Und dann in `api.py`

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
    

### **Async-Routen aktivieren**

  
Setzen Sie in `model_config` `async_routes` auf `True`

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
    

  
Durch das Setzen des Parameters `async_routes` auf `True` in `model_config` wechselt der `ModelController` dynamisch zwischen `ModelAsyncEndpointFactory` und `ModelEndpointFactory`, um je nach Konfiguration asynchrone oder synchrone Endpunkte zu erzeugen.

### **Model Controller und Model Service zusammen**

  
Bei Bedarf können Controller und Model Service auch zusammengeführt werden:

  
Zum Beispiel unter Verwendung des von uns erstellten `EventModelService`

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

  
`ModelEndpointFactory` ist eine Factory-Klasse, die vom Model Controller verwendet wird, um Endpunkte nahtlos zu erzeugen. Sie kann für denselben Zweck auch direkt in einem beliebigen NinjaExtra-Controller verwendet werden.

  
Wenn wir zum Beispiel ein `Event` zu einer neuen `Category` hinzufügen möchten, kann dies wie folgt geschehen:

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
    

  
Im obigen Beispiel haben wir `ModelEndpointFactory.create` verwendet, um einen Endpunkt `POST /{int:event_id}/new-category` zu erzeugen, und dabei die Ein- und Ausgabeschemata sowie einen benutzerdefinierten Handler übergeben. Durch die Übergabe von `custom_handler` delegiert die erzeugte Routen-Funktion ihre Verarbeitung an den bereitgestellten `custom_handler`, statt `service.create` aufzurufen.

**  
Async Model Endpoint Factory**
---------------

  
`ModelAsyncEndpointFactory` hat dieselbe API-Schnittstelle wie `ModelEndpointFactory`, wurde aber speziell für die Erzeugung asynchroner Endpunkte entwickelt.

  
Wir können dasselbe Beispiel wie mit `ModelEndpointFactory` erstellen

Zum Beispiel:

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
    

  
In der obigen Darstellung haben wir `add_event_to_new_category` als asynchrone Funktion erstellt und außerdem `handle_add_event_to_new_category` in eine asynchrone Funktion umgewandelt.

**QueryGetter und ObjectGetter**
--------------------------------

  
`ModelEndpointFactory` bietet einen flexibleren Weg, um ein Modell-Objekt bzw. einen Queryset-Filter abzurufen — im Fall von `ModelEndpointFactory.find_one` bzw. `ModelEndpointFactory.list`.

  
Zum Beispiel das Abrufen der Kategorie eines Events (nicht praktikabel, aber zur Veranschaulichung):

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
    

  
Im obigen Beispiel haben wir `ModelEndpointFactory.find_one` verwendet, um den Endpunkt `get_event_category` zu erzeugen, und einen `object_getter` als Callback angegeben, um das Modell anhand von `event_id` abzurufen. Der `lookup_param` gibt den Schlüssel in `kwargs` an, der verwendet wird, um den pk-Wert zum Abrufen des Objektmodells zu definieren, sofern kein `object_getter`-Handler implementiert ist.

  
Andererseits kann es vorkommen, dass Sie Events nach `category_id` auflisten möchten:

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
    

  
Durch die Verwendung von `ModelEndpointFactory.list` mit `queryset_getter` können Sie schnell einen Listen-Endpunkt einrichten, der die zu einer Kategorie gehörenden Events zurückgibt. Beachten Sie, dass unser `queryset_getter` fehlschlagen kann, wenn eine ungültige ID angegeben wird, da dies nur ein Beispiel ist.

  
Beachten Sie außerdem, dass Einstellungen wie `model_config` auch nach der Instanziierung der ModelConfig weiterhin verwendet werden können, wie etwa `create_schema`, `retrieve_schema`, `patch_schema` und `update_schema`.

**  
Pfad- und Query-Parameter**
--------------

  
In `ModelEndpointFactory` werden Pfadparameter geparst, um `path`- und `query`-Parameter zu identifizieren. Diese Parameter werden dann als Felder im Ninja-Eingabeschema angelegt und während der Anfrage geparst, wobei sie als kwargs an den Handler übergeben werden.

Zum Beispiel,

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
    

  
In diesem Beispiel erzeugt der Pfad `/{int:id}/tags/{post_id}?query=int&query1=int` zwei Pfadparameter `['id:int', 'post_id:str']` und zwei Query-Parameter `['query:int', 'query1:int']`. Diese Parameter werden in das Ninja-Eingabeschema gepackt und während der Anfrage geparst, wobei sie als kwargs an den Route-Handler übergeben werden.

  
Beachten Sie, dass definierte `path`- und `query`-Parameter als Pflichtfelder zum Ninja-Eingabeschema hinzugefügt werden, nicht als optional. Außerdem müssen die Datentypen von Pfad und Query mit den Django-URL-Konvertern kompatibel sein.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
