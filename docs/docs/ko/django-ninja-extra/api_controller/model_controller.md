**모델 컨트롤러**
=======================

  
모델 컨트롤러는 지정된 구성에 따라 컨트롤러 내에서 Django ORM 모델에 대한 CRUD(Create, Read, Update, Delete) 작업을 동적으로 생성합니다.

  
모델 컨트롤러는 `ControllerBase` 클래스를 확장하며 `model_config`와 `model_service`라는 두 가지 구성 변수를 도입합니다.

*     
    `model_config`는 라우트 및 스키마 생성과 관련된 구성을 정의하는 역할을 합니다.
*     
    `model_service`는 지정된 모델에 대한 CRUD(Create, Read, Update, Delete) 작업을 관리하는 데 사용되는 클래스를 나타냅니다.

  
예를 들어, Django에서 정의된 `Event` 모델을 고려해 봅시다:

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
    

  
이제 `Event` 모델에 대한 `ModelController`를 만들어 봅시다. `api.py` 파일에서 `EventModelController`를 정의합니다:

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
    

  
모델 컨트롤러는 자동 스키마 생성을 위해 `ninja-schema` 패키지에 의존한다는 점에 유의하세요. 패키지를 설치하려면 다음 명령을 사용하세요:

    pip install ninja-schema
    

  
설치 후 http://localhost:8000/api/docs를 방문하여 자동 생성된 API 문서에 액세스할 수 있습니다.

  
이 문서는 `Event` 모델에 대해 `EventModelController`가 노출하는 라우트, 스키마 및 기능에 대한 자세한 개요를 제공합니다.

**모델 구성**
-----------------------

  
`ModelConfig`는 모델 컨트롤러의 동작을 검증하고 구성하는 데 사용되는 Pydantic 스키마입니다. 주요 구성 옵션은 다음과 같습니다:

*     
    Model: 모델 컨트롤러와 연결된 Django 모델 타입을 나타내는 필수 필드.
*     
    async_routes: 컨트롤러 라우트를 `비동기` 라우트 함수로 생성해야 하는지 여부를 나타냅니다.
*     
    allowed_routes: 모델 컨트롤러에서 생성할 허용된 API 작업을 지정하는 목록. 기본값은 `["create", "find_one", "update", "patch", "delete", "list"]`입니다.
*     
    create_schema: 모델 컨트롤러의 `create` 또는 `POST` 작업에 대한 데이터 입력 타입을 설명하는 선택적 Pydantic 스키마. 기본값은 `None`입니다. 제공되지 않으면 `ModelController`가 `schema_config` 옵션을 기반으로 새 스키마를 생성합니다.
*     
    update_schema: 모델 컨트롤러의 `update` 또는 `PUT` 작업에 대한 데이터 입력 타입을 자세히 설명하는 선택적 Pydantic 스키마. 기본값은 `None`입니다. 제공되지 않으면 사용 가능한 경우 `create_schema`가 사용되며, 그렇지 않으면 `schema_config` 옵션을 기반으로 새 스키마가 생성됩니다.
*     
    retrieve_schema: 다양한 작업에 대한 데이터 출력 타입을 정의하는 선택적 Pydantic 스키마 출력. 기본값은 `None`입니다. 제공되지 않으면 `ModelController`가 `schema_config` 옵션을 기반으로 스키마를 생성합니다.
*     
    patch_schema: `patch/PATCH` 작업에 대한 입력 데이터 타입을 지정하는 선택적 Pydantic 스키마 출력. 기본값은 `None`입니다. 제공되지 않으면 `ModelController`가 모든 필드가 선택 사항인 스키마를 생성합니다.
