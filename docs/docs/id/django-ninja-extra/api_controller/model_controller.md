**Model Controller**
=======================

  
Model controller secara dinamis menghasilkan operasi CRUD (Create, Read, Update, Delete) untuk sebuah model Django ORM di dalam controller, berdasarkan konfigurasi yang ditentukan.

  
Model controller meng-extend class `ControllerBase` dan memperkenalkan dua variabel konfigurasi, yaitu `model_config` dan `model_service`.

*     
    `model_config` bertanggung jawab mendefinisikan konfigurasi terkait generasi route dan schema.
    
*     
    `model_service` merujuk pada class yang digunakan untuk mengelola operasi CRUD (Create, Read, Update, Delete) untuk model yang ditentukan.

  
Sebagai contoh, perhatikan model `Event` yang didefinisikan di Django:

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
    

  
Sekarang, mari kita buat sebuah `ModelController` untuk model `Event`. Di file `api.py`, kita mendefinisikan sebuah `EventModelController`:

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
    

  
Perhatikan bahwa model controller bergantung pada package `ninja-schema` untuk generasi schema otomatis. Untuk menginstall package tersebut, gunakan perintah berikut:

    pip install ninja-schema
    

  
Setelah instalasi, Anda dapat mengakses dokumentasi API yang dihasilkan secara otomatis dengan mengunjungi http://localhost:8000/api/docs.

  
Dokumen ini memberikan gambaran detail tentang route, schema, dan fitur yang diekspos oleh `EventModelController` untuk model `Event`.

**Konfigurasi Model**
-----------------------

  
`ModelConfig` adalah sebuah Pydantic schema yang digunakan untuk memvalidasi dan mengonfigurasi perilaku model controller. Opsi konfigurasi utama meliputi:

*     
    Model: Field yang wajib yang merepresentasikan tipe model Django yang terkait dengan Model Controller.
    
*     
    async_routes: Menunjukkan apakah route controller sebaiknya dibuat sebagai fungsi route `asynchronous`.
    
*     
    allowed_routes: List yang menentukan operasi API yang diizinkan untuk dihasilkan di Model Controller. Nilai defaultnya adalah `["create", "find_one", "update", "patch", "delete", "list"]`.
    
*     
    create_schema: Pydantic schema opsional yang menguraikan tipe input data untuk operasi `create` atau `POST` di model controller. Nilai defaultnya adalah `None`. Jika tidak disediakan, `ModelController` akan menghasilkan schema baru berdasarkan opsi `schema_config`.
    
*     
    update_schema: Pydantic schema opsional yang merinci tipe input data untuk operasi `update` atau `PUT` di model controller. Nilai defaultnya adalah `None`. Jika tidak disediakan, `create_schema` akan digunakan jika tersedia, jika tidak, schema baru akan dihasilkan berdasarkan opsi `schema_config`.
    
*     
    retrieve_schema: Pydantic schema opsional untuk output yang mendefinisikan tipe output data untuk berbagai operasi. Nilai defaultnya adalah `None`. Jika tidak disediakan, `ModelController` akan menghasilkan schema berdasarkan opsi `schema_config`.
    
*     
    patch_schema: Pydantic schema opsional untuk output yang menentukan tipe input data untuk operasi `patch/PATCH`. Nilai defaultnya adalah `None`. Jika tidak disediakan, `ModelController` akan menghasilkan schema dengan semua field bersifat opsional.
    
