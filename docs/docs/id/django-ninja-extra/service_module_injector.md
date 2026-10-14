Injeksi Dependensi
=====

  
Salah satu fitur utama dari APIController Django Ninja Extra adalah dukungan untuk dependency injection menggunakan Injector.

  
Sebagai contoh, jika Anda memiliki sebuah service bernama AuthService dan ingin menggunakannya di dalam kelas `UsersController` Anda, Anda cukup menambahkannya sebagai parameter di konstruktor kelas dan menganotasinya dengan tipenya.

    class UsersController(ControllerBase):
        def __init__(self, auth_service: AuthService):
            self.auth_service = auth_service
    

  
Kemudian dalam konfigurasi aplikasi Anda, Anda dapat mendaftarkan service tersebut beserta scope-nya. Secara default, service memiliki scope singleton kecuali ditentukan lain.

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    

  
Anda juga dapat menentukan scope dari service. Ini berguna ketika Anda ingin menggunakan instance yang berbeda dari service yang sama untuk request yang berbeda.

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=noscope)
    

  
Dengan cara ini, Anda dapat dengan mudah meng-inject service ke dalam controller dan menggunakannya di seluruh aplikasi. Hal ini memudahkan pengujian controller dan penggantian implementasi service tanpa memengaruhi bagian lain dari aplikasi.

  
!!! info Django-Ninja-Extra mendukung django_injector. Tidak diperlukan konfigurasi tambahan.

Membuat Service
------------------

  
Service adalah modul atau unit fungsional yang mandiri dan dapat digunakan kembali di berbagai bagian aplikasi. Service biasanya digunakan untuk mengenkapsulasi business logic atau menyediakan akses ke sumber daya bersama (seperti database atau API eksternal). Service umumnya diimplementasikan sebagai kelas dan dapat diakses melalui antarmuka berorientasi objek. Service dapat digunakan untuk melakukan operasi, berinteraksi dengan sistem eksternal, dan melakukan komputasi. Service biasanya memiliki beberapa method dan properti publik yang memungkinkan objek lain berinteraksi dengannya. Service umumnya digunakan untuk memisahkan logika aplikasi dari infrastruktur, sehingga logika aplikasi dapat digunakan kembali, diuji, dan dipelihara secara independen.

  
Mari kita buat sebuah service bucket S3 sederhana. Buat `service.py` di proyek Anda dan tambahkan kode berikut

    from ninja import File
    from ninja.files import UploadedFile
    from ninja_extra import NinjaExtraAPI, api_controller, http_post
    
    class BucketFileUploadService:
        def upload_file_to_s3(self, file, bucket_name=None, acl="public-read", file_key=None):
            pass
    
        def upload_existing_file_to_s3(
                self, filepath, file_key, bucket_name=None, acl="public-read", delete_file_afterwards=False,
                clean_up_root_limit=None
        ):
            pass
    
    
    @api_controller('/user_profile')
    class UserProfileController:
        def __init__(self, upload_service: BucketFileUploadService):
            self.upload_service = upload_service
        
        @http_post('/upload')
        def upload_profile_pic(self, file: UploadedFile = File(...)):
            self.upload_service.upload_file_to_s3(file=file)
            return {'message', 'uploaded successfully'}
    
    
    api = NinjaExtraAPI(title='Injector Test')
    api.register_controllers(UserProfileController)
    

### Membuat module

  
Dalam Python Injector, module adalah kelas atau fungsi yang digunakan untuk mengonfigurasi container dependency injection. Module bertanggung jawab untuk mengikat service ke implementasinya dan mengonfigurasi scope dari service.

  
Sebuah module dapat mendefinisikan fungsi `configure(binder: Binder)` yang digunakan untuk mengonfigurasi container dependency injection. Parameter `binder` adalah instance dari kelas Binder yang digunakan untuk mengikat service ke implementasinya.

  
Sebuah module juga dapat mendefinisikan satu atau lebih fungsi provider yang digunakan untuk membuat instance service. Fungsi-fungsi ini dapat didekorasi dengan `@inject` untuk menentukan dependensi yang perlu di-resolve, dan dengan `@provider` untuk menandakan bahwa fungsi tersebut harus digunakan untuk membuat instance service.