*     
    schema_config: 모델 컨트롤러 작업에 필요한 스키마 생성 방법을 설명하는 또 다른 필수 필드. 구성 옵션은 다음과 같습니다:
    *     
        `include`: 포함할 필드 목록. 기본값은 `__all__`입니다.
        
    *     
        `exclude`: 제외할 필드 목록. 기본값은 `[]`입니다.
        
    *     
        `optional`: 선택 사항으로 강제할 필드 목록. 기본값은 `[pk]`입니다.
        
    *     
        `depth`: 중첩 스키마 생성을 위한 깊이.
        
    *     
        `read_only_fields`: create, update 및 patch 작업에 대한 입력 스키마를 생성할 때 제외할 필드 목록.
        
    *     
        `write_only_fields`: find_one 및 list 작업에 대한 출력 스키마를 생성할 때 제외할 필드 목록.
        
    *     
        pagination: 요청에서 한 번에 `100_000`개의 항목을 전송하는 것을 방지하기 위한 모델 `list/GET` 작업의 요구 사항. 페이지네이션 구성에는 `ModelPagination` Pydantic 스키마 객체 설정이 필요합니다. 옵션은 다음과 같습니다:
        
        *     
            `klass`: `PaginationBase` 타입의 페이지네이션 클래스. 기본값은 `PageNumberPaginationExtra`입니다.
        *     
            `paginator_kwargs`: `PaginationBase` 초기화를 위한 딕셔너리 값. 기본값은 None입니다.
        *     
            `pagination_schema`: `list/GET` 작업에 대한 응답 스키마를 생성하기 위해 `retrieve_schema`와 결합된 Pydantic 제네릭 스키마.
        
          
        예를 들어, `LimitOffsetPagination`과 같은 `ninja` 페이지네이션을 선택하는 경우:
        
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
모델 컨트롤러 작업에 대한 추가 정보**
------------------

  
NinjaExtra 모델 컨트롤러에서 컨트롤러의 동작은 `model_config` 옵션의 `allowed_routes` 목록 내용을 통해 제어할 수 있습니다.

  
예를 들어, 다음과 같이 읽기 전용 컨트롤러를 만들 수 있습니다:

    from ninja_extra import api_controller, ModelControllerBase, ModelConfig, ModelSchemaConfig
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            allowed_routes=['find_one', 'list'],
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    

  
이렇게 하면 목록을 위한 `GET/{id}` 및 `GET/` 라우트만 생성됩니다.

  
기존 `EventModelController`에 더 많은 엔드포인트를 추가할 수도 있습니다. 예를 들어:

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
    

**모델 서비스**
-----------------

  
각 모델 컨트롤러는 런타임에 `ModelService` 인스턴스를 생성하여 모델과 컨트롤러 간의 상호 작용을 관리합니다. 일반적으로 이러한 모델 서비스 작업은 모델 컨트롤러의 일부였지만, 더 동적인 접근 방식을 허용하기 위해 서비스로 추상화되었습니다.

    class ModelService(ModelServiceBase):
        """
        Model Service for Model Controller model CRUD operations with simple logic for simple models.
    
        It's advised to override this class if you have a complex model.
        """
        def __init__(self, model: Type[DjangoModel]) -> None:
            self.model = model
    
        # ... (other CRUD methods)
    

  
이러한 작업은 모델 컨트롤러의 현재 작업 또는 모델 컨트롤러가 처리 중인 요청에 따라 호출됩니다.

### **커스텀 모델 서비스 사용하기**

  
모델 컨트롤러에서 `ModelService`를 오버라이드하는 것이 라우트 작업을 오버라이드하는 것보다 더 중요합니다. 모델 컨트롤러에서 사용되는 기본 `ModelService`는 간단한 Django 모델을 위해 설계되었습니다. 모델이 복잡한 경우 `ModelService`를 오버라이드하는 것이 권장됩니다.

  
예를 들어, `Event` 모델의 저장 방식을 변경하려는 경우:

    from ninja_extra import ModelService
    
    class EventModelService(ModelService):
        def create(self, schema: PydanticModel, **kwargs: Any) -> Any:
            data = schema.dict(by_alias=True)
            data.update(kwargs)
            
            instance = self.model._default_manager.create(**data)
            return instance
    
            
    

그런 다음 `api.py`에서

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
    

### **비동기 라우트 활성화**

  
`model_config`에서 `async_routes`를 `True`로 설정합니다

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
    

  
`model_config`에서 `async_routes` 파라미터를 `True`로 설정하면 `ModelController`가 구성에 따라 `ModelAsyncEndpointFactory`와 `ModelEndpointFactory` 사이를 동적으로 전환하여 비동기 또는 동기 엔드포인트를 생성합니다.

### **모델 컨트롤러와 모델 서비스 함께 사용하기**

  
필요한 경우 컨트롤러와 모델 서비스를 함께 병합할 수도 있습니다:

  
예를 들어, 우리가 만든 `EventModelService`를 사용합니다

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
    

