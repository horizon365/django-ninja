**Model Controller**
=======================

  
Модельный контроллер динамически генерирует CRUD-операции (Create, Read, Update, Delete) для модели Django ORM внутри контроллера на основе заданной конфигурации.

  
Модельный контроллер расширяет класс `ControllerBase` и вводит две конфигурационные переменные, а именно `model_config` и `model_service`.

*     
    `model_config` отвечает за определение конфигурации, связанной с генерацией маршрутов и схем.
*     
    `model_service` — это класс, используемый для управления CRUD-операциями (Create, Read, Update, Delete) для указанной модели.

  
Например, рассмотрим модель `Event`, определённую в Django:

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
    

  
Теперь давайте создадим `ModelController` для модели `Event`. В файле `api.py` мы определяем `EventModelController`:

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
    

  
Обратите внимание, что модельный контроллер полагается на пакет `ninja-schema` для автоматической генерации схем. Чтобы установить пакет, используйте следующую команду:

    pip install ninja-schema
    

  
После установки вы можете получить доступ к автоматически сгенерированной документации API, посетив http://localhost:8000/api/docs.

  
Этот документ предоставляет подробный обзор маршрутов, схем и возможностей, предоставляемых `EventModelController` для модели `Event`.

**Конфигурация модели**
-----------------------

  
`ModelConfig` — это Pydantic-схема, используемая для валидации и настройки поведения модельного контроллера. Ключевые опции конфигурации включают:

*     
    Model: обязательное поле, представляющее тип модели Django, связанный с Model Controller.
*     
    async_routes: указывает, должны ли маршруты контроллера создаваться как `асинхронные` функции маршрутов.
*     
    allowed_routes: список, указывающий разрешённые API-операции, которые будут сгенерированы в Model Controller. Значение по умолчанию — `["create", "find_one", "update", "patch", "delete", "list"]`.
*     
    create_schema: необязательная Pydantic-схема, описывающая тип входных данных для операции `create` или `POST` в модельном контроллере. Значение по умолчанию — `None`. Если не указана, `ModelController` сгенерирует новую схему на основе опции `schema_config`.
*     
    update_schema: необязательная Pydantic-схема, описывающая тип входных данных для операции `update` или `PUT` в модельном контроллере. Значение по умолчанию — `None`. Если не указана, будет использована `create_schema`, если она доступна, в противном случае новая схема будет сгенерирована на основе опции `schema_config`.
*     
    retrieve_schema: необязательная выходная Pydantic-схема, определяющая тип выходных данных для различных операций. Значение по умолчанию — `None`. Если не указана, `ModelController` сгенерирует схему на основе опции `schema_config`.
*     
    patch_schema: необязательная выходная Pydantic-схема, определяющая тип входных данных для операции `patch/PATCH`. Значение по умолчанию — `None`. Если не указана, `ModelController` сгенерирует схему, в которой все поля будут необязательными.
*     
    schema_config: ещё одно обязательное поле, описывающее способ генерации схем, необходимый для операций Model Controller. Опции конфигурации включают:
    *     
        `include`: список полей для включения. По умолчанию `__all__`.
        
    *     
        `exclude`: список полей для исключения. Значение по умолчанию `[]`.
        
    *     
        `optional`: список полей, которые принудительно делаются необязательными. Значение по умолчанию `[pk]`.
        
    *     
        `depth`: глубина для генерации вложенных схем.
        
    *     
        `read_only_fields`: список полей, исключаемых при генерации входных схем для операций create, update и patch.
        
    *     
        `write_only_fields`: список полей, исключаемых при генерации выходных схем для операций find_one и list.
        
    *     
        pagination: требование для операции модели `list/GET`, чтобы предотвратить отправку `100_000` элементов за один запрос. Конфигурация пагинации требует установки Pydantic-объекта схемы `ModelPagination`. Опции включают:
        
        *     
            `klass`: класс пагинации типа `PaginationBase`. Значение по умолчанию — `PageNumberPaginationExtra`.
        *     
            `paginator_kwargs`: значения словаря для инициализации `PaginationBase`. Значение по умолчанию — None.
        *     
            `pagination_schema`: универсальная Pydantic-схема, комбинируемая с `retrieve_schema` для генерации схемы ответа для операции `list/GET`.
        
          
        Например, если выбрать пагинацию `ninja` вроде `LimitOffsetPagination`:
        
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
Подробнее об операциях Model Controller**
------------------

  
В модельных контроллерах NinjaExtra поведение контроллера можно управлять через содержимое списка `allowed_routes` в опции `model_config`.

  
Например, вы можете создать контроллер только для чтения следующим образом:

    from ninja_extra import api_controller, ModelControllerBase, ModelConfig, ModelSchemaConfig
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            allowed_routes=['find_one', 'list'],
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    

  
Это создаст только маршруты `GET/{id}` и `GET/` для вывода списка.

  
Вы также можете добавить больше эндпоинтов к существующему `EventModelController`. Например:

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

  
Каждый модельный контроллер создаёт экземпляр `ModelService` во время выполнения для управления взаимодействием между моделью и контроллером. Обычно эти операции модельного сервиса были бы частью модельного контроллера, но они абстрагированы в сервис, чтобы обеспечить более динамичный подход.

    class ModelService(ModelServiceBase):
        """
        Model Service for Model Controller model CRUD operations with simple logic for simple models.
    
        It's advised to override this class if you have a complex model.
        """
        def __init__(self, model: Type[DjangoModel]) -> None:
            self.model = model
    
        # ... (other CRUD methods)
    

  