Sebagai contoh:

    from injector import Binder, singleton, inject, provider
    
    class MyModule:
        def configure(self, binder: Binder) -> Binder:
            binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    
        @provider
        @inject
        def provide_user_service(self, auth_service: AuthService) -> UserService:
            return UserService(auth_service)
    

  
Pada contoh di atas, kelas `MyModule` memiliki method `configure` yang mengikat `AuthService` dan mengatur scope menjadi `singleton`, serta `provide_user_service`, yang didekorasi dengan `@provider` dan `@inject` untuk menyediakan `UserService`, dengan `AuthService` di-inject sebagai dependensi.

  
Dengan mendaftarkan module di pengaturan Ninja Extra, semua service, provider, dan konfigurasi yang didefinisikan dalam module tersebut akan ditambahkan ke Injector, dan service-service ini dapat di-resolve dan digunakan di seluruh aplikasi.

  
Mari kita buat module untuk service `BucketFileUpload` yang telah kita buat sebelumnya. Buat `module.py` di proyek Anda dan tambahkan kode berikut.

    import logging
    import os
    
    from typing import cast
    from django.conf import Settings
    from injector import inject, Module, Binder, singleton
    
    logger = logging.getLogger()
    
    class InMemoryBucketFileUpload(BucketFileUpload):
        @inject
        def __init__(self, settings: Settings):
            logger.info(f"===== Using InMemoryBucketFileUpload =======")
            self.settings = settings
            assert isinstance(self.settings, Settings)
    
        def upload_file_to_s3(self, file, bucket_name=None, acl="public-read", file_key=None):
            logger.info(
                f"InMemoryBucketFileUpload ---- "
                f"upload_file_to_s3(file={file.filename}, bucket_name{bucket_name}, acl={acl}, file_key={file_key})"
            )
            if not file_key:
                return os.path.join(self.settings.UPLOAD_FOLDER, file.filename)
            return os.path.join(self.settings.BASE_DIR, file_key)
    
        def upload_existing_file_to_s3(self, filepath, file_key, bucket_name=None, acl="public-read",
                                       delete_file_afterwards=False, clean_up_root_limit=None):
            logger.info(f"InMemoryBucketFileUpload ---- upload_existing_file_to_s3("
                        f"filepath={filepath}, file_key={file_key}, "
                        f"bucket_name={bucket_name}, acl={acl}, delete_file_afterwards={delete_file_afterwards})")
            return filepath
    
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=singleton)
    

  
Kami membuat `FileServiceModule` yang mengikat `BucketFileUpload` ke `InMemoryBucketFileUpload`. Di aplikasi kami, ketika melakukan resolve `BucketFileUpload`, kami akan mendapatkan instance `InMemoryBucketFileUpload` yang disediakan oleh injector. Kami juga menggunakan dekorator `inject` untuk meng-inject django settings ke dalam service `InMemoryBucketFileUpload` dari `injector`.

  
Kelas konkret `InMemoryBucketFileUpload` adalah kelas sederhana untuk keperluan pengembangan. Di production, Anda mungkin ingin menulis service yang lebih baik untuk menyimpan file ke bucket AWS S3 Anda.

Scope Service
-------------

  
Scope mendefinisikan lifecycle dari service yang dibuat. Ada tiga scope utama ketika menggunakan dependency injection dalam web framework.

### `singleton` scope

  
Service singleton hanya dibuat satu kali, dan instance yang sama digunakan kembali selama masa hidup seluruh aplikasi. Ini adalah scope default ketika tidak ada scope yang ditentukan.

    from injector import Module, Binder, singleton
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=singleton)
    

### `transient` scope

  
Service transient dibuat pada setiap request. Setiap request membuat instance baru. Ini berguna untuk service yang tidak menyimpan state atau tidak boleh dibagikan di antara beberapa request.

    from injector import Module, Binder, noscope
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=noscope)
    

