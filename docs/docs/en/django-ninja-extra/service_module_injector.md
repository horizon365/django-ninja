Dependency Injection
=====

  
One of the core features of the Django Ninja Extra APIController is the support for dependency injection using Injector.

  
For example, if you have a service called AuthService and want to use it in your `UsersController` class, you can simply add it as a parameter in the class constructor and annotate it with its type.

    class UsersController(ControllerBase):
        def __init__(self, auth_service: AuthService):
            self.auth_service = auth_service
    

  
Then in your application configuration, you can register this service and its scope. By default, services are singleton scoped unless specified.

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    

  
You can also specify the scope of the service. This is useful when you want to use different instances of the same service for different requests.

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=noscope)
    

  
This way, you can easily inject services into controllers and use them throughout the application. This makes it easy to test controllers and change service implementations without affecting other parts of the application.

  
!!! info Django-Ninja-Extra supports django_injector. No additional configuration is required.

Creating a Service
------------------

  
A service is a self-contained module or functional unit that can be reused across different parts of an application. Services are typically used to encapsulate business logic or provide access to shared resources (such as databases or external APIs). Services are usually implemented as classes and can be accessed through an object-oriented interface. Services can be used to perform operations, interact with external systems, and perform computations. They typically have some public methods and properties that allow other objects to interact with them. Services are commonly used to separate application logic from infrastructure, so that application logic can be independently reused, tested, and maintained.

  
Let's create a simple S3 bucket service. Create a `service.py` in your project and add the following

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
    

### Create a module

  
In Python Injector, a module is a class or function used to configure the dependency injection container. A module is responsible for binding services to their implementations and configuring the scope of services.

  
A module can define a `configure(binder: Binder)` function used to configure the dependency injection container. The `binder` parameter is an instance of the Binder class used to bind services to their implementations.

  
A module can also define one or more provider functions used to create instances of services. These functions can be decorated with `@inject` to specify the dependencies they need to resolve, and with `@provider` to indicate that they should be used to create instances of the service.

For example:

    from injector import Binder, singleton, inject, provider
    
    class MyModule:
        def configure(self, binder: Binder) -> Binder:
            binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    
        @provider
        @inject
        def provide_user_service(self, auth_service: AuthService) -> UserService:
            return UserService(auth_service)
    

  
In the above example, the `MyModule` class has a `configure` method that binds `AuthService` and sets the scope to `singleton`, and `provide_user_service`, which is decorated with `@provider` and `@inject` to provide `UserService`, with `AuthService` injected as a dependency.

  
By registering a module in the Ninja Extra settings, all services, providers, and configurations defined in that module will be added to the Injector, and these services can be resolved and used throughout the application.

  
Let's create a module for the `BucketFileUpload` service we created earlier. Create a `module.py` in your project and add the following code.

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
    

  
We created a `FileServiceModule` that binds `BucketFileUpload` to `InMemoryBucketFileUpload`. In our application, when resolving `BucketFileUpload`, we will get an instance of `InMemoryBucketFileUpload` provided by the injector. We also used the `inject` decorator to inject django settings into the `InMemoryBucketFileUpload` service from the `injector`.

  
The `InMemoryBucketFileUpload` concrete class is a simple development class. In production, you may want to write a better service to save files to your AWS S3 bucket.

Service Scope
-------------

  
Scope defines the lifecycle of created services. There are three main scopes when using dependency injection in web frameworks.

### `singleton` scope

  
A singleton service is created only once, and the same instance is reused throughout the lifetime of the entire application. This is the default scope when no scope is specified.

    from injector import Module, Binder, singleton
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=singleton)
    

### `transient` scope

  
A transient service is created on every request. Each request creates a new instance. This is useful for services that do not maintain state or should not be shared across multiple requests.

    from injector import Module, Binder, noscope
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=noscope)
    

### `scoped`

  
A scoped service is created once per request. A new instance is created for each incoming request and shared among all components that depend on it within the same request. This is useful for services that maintain request-specific state.

  
Currently, Ninja Extra does not support `scoped` scope services.

  
When registering services with the dependency injection container, choosing the appropriate scope is important. `Singleton` services are suitable for services that maintain application-wide state, `transient` services are suitable for services that do not maintain state, and `scoped` services are suitable for services that maintain request-specific state.

  
Adding Services to Controllers
-----------

  
The Ninja Extra controller constructor (`__init__`) is decorated with the `inject` function from the `injector` library. This makes it possible to define parameters with type annotations in the constructor, and the annotated types will be injected during object instantiation.

  
We have created a `BucketFileUpload` contract and some concrete implementations, let's add it to a controller.

  
Let's create a `controller.py` with the following code

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
    

  
Now, we have defined a `BucketFileUpload` service dependency for the `UserProfileController`. We need to register the `FileServiceModule` to the settings to avoid an `UnsatisfiedRequirement` exception from the injector when Ninja Extra tries to create the object.

**Module Registration**
-----------------------

  
There are different ways to register injector modules in a Django application.

*     
    django_injector: If you are using django_injector, it has documentation on how to register modules.
*     
    Ninja Extra: You can provide module string paths in `INJECTOR_MODULES` within the `NINJA_EXTRA` field, as shown below:

###   
Ninja Extra-based Registration

  
We register modules in the `INJECTOR_MODULES` key within the Ninja Extra settings in the django settings file.

    NINJA_EXTRA = {
        'INJECTOR_MODULES': [
            'myproject.app1.modules.SomeModule',
            'myproject.app2.modules.SomeAppModule',
        ]
    }
    

  
Let's register the `FileServiceModule` module in the `NinjaExtra` settings

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
    

  
That's it. We have fully wired the `BucketFileUpload` service to the `UserProfileController`.

  
!!! warning You can also override your APIController constructor with parameters that are not annotated. More on Python Injector

Using `service_resolver`
------------------------

  
`service_resolver` is a utility class used to resolve types registered in the `injector` instance. We can use it when we need to resolve services outside of a controller.

For example:

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service = service_resolver(BucketFileUpload)
    bucket_service.upload_file_to_s3('/path/to/file')
    

  
We can also resolve multiple services at once, and a tuple result will be returned.

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service, service_a, service_b = service_resolver(BucketFileUpload, AnotherServiceA, AnotherServiceB)
    bucket_service.upload_file_to_s3('/path/to/file')
    
    service_a.do_something()
    service_b.do_something()
    
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