Эти операции вызываются в зависимости от текущей операции над модельным контроллером или от запроса, который обрабатывает модельный контроллер.

### **Использование кастомного Model Service**

  
Переопределение `ModelService` в модельном контроллере важнее, чем переопределение операций маршрутов. Используемый по умолчанию в модельных контроллерах `ModelService` спроектирован для простых моделей Django. Если модель сложная, рекомендуется переопределить `ModelService`.

  
Например, если вы хотите изменить способ сохранения модели `Event`:

    from ninja_extra import ModelService
    
    class EventModelService(ModelService):
        def create(self, schema: PydanticModel, **kwargs: Any) -> Any:
            data = schema.dict(by_alias=True)
            data.update(kwargs)
            
            instance = self.model._default_manager.create(**data)
            return instance
    
            
    

Затем в `api.py`

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
    

### **Включение асинхронных маршрутов**

  
В `model_config` установите `async_routes` в `True`

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
    

  
Установив параметр `async_routes` в `True` в `model_config`, `ModelController` динамически переключается между `ModelAsyncEndpointFactory` и `ModelEndpointFactory` в зависимости от конфигурации, чтобы генерировать асинхронные или синхронные эндпоинты.

### **Model Controller и Model Service вместе**

  
При необходимости контроллер и модельный сервис также можно объединить вместе:

  
Например, используя созданный нами `EventModelService`

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

  
`ModelEndpointFactory` — это класс-фабрика, используемый модельным контроллером для бесшовной генерации эндпоинтов. Его также можно использовать напрямую в любом контроллере NinjaExtra для той же цели.

  
Например, если мы хотим добавить `Event` в новую `Category`, это можно сделать следующим образом:

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
    

  
В приведённом выше примере мы использовали `ModelEndpointFactory.create` для создания эндпоинта `POST /{int:event_id}/new-category`, передав входную и выходную схемы вместе с кастомным обработчиком. Передавая `custom_handler`, сгенерированная функция маршрута делегирует свою операцию обработки предоставленному `custom_handler` вместо вызова `service.create`.

**  
Асинхронная Model Endpoint Factory**
---------------

  
`ModelAsyncEndpointFactory` имеет тот же API-интерфейс, что и `ModelEndpointFactory`, но специально предназначен для генерации асинхронных эндпоинтов.

  
Мы можем создать тот же пример, что и с `ModelEndpointFactory`

Например:

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
    

  
В этом примере мы создали `add_event_to_new_category` как асинхронную функцию, а также преобразовали `handle_add_event_to_new_category` в асинхронную функцию.

**QueryGetter и ObjectGetter**
--------------------------------

  
`ModelEndpointFactory` предоставляет более гибкий способ получения объекта модели или фильтра queryset — в случае `ModelEndpointFactory.find_one` и `ModelEndpointFactory.list` соответственно.

  
Например, получение категории события (непрактично, но для иллюстрации):

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
    

  
В приведённом выше примере мы использовали `ModelEndpointFactory.find_one` для создания эндпоинта `get_event_category` и предоставили `object_getter` в качестве обратного вызова для выборки модели на основе `event_id`. `lookup_param` указывает ключ в `kwargs`, используемый для определения значения pk при выборке объекта модели, если не реализован обработчик `object_getter`.

  
С другой стороны, вы можете столкнуться с ситуацией, когда нужно вывести список событий по `category_id`:

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
    

  
Используя `ModelEndpointFactory.list` с `queryset_getter`, вы можете быстро настроить эндпоинт списка, возвращающий события, принадлежащие категории. Обратите внимание, что при передаче недопустимого ID наш `queryset_getter` может завершиться ошибкой, поскольку это всего лишь пример.

  
Кроме того, имейте в виду, что после инстанцирования ModelConfig такие настройки, как `model_config`, всё ещё можно использовать, например `create_schema`, `retrieve_schema`, `patch_schema` и `update_schema`.

**  
Параметры пути и запроса**
--------------

  
В `ModelEndpointFactory` параметры пути разбираются для определения параметров `path` и `query`. Затем эти параметры создаются как поля во входной схеме Ninja и разбираются во время запроса, передаваясь в обработчик как kwargs.

Например,

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
    

  
В этом примере путь `/{int:id}/tags/{post_id}?query=int&query1=int` генерирует два параметра пути `['id:int', 'post_id:str']` и два параметра запроса `['query:int', 'query1:int']`. Эти параметры упаковываются во входную схему Ninja и разбираются во время запроса, передаваясь как kwargs в обработчик маршрута.

  
Обратите внимание, что когда параметры `path` и `query` определены, они добавляются как обязательные поля во входную схему ninja, а не как необязательные. Кроме того, типы данных пути и запроса должны быть совместимы с конвертерами URL Django.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