### `scoped`

  
Service scoped dibuat satu kali per request. Instance baru dibuat untuk setiap request yang masuk dan dibagikan di antara semua komponen yang bergantung padanya dalam request yang sama. Ini berguna untuk service yang menyimpan state spesifik request.

  
Saat ini, Ninja Extra belum mendukung service dengan scope `scoped`.

  
Saat mendaftarkan service ke dalam container dependency injection, pemilihan scope yang tepat sangatlah penting. Service `Singleton` cocok untuk service yang menyimpan state di tingkat aplikasi, service `transient` cocok untuk service yang tidak menyimpan state, dan service `scoped` cocok untuk service yang menyimpan state spesifik request.

  
Menambahkan Service ke Controller
-----------

  
Konstruktor controller Ninja Extra (`__init__`) didekorasi dengan fungsi `inject` dari library `injector`. Hal ini memungkinkan pendefinisian parameter dengan anotasi tipe di konstruktor, dan tipe yang dianotasi tersebut akan di-inject saat objek dibuat.

  
Kami telah membuat kontrak `BucketFileUpload` beserta beberapa implementasi konkretnya, mari kita tambahkan ke sebuah controller.

  
Mari kita buat `controller.py` dengan kode berikut

    from ninja import File
    from ninja.files import UploadedFile
    from ninja_extra import NinjaExtraAPI, api_controller, http_post
    from .modules import BucketFileUpload, InMemoryBucketFileUpload
    
    @api_controller('/user_profile')
    class UserProfileController:
        def __init__(self, upload_service: BucketFileUpload):
            self.upload_service = upload_service
        
        @http_post('/upload')
        def upload_profile_pic(self, file: UploadedFile = File(...)):
            self.upload_service.upload_file_to_s3(file=file)
            assert isinstance(self.upload_service, InMemoryBucketFileUpload) # True
            return {'message', 'uploaded successfully'}
    
    
    api = NinjaExtraAPI(title='Injector Test')
    api.register_controllers(UserProfileController)
    

  
Sekarang, kami telah mendefinisikan dependensi service `BucketFileUpload` untuk `UserProfileController`. Kita perlu mendaftarkan `FileServiceModule` ke pengaturan untuk menghindari exception `UnsatisfiedRequirement` dari injector ketika Ninja Extra mencoba membuat objek tersebut.

**Registrasi Module**
-----------------------

  
Ada beberapa cara untuk mendaftarkan module injector di aplikasi Django.

*     
    django_injector: Jika Anda menggunakan django_injector, tersedia dokumentasi tentang cara mendaftarkan module.
*     
    Ninja Extra: Anda dapat menyediakan path module dalam bentuk string di `INJECTOR_MODULES` di dalam field `NINJA_EXTRA`, seperti yang ditunjukkan di bawah ini:

###   
Registrasi Berbasis Ninja Extra

  
Kami mendaftarkan module di key `INJECTOR_MODULES` di dalam pengaturan Ninja Extra pada file django settings.

    NINJA_EXTRA = {
        'INJECTOR_MODULES': [
            'myproject.app1.modules.SomeModule',
            'myproject.app2.modules.SomeAppModule',
        ]
    }
    

  
Mari kita daftarkan module `FileServiceModule` di pengaturan `NinjaExtra`

    # settings.py
    ...
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    NinjaExtra = {
        'INJECTOR_MODULES': [
            'myproject.modules.FileServiceModule'
        ]
    }
    ...
    

  
Selesai. Kami telah menghubungkan service `BucketFileUpload` secara lengkap ke `UserProfileController`.

  
!!! warning Anda juga dapat meng-override konstruktor APIController Anda dengan parameter yang tidak dianotasi. Selengkapnya tentang Python Injector

Menggunakan `service_resolver`
------------------------

  
`service_resolver` adalah kelas utilitas yang digunakan untuk melakukan resolve terhadap tipe-tipe yang terdaftar dalam instance `injector`. Kita dapat menggunakannya ketika perlu melakukan resolve service di luar controller.

Sebagai contoh:

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service = service_resolver(BucketFileUpload)
    bucket_service.upload_file_to_s3('/path/to/file')
    

  
Kita juga dapat melakukan resolve beberapa service sekaligus, dan hasilnya akan dikembalikan dalam bentuk tuple.

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service, service_a, service_b = service_resolver(BucketFileUpload, AnotherServiceA, AnotherServiceB)
    bucket_service.upload_file_to_s3('/path/to/file')
    
    service_a.do_something()
    service_b.do_something()
    
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
