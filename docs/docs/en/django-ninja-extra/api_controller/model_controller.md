**Model Controller**
=======================

  
The model controller dynamically generates CRUD (Create, Read, Update, Delete) operations for a Django ORM model within a controller, based on the specified configuration.

  
The model controller extends the `ControllerBase` class and introduces two configuration variables, namely `model_config` and `model_service`.

*     
    `model_config` is responsible for defining the configuration related to route and schema generation.
*     
    `model_service` refers to the class used to manage CRUD (Create, Read, Update, Delete) operations for the specified model.

  
For example, consider an `Event` model defined in Django:

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
    

  
Now, let's create a `ModelController` for the `Event` model. In the `api.py` file, we define an `EventModelController`:

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
    

  
Note that the model controller relies on the `ninja-schema` package for automatic schema generation. To install the package, use the following command:

    pip install ninja-schema
    

  
After installation, you can access the automatically generated API documentation by visiting http://localhost:8000/api/docs.

  
This document provides a detailed overview of the routes, schemas, and features exposed by the `EventModelController` for the `Event` model.

**Model Configuration**
-----------------------

  
`ModelConfig` is a Pydantic schema used to validate and configure the behavior of the model controller. Key configuration options include:

*     
    Model: A required field representing the Django model type associated with the Model Controller.
*     
    async_routes: Indicates whether the controller routes should be created as `asynchronous` route functions.
*     
    allowed_routes: A list specifying the permitted API operations to be generated in the Model Controller. The default value is `["create", "find_one", "update", "patch", "delete", "list"]`.
*     
    create_schema: An optional Pydantic schema outlining the data input type for the `create` or `POST` operation in the model controller. Default value is `None`. If not provided, the `ModelController` will generate a new schema based on the `schema_config` option.
*     
    update_schema: An optional Pydantic schema detailing the data input type for the `update` or `PUT` operation in the model controller. Default value is `None`. If not provided, the `create_schema` will be used if available, otherwise a new schema will be generated based on the `schema_config` option.
*     
    retrieve_schema: An optional Pydantic schema output defining the data output type for various operations. Default value is `None`. If not provided, the `ModelController` will generate a schema based on the `schema_config` option.
*     
    patch_schema: An optional Pydantic schema output specifying the input data type for the `patch/PATCH` operation. Default value is `None`. If not provided, the `ModelController` will generate a schema with all fields optional.
*     
    schema_config: Another required field describing the schema generation method required for the Model Controller operations. Configuration options include:
    *     
        `include`: A list of fields to include. Default is `__all__`.
        
    *     
        `exclude`: A list of fields to exclude. Default value is `[]`.
        
    *     
        `optional`: A list of fields to force as optional. Default value is `[pk]`.
        
    *     
        `depth`: The depth for generating nested schemas.
        
    *     
        `read_only_fields`: A list of fields to exclude when generating input schemas for create, update, and patch operations.
        
    *     
        `write_only_fields`: A list of fields to exclude when generating output schemas for find_one and list operations.
        
    *     
        pagination: A requirement for the model `list/GET` operation to prevent sending `100_000` items at once in a request. The pagination configuration requires setting a `ModelPagination` Pydantic schema object. Options include:
        
        *     
            `klass`: A pagination class of type `PaginationBase`. Default value is `PageNumberPaginationExtra`.
        *     
            `paginator_kwargs`: Dictionary values for `PaginationBase` initialization. Default value is None.
        *     
            `pagination_schema`: A Pydantic generic schema combined with `retrieve_schema` to generate the response schema for the `list/GET` operation.
        
          
        For example, if choosing a `ninja` pagination like `LimitOffsetPagination`:
        
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
More on Model Controller Operations**
------------------

  
In NinjaExtra model controllers, the behavior of the controller can be controlled through the contents of the `allowed_routes` list in the `model_config` option.

  
For example, you can create a read-only controller like this:

    from ninja_extra import api_controller, ModelControllerBase, ModelConfig, ModelSchemaConfig
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            allowed_routes=['find_one', 'list'],
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    

  
This will only create `GET/{id}` and `GET/` routes for listing.

  
You can also add more endpoints to an existing `EventModelController`. For example:

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

  
Each model controller creates a `ModelService` instance at runtime to manage the interaction between the model and the controller. Typically, these model service operations would have been part of the model controller, but they are abstracted into a service to allow for a more dynamic approach.

    class ModelService(ModelServiceBase):
        """
        Model Service for Model Controller model CRUD operations with simple logic for simple models.
    
        It's advised to override this class if you have a complex model.
        """
        def __init__(self, model: Type[DjangoModel]) -> None:
            self.model = model
    
        # ... (other CRUD methods)
    

  
