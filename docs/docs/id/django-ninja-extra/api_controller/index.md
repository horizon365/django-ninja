**Controller**
==============

  
API controller Ninja-Extra bertanggung jawab untuk menangani request yang masuk dan mengembalikan respons kepada client.

  
Di Ninja-Extra, terdapat beberapa komponen utama untuk membuat model controller:

*   ControllerBase
*   Decorator APIController

ControllerBase
--------------

  
Class `ControllerBase` adalah base class untuk semua controller di Django Ninja Extra. Ia menyediakan fungsionalitas inti untuk menangani request, memvalidasi input, dan mengembalikan respons dengan cara class-based.

  
Class ini mencakup atribut dan metode yang umum untuk semua controller, seperti objek `request`, `permission_classes`, dan objek `response`, yang merupakan bagian dari `RouteContext`. Objek request berisi informasi tentang request yang masuk, seperti headers, query parameters, dan body data. Atribut permission_classes digunakan untuk mendefinisikan permission yang dibutuhkan untuk mengakses route milik controller, sedangkan objek response digunakan untuk membangun respons akhir yang dikembalikan kepada client.

  
Selain atribut inti, class `ControllerBase` juga berisi utility methods yang dapat digunakan untuk menangani tugas-tugas umum seperti pemeriksaan permission objek (`check_object_permission`), membuat respons cepat (`create_response`), dan mengambil data dari database (`get_object_or_exception`). Metode-metode ini dapat di-override di subclass untuk memberikan perilaku kustom.

  
Base class controller juga menyertakan sistem dependency injection yang memungkinkan akses mudah ke service dan objek lain di aplikasi, seperti repository services.

    from ninja_extra import ControllerBase, api_controller
    
    @api_controller('/users')
    class UserControllerBase(ControllerBase):
        ...
    

Decorator APIController
------------------

  
Decorator `api_controller` digunakan untuk mendefinisikan controller class-based di Django Ninja Extra. Ia diterapkan pada class ControllerBase dan menerima beberapa parameter untuk mengonfigurasi routing dan fungsionalitas controller.

  
Parameter pertama, `prefix_or_class`, adalah string prefix untuk semua route yang terdaftar di bawah controller yang dikelompokkan, atau objek class yang diterapkan decorator tersebut.

  
Parameter kedua, `auth`, adalah list yang berisi semua class Auth Django Ninja yang sebaiknya diterapkan pada route milik controller.

  
Parameter ketiga, `tags`, adalah list berisi string yang digunakan untuk keperluan tagging OPENAPI.

  
Parameter keempat, `permissions`, adalah list yang berisi semua permission yang sebaiknya diterapkan pada route milik controller.

  
Parameter kelima, `auto_import`, secara default bernilai true dan otomatis menambahkan controller Anda ke daftar auto-import.

sebagai contoh:

    import typing
    from ninja_extra import api_controller, ControllerBase, permissions, route
    from django.contrib.auth.models import User
    from ninja.security import APIKeyQuery
    from ninja import ModelSchema
    
    
    class UserSchema(ModelSchema):
        class Config:
            model = User
            model_fields = ['username', 'email', 'first_name']
    
    
    @api_controller('users/', auth=[APIKeyQuery()], permissions=[permissions.IsAuthenticated])
    class UsersController(ControllerBase):
        @route.get('', response={200: typing.List[UserSchema]})
        def get_users(self):
            # Logic to handle GET request to the /users endpoint
            users = User.objects.all()
            return users
    
        @route.post('create/', response={200: UserSchema})
        def create_user(self, payload: UserSchema):
            # Logic to handle POST request to the /users endpoint
            new_user = User.objects.create(
                username=payload.username,
                email=payload.email,
                first_name=payload.first_name,
            )
            new_user.set_password('password')
            return new_user
    

  
Pada kode di atas, kita mendefinisikan sebuah controller bernama `UsersController` menggunakan decorator `api_controller`. Decorator tersebut diterapkan pada class dan menerima dua argumen, yaitu endpoint URL `/users` serta class `auth` dan `permission`. `get_users` dan `create_user` adalah fungsi route yang menangani request GET `/users` dan POST `/users/create` yang masuk.

  
!!!info Mewarisi class ControllerBase memberi Anda dukungan IDE IntelliSense yang lebih baik.