*     
    schema_config: Field wajib lainnya yang mendeskripsikan metode generasi schema yang dibutuhkan untuk operasi Model Controller. Opsi konfigurasinya meliputi:
    
    *     
        `include`: List field yang disertakan. Defaultnya adalah `__all__`.
        
    *     
        `exclude`: List field yang dikecualikan. Nilai defaultnya adalah `[]`.
        
    *     
        `optional`: List field yang dipaksa menjadi opsional. Nilai defaultnya adalah `[pk]`.
        
    *     
        `depth`: Kedalaman untuk generasi schema bersarang (nested).
        
    *     
        `read_only_fields`: List field yang dikecualikan saat menghasilkan input schema untuk operasi create, update, dan patch.
        
    *     
        `write_only_fields`: List field yang dikecualikan saat menghasilkan output schema untuk operasi find_one dan list.
        
    *     
        pagination: Sebuah kebutuhan bagi operasi model `list/GET` untuk mencegah pengiriman `100_000` item sekaligus dalam satu request. Konfigurasi pagination membutuhkan pengaturan objek Pydantic schema `ModelPagination`. Opsinya meliputi:
        
        *     
            `klass`: Sebuah pagination class bertipe `PaginationBase`. Nilai defaultnya adalah `PageNumberPaginationExtra`.
            
        *     
            `paginator_kwargs`: Nilai dictionary untuk inisialisasi `PaginationBase`. Nilai defaultnya adalah None.
            
        *     
            `pagination_schema`: Pydantic generic schema yang dikombinasikan dengan `retrieve_schema` untuk menghasilkan response schema bagi operasi `list/GET`.
        
          
        Sebagai contoh, jika memilih pagination `ninja` seperti `LimitOffsetPagination`:
        
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
Lebih Lanjut tentang Operasi Model Controller**
------------------

  
Pada model controller NinjaExtra, perilaku controller dapat dikendalikan melalui isi list `allowed_routes` di opsi `model_config`.

  
Sebagai contoh, Anda dapat membuat sebuah controller read-only seperti ini:

    from ninja_extra import api_controller, ModelControllerBase, ModelConfig, ModelSchemaConfig
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            allowed_routes=['find_one', 'list'],
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    

  
Ini hanya akan membuat route `GET/{id}` dan `GET/` untuk listing.

  
Anda juga dapat menambahkan lebih banyak endpoint ke sebuah `EventModelController` yang sudah ada. Misalnya:

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

  
Setiap model controller membuat sebuah instance `ModelService` saat runtime untuk mengelola interaksi antara model dan controller. Biasanya, operasi model service ini merupakan bagian dari model controller, tetapi keduanya diabstraksi menjadi sebuah service untuk memungkinkan pendekatan yang lebih dinamis.

    class ModelService(ModelServiceBase):
        """
        Model Service for Model Controller model CRUD operations with simple logic for simple models.
    
        It's advised to override this class if you have a complex model.
        """
        def __init__(self, model: Type[DjangoModel]) -> None:
            self.model = model
    
        # ... (other CRUD methods)
    

  
Operasi-operasi ini dipanggil berdasarkan operasi yang sedang berjalan pada model controller atau request yang sedang diproses oleh model controller tersebut.

### **Menggunakan Model Service Kustom**

  
Meng-override `ModelService` di sebuah model controller lebih penting daripada meng-override operasi route. `ModelService` default yang digunakan di model controller dirancang untuk model Django yang sederhana. Jika modelnya kompleks, disarankan untuk meng-override `ModelService`.

  
Sebagai contoh, jika Anda ingin mengubah cara model `Event` disimpan:

    from ninja_extra import ModelService
    
    class EventModelService(ModelService):
        def create(self, schema: PydanticModel, **kwargs: Any) -> Any:
            data = schema.dict(by_alias=True)
            data.update(kwargs)
            
            instance = self.model._default_manager.create(**data)
            return instance
    
            
    

  
Kemudian di `api.py`

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
    

### **Mengaktifkan Route Async**

  
Di `model_config`, atur `async_routes` menjadi `True`

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
    

  
Dengan mengatur parameter `async_routes` menjadi `True` di `model_config`, `ModelController` secara dinamis berpindah antara `ModelAsyncEndpointFactory` dan `ModelEndpointFactory` berdasarkan konfigurasi untuk menghasilkan endpoint async atau sync.

