**模型控制器**
=======================

  
模型控制器根据指定的配置，在控制器中为 Django ORM 模型动态生成 CRUD（创建、读取、更新、删除）操作。

  
模型控制器扩展了 `ControllerBase` 类，并引入了两个配置变量，即 `model_config` 和 `model_service` 。

*     
    `model_config` 负责定义与路由和模式生成相关的配置
*     
    `model_service` 指的是用于管理指定模型的 CRUD（创建、读取、更新、删除）操作的类。

  
例如，考虑在 Django 中定义一个 `Event` 模型：

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
    

  
现在，让我们为 `Event` 模型创建一个 `ModelController` 。在 `api.py` 文件中，我们定义了一个 `EventModelController` ：

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
    

  
需要注意的是，模型控制器依赖于 `ninja-schema` 包进行自动模式生成。要安装该包，请使用以下命令：

    pip install ninja-schema
    

  
安装完成后，您可以通过访问 http://localhost:8000/api/docs 来访问自动生成的 API 文档。

  
本文档提供了有关 `EventModelController` 为 `Event` 模型公开的可用路由、模式和功能的详细概述。

**Model Configuration**
-----------------------

  
`ModelConfig` 是一个用于验证和配置模型控制器行为的 Pydantic 模式。关键配置选项包括：

*     
    模型：一个必填字段，表示与 Model Controller 关联的 Django 模型类型。
*     
    async_routes: 表示是否应将控制器路由创建为 `asynchronous` 路由函数
*     
    允许的路由：一个列表，指定了在 Model Controller 中生成的 API 操作的许可。默认值是 `["create", "find_one", "update", "patch", "delete", "list"]` 。
*     
    create_schema：可选的 Pydantic 模式，概述了模型控制器中 `create` 或 `POST` 操作的数据输入类型。默认值为 `None` 。如果未提供，则 `ModelController` 将根据 `schema_config` 选项生成新的模式。
*     
    update_schema：可选的 Pydantic 模式，详细说明了模型控制器中 `update` 或 `PUT` 操作的数据输入类型。默认值为 `None` 。如果未提供，则如果可用，将使用 `create_schema` ，否则将根据 `schema_config` 选项生成新的模式。
*     
    retrieve_schema：一个可选的 Pydantic 模式输出，用于定义各种操作的数据输出类型。默认值为 `None` 。如果未提供，则 `ModelController` 将根据 `schema_config` 选项生成一个模式。
*     
    补丁模式：一个可选的 Pydantic 模式输出，指定了 `patch/PATCH` 操作的输入数据类型。默认值为 `None` 。如果未提供，则 `ModelController` 将生成一个具有所有字段可选的模式。
*     
    模式配置：另一个必填字段，用于描述 Model Controller 操作所需的模式生成方法。配置选项包括：
    *     
        `include` ：要包含的字段列表。默认是 `__all__` 。
        
    *     
        `exclude` ：要排除的字段列表。默认值为 `[]` 。
        
    *     
        `optional` ：要强制为可选的字段列表。默认值为 `[pk]` 。
        
    *     
        `depth` ：生成嵌套模式的深度。
        
    *     
        `read_only_fields` ：创建、更新和补丁操作生成输入模式时要排除的字段列表。
        
    *     
        `write_only_fields` ：在生成 find_one 和列表操作的输出模式时要排除的字段列表。
        
    *     
        分页：模型 `list/GET` 操作的必要条件，用于防止在请求中一次发送 `100_000` 个项目。分页配置要求设置一个 `ModelPagination` Pydantic 模式对象。选项包括：
        
        *     
            `klass` ：类型为 `PaginationBase` 的分页类。默认值为 `PageNumberPaginationExtra` 。
        *     
            `paginator_kwargs` ： `PaginationBase` 初始化的字典值。默认值为 None。
        *     
            `pagination_schema` ：一个 Pydantic 泛型模式，与 `retrieve_schema` 结合为 `list/GET` 操作生成响应模式。
        
          
        例如，如果选择像 `LimitOffsetPagination` 那样的 `ninja` 分页：
        
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
更多关于模型控制器操作**
------------------

  
在 NinjaExtra 模型控制器中，可以通过 `model_config` 选项中的 `allowed_routes` 列表提供的内容来控制控制器的行为。

  
例如，你可以这样创建一个只读控制器：

    from ninja_extra import api_controller, ModelControllerBase, ModelConfig, ModelSchemaConfig
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            allowed_routes=['find_one', 'list'],
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    

  
这将仅为列表创建 `GET/{id}` 和 `GET/` 路由。

  
你还可以向现有 `EventModelController` 添加更多端点。例如：

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

  
每个模型控制器在运行时都会创建一个 `ModelService` 实例来管理模型与控制器的交互。通常，这些模型服务操作本来应该是模型控制器的一部分，但它们被抽象为一个服务，以允许更动态的方法。

    class ModelService(ModelServiceBase):
        """
        Model Service for Model Controller model CRUD operations with simple logic for simple models.
    
        It's advised to override this class if you have a complex model.
        """
        def __init__(self, model: Type[DjangoModel]) -> None:
            self.model = model
    
        # ... (other CRUD methods)
    

  