Contoh Cepat
-------------

  
Mari kita buat sebuah APIController untuk mengelola model user Django dengan benar

    import uuid
    from ninja import ModelSchema
    from ninja_extra import (
        http_get, http_post, http_generic, http_delete,
        api_controller, status, ControllerBase, pagination
    )
    from ninja_extra.controllers.response import Detail
    from django.contrib.auth import get_user_model
    
    
    class UserSchema(ModelSchema):
        class Config:
            model = get_user_model()
            model_fields = ['username', 'email', 'first_name']
    
    
    @api_controller('/users')
    class UsersController(ControllerBase):
        user_model = get_user_model()
    
        @http_post()
        def create_user(self, user: UserSchema):
            # just simulating created user
            return dict(id=uuid.uuid4())
    
        @http_generic('/{int:user_id}', methods=['put', 'patch'], response=UserSchema)
        def update_user(self, user_id: int):
            """ Django Ninja will serialize Django ORM model to schema provided as `response`"""
            user = self.get_object_or_exception(self.user_model, id=user_id)
            return user
    
        @http_delete('/{int:user_id}', response=Detail(status_code=status.HTTP_204_NO_CONTENT))
        def delete_user(self, user_id: int):
            user = self.get_object_or_exception(self.user_model, id=user_id)
            user.delete()
            return self.create_response('', status_code=status.HTTP_204_NO_CONTENT)
    
        @http_get("", response=pagination.PaginatedResponseSchema[UserSchema])
        @pagination.paginate(pagination.PageNumberPaginationExtra, page_size=50)
        def list_user(self):
            return self.user_model.objects.all()
    
        @http_get('/{user_id}', response=UserSchema)
        def get_user_by_id(self, user_id: int):
            user = self.get_object_or_exception(self.user_model, id=user_id)
            return user
    

  
Pada contoh di atas, class `UsersController` mendefinisikan beberapa metode yang sesuai dengan HTTP method yang berbeda, seperti `create_user`, `update_user`, `delete_user`, `list_user`, dan `get_user_by_id`. Metode-metode ini didekorasi dengan decorator `http_post`, `http_generic`, `http_delete`, dan `http_get` masing-masing.

  
Metode `create_user` menggunakan decorator `http_post` dan menerima parameter user bertipe `UserSchema`, yang merupakan `ModelSchema` yang digunakan untuk memvalidasi dan menserialisasi data input. Metode ini digunakan untuk membuat user baru di sistem dan mengembalikan `ID` user tersebut.

  
Metode `update_user` menggunakan decorator `http_generic` dan menerima parameter `user_id` bertipe int. Decorator tersebut dikonfigurasi untuk menangani metode `PUT` dan `PATCH` serta menyediakan parameter response bertipe `UserSchema` yang digunakan untuk menserialisasi objek user.

  
Metode `delete_user` menggunakan decorator `http_delete` dan menerima parameter `user_id` bertipe int dan parameter response bertipe Detail, yang akan mengembalikan status code 204 dengan body kosong jika berhasil.

  
Metode `list_user` menggunakan decorator `http_get` dan didekorasi dengan decorator `pagination.paginate`, yang menggunakan class `PageNumberPaginationExtra` untuk memaginasi hasil metode tersebut dengan 50 hasil per halaman. Ia juga menyediakan parameter response bertipe `pagination.PaginatedResponseSchema[UserSchema]`, yang akan digunakan untuk menserialisasi dan memaginasi list user yang dikembalikan oleh metode tersebut.

  
Metode `get_user_by_id` menggunakan decorator `http_get` dan menerima parameter `user_id` bertipe int dan parameter response bertipe UserSchema, yang akan digunakan untuk menserialisasi objek user.

  
Controller user juga menggunakan `self.get_object_or_exception(self.user_model, id=user_id)`, sebuah helper method yang memunculkan exception jika objek user tidak dapat ditemukan.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