These operations are called based on the current operation on the model controller or the request the model controller is processing.

### **Using Custom Model Service**

  
Overriding the `ModelService` in a model controller is more important than overriding route operations. The default `ModelService` used in model controllers is designed for simple Django models. If the model is complex, overriding the `ModelService` is recommended.

  
For example, if you want to change how the `Event` model is saved:

    from ninja_extra import ModelService
    
    class EventModelService(ModelService):
        def create(self, schema: PydanticModel, **kwargs: Any) -> Any:
            data = schema.dict(by_alias=True)
            data.update(kwargs)
            
            instance = self.model._default_manager.create(**data)
            return instance
    
            
    

Then in `api.py`

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
    

### **Enable Async Routes**

  
In `model_config`, set `async_routes` to `True`

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
    

  
By setting the `async_routes` parameter to `True` in `model_config`, the `ModelController` dynamically switches between `ModelAsyncEndpointFactory` and `ModelEndpointFactory` based on the configuration to generate async or sync endpoints.

### **Model Controller and Model Service Together**

  
If needed, the controller and model service can also be merged together:

  
For example, using the `EventModelService` we created

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

  
`ModelEndpointFactory` is a factory class used by the model controller to seamlessly generate endpoints. It can also be used directly in any NinjaExtra controller for the same purpose.

  
For example, if we want to add an `Event` to a new `Category`, it can be done as follows:

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
    

  
In the above example, we used `ModelEndpointFactory.create` to create an endpoint `POST /{int:event_id}/new-category`, passing in the input and output schemas along with a custom handler. By passing in `custom_handler`, the generated route function delegates its handling operation to the provided `custom_handler` instead of calling `service.create`.

**  
Async Model Endpoint Factory**
---------------

  
`ModelAsyncEndpointFactory` has the same API interface as `ModelEndpointFactory`, but is specifically designed to generate async endpoints.

  
We can create the same example as with `ModelEndpointFactory`

For example:

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
    

  
In the illustration above, we created `add_event_to_new_category` as an async function and also converted `handle_add_event_to_new_category` to an async function.

**QueryGetter and ObjectGetter**
--------------------------------

  
`ModelEndpointFactory` exposes a more flexible way to get a model object or a queryset filter, in the case of `ModelEndpointFactory.find_one` and `ModelEndpointFactory.list` respectively.

  
For example, retrieving the category of an event (not practical, but for illustration):

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
    

  
In the above example, we used `ModelEndpointFactory.find_one` to create a `get_event_category` endpoint and provided an `object_getter` as a callback to fetch the model based on `event_id`. The `lookup_param` indicates the key in `kwargs` used to define the pk value for fetching the object model, if no `object_getter` handler is implemented.

  
On the other hand, you may encounter a situation where you need to list events by `category_id`:

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
    

  
By using `ModelEndpointFactory.list` with `queryset_getter`, you can quickly set up a list endpoint that returns events belonging to a category. Note that if an invalid ID is provided, our `queryset_getter` may fail since this is just an example.

  
Additionally, keep in mind that after the ModelConfig is instantiated, settings like `model_config` can still be used, such as `create_schema`, `retrieve_schema`, `patch_schema`, and `update_schema`.

**  
Path and Query Parameters**
--------------

  
In `ModelEndpointFactory`, path parameters are parsed to identify `path` and `query` parameters. These parameters are then created as fields in the Ninja input schema and parsed during the request, passing them as kwargs to the handler.

For example,

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
    

  
In this example, the path `/{int:id}/tags/{post_id}?query=int&query1=int` generates two path parameters `['id:int', 'post_id:str']` and two query parameters `['query:int', 'query1:int']`. These parameters are packed into the Ninja input schema and parsed during the request, passing them as kwargs to the route handler.

  
Note that when `path` and `query` parameters are defined, they are added as required fields to the ninja schema input, not optional. Additionally, path and query data types must be compatible with Django URL converters.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