这些操作是基于模型控制器上的当前操作或模型控制器正在处理的请求来调用的。

### **Using Custom Model Service**

  
在模型控制器中重写 `ModelService` 比重写路由操作更重要。模型控制器中使用的默认 `ModelService` 是为简单的 Django 模型设计的。如果模型复杂，建议重写 `ModelService` 。

  
例如，如果你想改变 `Event` 模型的保存方式：

    from ninja_extra import ModelService
    
    class EventModelService(ModelService):
        def create(self, schema: PydanticModel, **kwargs: Any) -> Any:
            data = schema.dict(by_alias=True)
            data.update(kwargs)
            
            instance = self.model._default_manager.create(**data)
            return instance
    
            
    

然后在 `api.py`

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

  
在 `model_config` 中，将 `async_routes` 设置为 `True`

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
    

  
通过在 `model_config` 中将 `async_routes` 参数设置为 `True` ， `ModelController` 根据配置在 `ModelAsyncEndpointFactory` 和 `ModelEndpointFactory` 之间动态切换，以生成异步或同步端点。

### **模型控制器和模型服务一起**

  
如果需要，也可以将控制器和模型服务合并在一起：

  
例如，使用我们创建的 `EventModelService`

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
    

**模型端点工厂**
-----------

  
`ModelEndpointFactory` 是模型控制器用于无缝生成端点的工厂类。它也可以直接在任何 NinjaExtra 控制器中用于相同目的。

  
例如，如果我们想给新的 `Category` 添加一个 `Event` ，可以按照如下方式进行：

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
    

  
在上述示例中，我们使用 `ModelEndpointFactory.create` 创建了一个端点 `POST /{int:event_id}/new-category` ，并传入了输入和输出模式以及一个自定义处理程序。通过传入 `custom_handler` ，生成的路由函数将其处理操作委托给提供的 `custom_handler` ，而不是调用 `service.create` 。

**  
异步模型端点工厂**
---------------

  
`ModelAsyncEndpointFactory` 与 `ModelEndpointFactory` 具有相同的 API 接口，但专门设计用于生成异步端点。

  
我们可以创建与 `ModelEndpointFactory` 相同的示例

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
    

  
在上面的插图中，我们创建了 `add_event_to_new_category` 作为一个异步函数，并将 `handle_add_event_to_new_category` 也转换为异步函数。

**QueryGetter and ObjectGetter**
--------------------------------

  
`ModelEndpointFactory` 在 `ModelEndpointFactory.find_one` 和 `ModelEndpointFactory.list` 的情况下，分别公开了一种更灵活的获取模型对象或获取查询集筛选器的方式。

  
例如，检索事件的类别（不实际，但用于说明）：

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
    

  
在上述示例中，我们使用 `ModelEndpointFactory.find_one` 创建了一个 `get_event_category` 端点，并提供了一个 `object_getter` 作为回调，用于根据 `event_id` 获取模型。而 `lookup_param` 表示 `kwargs` 中定义用于获取对象模型的 pk 值的键，如果没有实现 `object_getter` 处理程序的话。

  
另一方面，你可能会遇到需要按 `category_id` 对事件进行列表的情况：

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
    

  
通过使用 `ModelEndpointFactory.list` 和 `queryset_getter` ，您可以快速设置一个列表端点，该端点返回属于某个类别的事件。请注意，如果提供了无效的 ID，我们的 `queryset_getter` 可能会失败，因为这只是一个示例。

  
此外，请记住，在 ModelConfig 实例化后，还可以使用像 `model_config` 这样的设置，例如 `create_schema` 、 `retrieve_schema` 、 `patch_schema` 和 `update_schema` 。

**  
路径和查询参数**
--------------

  
在 `ModelEndpointFactory` 中，解析路径参数以识别 `path` 和 `query` 参数。然后，这些参数将在 Ninja 输入模式中创建为字段，并在请求期间进行解析，将它们作为 kwargs 传递给处理程序。

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
    

  
在这个示例中，路径 `/{int:id}/tags/{post_id}?query=int&query1=int` 生成了两个路径参数 `['id:int', 'post_id:str']` 和两个查询参数 `['query:int', 'query1:int']` 。这些参数被打包到 Ninja 输入模式中，并在请求期间进行解析，将它们作为 kwargs 传递给路由处理程序。

  
请注意，当定义 `path` 和 `query` 参数时，它们将作为必填字段添加到 ninja 模式输入中，而不是可选的。此外，路径和查询数据类型必须与 Django URL 转换器兼容。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
