**モデルコントローラ**
=======================

  
モデルコントローラは、指定された設定に基づいて、コントローラ内の Django ORM モデルに対する CRUD（Create、Read、Update、Delete）操作を動的に生成します。

  
モデルコントローラは `ControllerBase` クラスを継承し、`model_config` と `model_service` という 2 つの設定変数を導入します。

*     
    `model_config` は、ルートと schema の生成に関する設定を定義する役割を担います。
*     
    `model_service` は、指定されたモデルに対する CRUD（Create、Read、Update、Delete）操作を管理するために使用されるクラスを指します。

  
たとえば、Django で次のように `Event` モデルが定義されているとします：

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
    

  
次に、`Event` モデル用の `ModelController` を作成してみましょう。`api.py` ファイル内で `EventModelController` を定義します：

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
    

  
なお、モデルコントローラは自動 schema 生成のために `ninja-schema` パッケージに依存しています。このパッケージをインストールするには、次のコマンドを使用します：

    pip install ninja-schema
    

  
インストール後、http://localhost:8000/api/docs にアクセスすると、自動生成された API ドキュメントを閲覧できます。

  
このドキュメントでは、`Event` モデルに対して `EventModelController` が公開するルート、schema、および機能の詳細な概要を提供します。

**モデル設定**
-----------------------

  
`ModelConfig` は、モデルコントローラの挙動を検証および設定するために使用される Pydantic schema です。主な設定オプションは次のとおりです：

*     
    Model: モデルコントローラに関連付けられた Django モデルの型を表す必須フィールド。
*     
    async_routes: コントローラのルートを `asynchronous`（非同期）な route 関数として作成するかどうかを示します。
*     
    allowed_routes: モデルコントローラで生成が許可される API 操作を指定するリスト。デフォルト値は `["create", "find_one", "update", "patch", "delete", "list"]` です。
*     
    create_schema: モデルコントローラにおける `create` または `POST` 操作のデータ入力型を示す、オプションの Pydantic schema。デフォルト値は `None` です。指定しない場合、`ModelController` は `schema_config` オプションに基づいて新しい schema を生成します。
*     
    update_schema: モデルコントローラにおける `update` または `PUT` 操作のデータ入力型を詳述する、オプションの Pydantic schema。デフォルト値は `None` です。指定しない場合、`create_schema` が利用可能ならそれが使用され、そうでなければ `schema_config` オプションに基づいて新しい schema が生成されます。
*     
    retrieve_schema: さまざまな操作のデータ出力型を定義する、オプションの Pydantic schema 出力。デフォルト値は `None` です。指定しない場合、`ModelController` は `schema_config` オプションに基づいて schema を生成します。
*     
    patch_schema: `patch/PATCH` 操作の入力データ型を指定する、オプションの Pydantic schema 出力。デフォルト値は `None` です。指定しない場合、`ModelController` はすべてのフィールドを任意（optional）にした schema を生成します。
*     
    schema_config: モデルコントローラの操作に必要な schema 生成方法を記述する、もう一つの必須フィールド。設定オプションは次のとおりです：
    *     
        `include`: 含めるフィールドのリスト。デフォルトは `__all__` です。
        
    *     
        `exclude`: 除外するフィールドのリスト。デフォルト値は `[]` です。
        
    *     
        `optional`: 強制的に任意（optional）にするフィールドのリスト。デフォルト値は `[pk]` です。
        
    *     
        `depth`: ネストされた schema を生成する際の深さ。
        
    *     
        `read_only_fields`: create、update、patch 操作用の入力 schema を生成する際に除外されるフィールドのリスト。
        
    *     
        `write_only_fields`: find_one と list 操作用の出力 schema を生成する際に除外されるフィールドのリスト。
        
    *     
        pagination: 1 つのリクエストで `100_000` 件のアイテムを一度に送信することを防ぐための、モデルの `list/GET` 操作に対する要件。ページネーション設定では、`ModelPagination` Pydantic schema オブジェクトの設定が必要です。オプションは次のとおりです：
        
        *     
            `klass`: `PaginationBase` 型のページネーションクラス。デフォルト値は `PageNumberPaginationExtra` です。
        *     
            `paginator_kwargs`: `PaginationBase` の初期化に使う辞書値。デフォルト値は None です。
        *     
            `pagination_schema`: `retrieve_schema` と組み合わせられて `list/GET` 操作のレスポンス schema を生成する、Pydantic のジェネリック schema。
        
          
        たとえば、`LimitOffsetPagination` のような `ninja` のページネーションを選択する場合は次のようになります：
        
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
モデルコントローラの操作についての詳細**
------------------

  
NinjaExtra のモデルコントローラでは、`model_config` オプションの `allowed_routes` リストの内容を通じてコントローラの挙動を制御できます。

  
たとえば、読み取り専用のコントローラを次のように作成できます：

    from ninja_extra import api_controller, ModelControllerBase, ModelConfig, ModelSchemaConfig
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            allowed_routes=['find_one', 'list'],
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    

  
これにより、一覧取得用の `GET/{id}` と `GET/` ルートのみが作成されます。

  
既存の `EventModelController` にさらにエンドポイントを追加することもできます。たとえば：

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
    

