  
Django Ninja Extra menyediakan objek RouteContext, yang tersedia di seluruh siklus hidup request. Objek ini menyimpan atribut-atribut penting bagi route handler yang akan memproses request. Atribut-atribut tersebut mencakup objek `HttpRequest` Django, list dari permission classes untuk route handler, objek response sementara yang digunakan Django-Ninja untuk membangun respons akhir, serta kwargs dan args yang dibutuhkan untuk memanggil fungsi route.

  
Perhatikan bahwa atribut-atribut ini tidak diatur pada awal request, tetapi menjadi tersedia seiring request berjalan melalui berbagai tahap, sebelum mencapai eksekusi fungsi route.

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
    

Cara Mengakses `RouteContext`
--------------------

  
Di Django Ninja Extra, objek `RouteContext` dapat diakses di class controller menggunakan atribut `self.context`. Atribut ini tersedia di level instance dari class controller, sehingga memudahkan akses ke atribut dan metode dari objek `RouteContext`.

Sebagai contoh.

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
    

  
Pada contoh ini, kita dapat mengakses objek `user` yang terautentikasi dari atribut `self.context` milik objek request, yang tersedia di class controller. Ini memungkinkan kita mengakses informasi user yang terautentikasi dengan mudah.

###   
Menggunakan RouteContext untuk Memodifikasi Response Headers

  
Objek `RouteContext` menyediakan atribut dan metode yang dibutuhkan untuk memanipulasi data response sebelum dikembalikan kepada client. Melalui objek RouteContext, Anda dapat dengan mudah memodifikasi data headers, status, atau cookie dalam response yang dikembalikan untuk request tertentu.

  
Sebagai contoh, mari tambahkan informasi `header` tambahan di endpoint baru, seperti yang ditunjukkan di bawah ini.

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
    

Menggunakan `RouteContext` di Schema
----------------------

  
Selama validasi schema, dapat muncul situasi di mana Anda perlu mengakses objek request. Django Ninja Extra mempermudah hal ini dengan menyediakan cara untuk me-resolve objek `RouteContext` selama request, yang kemudian dapat digunakan untuk mengakses objek request dan atribut lain yang diperlukan. Ini memungkinkan konteks request digunakan selama proses validasi, membuatnya lebih fleksibel dan powerful.

Sebagai contoh:

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
    

  
Pada contoh di atas, kita menggunakan `service_resolver`, sebuah fungsi utilitas dependency injection, untuk me-resolve objek `RouteContext`. Ini memungkinkan kita mengakses objek request, yang kita gunakan untuk membangun URL lengkap bagi detail toko. Dengan menggunakan `service_resolver` untuk mengakses route context, kita dapat dengan mudah mengakses objek request dan menggunakannya untuk mengumpulkan informasi yang diperlukan selama proses validasi.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