**모델 엔드포인트 팩토리**
-----------

  
`ModelEndpointFactory`는 모델 컨트롤러가 원활하게 엔드포인트를 생성하는 데 사용하는 팩토리 클래스입니다. 동일한 목적으로 모든 NinjaExtra 컨트롤러에서 직접 사용할 수도 있습니다.

  
예를 들어, 새 `Category`에 `Event`를 추가하려면 다음과 같이 할 수 있습니다:

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
    

  
위 예시에서 우리는 `ModelEndpointFactory.create`를 사용하여 `POST /{int:event_id}/new-category` 엔드포인트를 생성했으며, 입력 및 출력 스키마와 함께 커스텀 핸들러를 전달했습니다. `custom_handler`를 전달함으로써 생성된 라우트 함수는 `service.create`를 호출하는 대신 제공된 `custom_handler`에 처리 작업을 위임합니다.

**  
비동기 모델 엔드포인트 팩토리**
---------------

  
`ModelAsyncEndpointFactory`는 `ModelEndpointFactory`와 동일한 API 인터페이스를 갖지만 비동기 엔드포인트를 생성하도록 특별히 설계되었습니다.

  
`ModelEndpointFactory`와 동일한 예제를 만들 수 있습니다

예를 들어:

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
    

  
위 그림에서 우리는 `add_event_to_new_category`를 비동기 함수로 만들었고 `handle_add_event_to_new_category`도 비동기 함수로 변환했습니다.

**QueryGetter와 ObjectGetter**
--------------------------------

  
`ModelEndpointFactory`는 각각 `ModelEndpointFactory.find_one` 및 `ModelEndpointFactory.list`의 경우 모델 객체 또는 쿼리셋 필터를 가져오는 더 유연한 방법을 노출합니다.

  
예를 들어, 이벤트의 카테고리 검색(실용적이지는 않지만 설명을 위해):

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
    

  
위 예시에서 우리는 `ModelEndpointFactory.find_one`을 사용하여 `get_event_category` 엔드포인트를 생성했으며 `event_id`를 기반으로 모델을 가져오기 위한 콜백으로 `object_getter`를 제공했습니다. `lookup_param`은 `object_getter` 핸들러가 구현되지 않은 경우 객체 모델을 가져오기 위한 pk 값을 정의하는 데 사용되는 `kwargs`의 키를 나타냅니다.

  
반면에 `category_id`로 이벤트를 나열해야 하는 상황이 발생할 수 있습니다:

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
    

  
`ModelEndpointFactory.list`를 `queryset_getter`와 함께 사용하면 카테고리에 속하는 이벤트를 반환하는 목록 엔드포인트를 빠르게 설정할 수 있습니다. 유효하지 않은 ID가 제공되면 `queryset_getter`가 실패할 수 있다는 점에 유의하세요. 이는 단지 예시이기 때문입니다.

  
또한 ModelConfig가 인스턴스화된 후에도 `create_schema`, `retrieve_schema`, `patch_schema`, `update_schema`와 같은 `model_config` 설정을 계속 사용할 수 있다는 점을 명심하세요.

**  
경로 및 쿼리 파라미터**
--------------

  
`ModelEndpointFactory`에서 경로 파라미터는 `path` 및 `query` 파라미터를 식별하기 위해 파싱됩니다. 그런 다음 이러한 파라미터는 Ninja 입력 스키마에서 필드로 생성되고 요청 중에 파싱되어 핸들러에 kwargs로 전달됩니다.

예를 들어,

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
    

  
이 예시에서 경로 `/{int:id}/tags/{post_id}?query=int&query1=int`는 두 개의 경로 파라미터 `['id:int', 'post_id:str']`와 두 개의 쿼리 파라미터 `['query:int', 'query1:int']`를 생성합니다. 이러한 파라미터는 Ninja 입력 스키마에 패킹되고 요청 중에 파싱되어 라우트 핸들러에 kwargs로 전달됩니다.

  
`path` 및 `query` 파라미터가 정의되면 선택 사항이 아닌 필수 필드로 ninja 스키마 입력에 추가된다는 점에 유의하세요. 또한 경로 및 쿼리 데이터 타입은 Django URL 변환기와 호환되어야 합니다.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