**モデルサービス**
-----------------

  
各モデルコントローラは、実行時に `ModelService` インスタンスを作成し、モデルとコントローラの間のやり取りを管理します。通常、これらのモデルサービス操作はモデルコントローラの一部であるはずのものですが、より動的なアプローチを可能にするためにサービスとして抽象化されています。

    class ModelService(ModelServiceBase):
        """
        Model Service for Model Controller model CRUD operations with simple logic for simple models.
    
        It's advised to override this class if you have a complex model.
        """
        def __init__(self, model: Type[DjangoModel]) -> None:
            self.model = model
    
        # ... (other CRUD methods)
    

  
これらの操作は、モデルコントローラ上で現在行われている操作、つまりモデルコントローラが処理しているリクエストに基づいて呼び出されます。

### **カスタムモデルサービスの使用**

  
モデルコントローラで `ModelService` をオーバーライドすることは、ルート操作をオーバーライドすることよりも重要です。モデルコントローラで使用されるデフォルトの `ModelService` は、シンプルな Django モデル向けに設計されています。モデルが複雑な場合は、`ModelService` をオーバーライドすることをお勧めします。

  
たとえば、`Event` モデルの保存方法を変更したい場合は次のようになります：

    from ninja_extra import ModelService
    
    class EventModelService(ModelService):
        def create(self, schema: PydanticModel, **kwargs: Any) -> Any:
            data = schema.dict(by_alias=True)
            data.update(kwargs)
            
            instance = self.model._default_manager.create(**data)
            return instance
    
            
    

  
そして `api.py` 内では：

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
    

### **非同期ルートを有効にする**

  
`model_config` で `async_routes` を `True` に設定します

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
    

  
`model_config` の `async_routes` パラメータを `True` に設定すると、`ModelController` は設定に基づいて `ModelAsyncEndpointFactory` と `ModelEndpointFactory` の間を動的に切り替え、非同期または同期のエンドポイントを生成します。

### **モデルコントローラとモデルサービスの統合**

  
必要であれば、コントローラとモデルサービスを 1 つにまとめることもできます：

  
たとえば、先ほど作成した `EventModelService` を使う場合は次のようになります：

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
    

**モデルエンドポイントファクトリ**
-----------

  
`ModelEndpointFactory` は、モデルコントローラがエンドポイントをシームレスに生成するために使用するファクトリクラスです。同じ目的のために、任意の NinjaExtra コントローラで直接使用することもできます。

  
たとえば、`Event` を新しい `Category` に追加したい場合は、次のように実現できます：

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
    

  
上記の例では、`ModelEndpointFactory.create` を使ってエンドポイント `POST /{int:event_id}/new-category` を作成し、入力と出力の schema に加えてカスタムハンドラを渡しました。`custom_handler` を渡すことで、生成された route 関数は `service.create` を呼び出す代わりに、処理操作を提供された `custom_handler` に委譲します。

**  
非同期モデルエンドポイントファクトリ**
---------------

  
`ModelAsyncEndpointFactory` は `ModelEndpointFactory` と同じ API インターフェースを持ちますが、非同期エンドポイントを生成することに特化して設計されています。

  
`ModelEndpointFactory` と同じ例を作成できます

たとえば：

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
    

  
この例では、`add_event_to_new_category` を非同期関数として作成し、`handle_add_event_to_new_category` も非同期関数に変換しました。

**QueryGetter と ObjectGetter**
--------------------------------

  
`ModelEndpointFactory` は、それぞれ `ModelEndpointFactory.find_one` と `ModelEndpointFactory.list` のケースにおいて、モデルオブジェクトや queryset フィルタを取得するための、より柔軟な方法を公開しています。

  
たとえば、イベントのカテゴリを取得する場合（実用的ではありませんが、説明のための例です）：

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
    

  
上記の例では、`ModelEndpointFactory.find_one` を使って `get_event_category` エンドポイントを作成し、`event_id` に基づいてモデルを取得するコールバックとして `object_getter` を提供しました。`lookup_param` は、`object_getter` ハンドラが実装されていない場合に、オブジェクトモデルを取得するための pk 値を定義するために使用される `kwargs` 内のキーを示します。

  
一方、`category_id` によってイベントを一覧表示する必要がある状況に遭遇することもあるでしょう：

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
    

  
`ModelEndpointFactory.list` を `queryset_getter` と組み合わせて使うことで、あるカテゴリに属するイベントを返す list エンドポイントを素早くセットアップできます。なお、無効な ID が渡された場合、`queryset_getter` は失敗する可能性があります。これはあくまで例だからです。

  
さらに、ModelConfig がインスタンス化された後でも、`create_schema`、`retrieve_schema`、`patch_schema`、`update_schema` のような `model_config` の設定を引き続き使用できることに注意してください。

**  
パスパラメータとクエリパラメータ**
--------------

  
`ModelEndpointFactory` では、`path` パラメータと `query` パラメータを識別するためにパスが解析されます。これらのパラメータは、Ninja の入力 schema 内にフィールドとして作成され、リクエスト中に解析され、ハンドラに kwargs として渡されます。

たとえば、

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
    

  
この例では、パス `/{int:id}/tags/{post_id}?query=int&query1=int` は 2 つのパスパラメータ `['id:int', 'post_id:str']` と 2 つのクエリパラメータ `['query:int', 'query1:int']` を生成します。これらのパラメータは Ninja の入力 schema にパックされ、リクエスト中に解析され、route ハンドラに kwargs として渡されます。

  
なお、`path` と `query` のパラメータが定義されると、それらはオプションではなく、必須フィールドとして ninja の schema 入力に追加されます。さらに、path と query のデータ型は Django の URL コンバータと互換性がある必要があります。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