### **Model Controller dan Model Service Bersama**

  
Jika diperlukan, controller dan model service juga dapat digabungkan menjadi satu:

  
Sebagai contoh, menggunakan `EventModelService` yang telah kita buat

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

  
`ModelEndpointFactory` adalah factory class yang digunakan oleh model controller untuk menghasilkan endpoint secara mulus. Ia juga dapat digunakan langsung di controller NinjaExtra mana pun untuk tujuan yang sama.

  
Sebagai contoh, jika kita ingin menambahkan sebuah `Event` ke `Category` baru, dapat dilakukan sebagai berikut:

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
    

  
Pada contoh di atas, kita menggunakan `ModelEndpointFactory.create` untuk membuat endpoint `POST /{int:event_id}/new-category`, dengan memberikan input dan output schema beserta sebuah custom handler. Dengan memberikan `custom_handler`, fungsi route yang dihasilkan akan mendelegasikan operasi penanganannya ke `custom_handler` yang diberikan, alih-alih memanggil `service.create`.

**  
Async Model Endpoint Factory**
---------------

  
`ModelAsyncEndpointFactory` memiliki antarmuka API yang sama dengan `ModelEndpointFactory`, tetapi secara khusus dirancang untuk menghasilkan endpoint async.

  
Kita dapat membuat contoh yang sama seperti dengan `ModelEndpointFactory`

Sebagai contoh:

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
    

  
Pada ilustrasi di atas, kita membuat `add_event_to_new_category` sebagai fungsi async dan juga mengonversi `handle_add_event_to_new_category` menjadi fungsi async.

**QueryGetter dan ObjectGetter**
--------------------------------

  
`ModelEndpointFactory` mengekspos cara yang lebih fleksibel untuk mengambil objek model atau filter queryset, masing-masing untuk kasus `ModelEndpointFactory.find_one` dan `ModelEndpointFactory.list`.

  
Sebagai contoh, mengambil kategori dari sebuah event (tidak praktis, tetapi untuk ilustrasi):

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
    

  
Pada contoh di atas, kita menggunakan `ModelEndpointFactory.find_one` untuk membuat endpoint `get_event_category` dan menyediakan `object_getter` sebagai callback untuk mengambil model berdasarkan `event_id`. `lookup_param` menunjukkan key di `kwargs` yang digunakan untuk mendefinisikan nilai pk bagi pengambilan objek model, jika tidak ada handler `object_getter` yang diimplementasikan.

  
Di sisi lain, Anda mungkin menemui situasi di mana Anda perlu melakukan listing event berdasarkan `category_id`:

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
    

  
Dengan menggunakan `ModelEndpointFactory.list` beserta `queryset_getter`, Anda dapat dengan cepat menyiapkan endpoint list yang mengembalikan event-event yang termasuk dalam sebuah kategori. Perhatikan bahwa jika ID yang tidak valid diberikan, `queryset_getter` kami mungkin gagal karena ini hanyalah sebuah contoh.

  
Selain itu, perlu diingat bahwa setelah ModelConfig diinstansiasi, pengaturan-pengaturan seperti `model_config` tetap dapat digunakan, seperti `create_schema`, `retrieve_schema`, `patch_schema`, dan `update_schema`.

**  
Parameter Path dan Query**
--------------

  
Di `ModelEndpointFactory`, parameter path diparsing untuk mengidentifikasi parameter `path` dan `query`. Parameter-parameter ini kemudian dibuat sebagai field di input schema Ninja dan diparsing selama request, lalu diteruskan sebagai kwargs ke handler.

Sebagai contoh,

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
    

  
Pada contoh ini, path `/{int:id}/tags/{post_id}?query=int&query1=int` menghasilkan dua parameter path `['id:int', 'post_id:str']` dan dua parameter query `['query:int', 'query1:int']`. Parameter-parameter ini dikemas ke dalam input schema Ninja dan diparsing selama request, lalu diteruskan sebagai kwargs ke route handler.

  
Perhatikan bahwa ketika parameter `path` dan `query` didefinisikan, parameter tersebut ditambahkan sebagai field yang wajib ke input schema ninja, bukan opsional. Selain itu, tipe data path dan query harus kompatibel dengan Django URL converters.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
