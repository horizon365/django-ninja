依赖注入
=====

  
Django Ninja Extra APIController 的核心功能之一是使用 Injector 支持依赖注入

  
例如，如果您有一个名为 AuthService 的服务，并且想在您的 `UsersController` 类中使用它，您可以在类的构造函数中简单地将其添加为参数，并使用其类型进行注释。

    class UsersController(ControllerBase):
        def __init__(self, auth_service: AuthService):
            self.auth_service = auth_service
    

  
然后在你的应用程序配置中，你可以注册这个服务及其作用域。默认情况下，服务是单例作用域，除非指定。

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    

  
您还可以指定服务的范围。当您希望为不同的请求使用同一服务的不同实例时，这很有用。

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=noscope)
    

  
这样，您就可以轻松地将服务注入到控制器中，并在整个应用程序中使用它们。这使得测试控制器以及在不影响应用程序其他部分的情况下更改服务的实现变得容易。

  
!!! 信息 Django-Ninja-Extra 支持 django_injector。无需额外配置。

Creating a Service
------------------

  
服务是指可以在应用程序的不同部分重复使用的自包含模块或功能部分。服务通常用于封装业务逻辑或提供对共享资源（如数据库或外部 API）的访问。服务通常实现为类，并且可以通过面向对象的接口进行访问。服务可以用于执行操作、与外部系统交互和执行计算。它们通常具有一些公共方法和属性，允许其他对象与之交互。服务通常用于将应用程序逻辑与基础结构分离，这样应用程序逻辑就可以独立地被重用、测试和维护。

  
让我们创建一个简单的 S3 存储桶服务，在您的项目中创建一个 `service.py` ，并添加以下内容

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

  
在 Python Injector 中，模块是一个类或函数，用于配置依赖注入容器。模块负责将服务绑定到它们的实现，并配置服务的作用域。

  
一个模块可以定义一个 `configure(binder: Binder)` 函数，用于配置依赖注入容器。 `binder` 参数是 Binder 类的一个实例，用于将服务绑定到它们的实现。

  
一个模块还可以定义一个或多个提供程序函数，这些函数用于创建服务的实例。这些函数可以使用 `@inject` 进行修饰，以指定它们需要解析的依赖项，还可以使用 `@provider` 进行修饰，以指示它们应该用于创建服务的实例。

For example:

    from injector import Binder, singleton, inject, provider
    
    class MyModule:
        def configure(self, binder: Binder) -> Binder:
            binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    
        @provider
        @inject
        def provide_user_service(self, auth_service: AuthService) -> UserService:
            return UserService(auth_service)
    

  
在上面的示例中， `MyModule` 类有 `configure` 方法，用于绑定 `AuthService` 并将作用域设置为 `singleton` 和 `provide_user_service` ，该作用域被 `@provider` 和 `@inject` 修饰，以提供 `UserService` ，并且 `AuthService` 被注入为依赖项。

  
通过在 Ninja Extra 设置中注册一个模块，该模块中定义的所有服务、提供程序和配置都将被添加到 Injector 中，并且这些服务可以在整个应用程序中被解析和使用。

  
让我们为之前创建的 `BucketFileUpload` 服务创建一个模块。在你的项目中创建一个 `module.py` ，并添加以下代码。

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
    

  
我们创建了一个 `FileServiceModule` ，将 `BucketFileUpload` 绑定到 `InMemoryBucketFileUpload` 。在我们的应用程序中，当解析 `BucketFileUpload` 时，我们将获得 injector 为我们提供的 `InMemoryBucketFileUpload` 的实例。我们还使用了 `inject` 装饰器从 `injector` 向 `InMemoryBucketFileUpload` 服务注入 django 设置。

  
`InMemoryBucketFileUpload` 具体类是一个简单的开发类。在生产时间，你可能想编写一个更好的服务来将文件保存到你的 AWS S3 存储桶中。

Service Scope
-------------

  
范围定义了创建的服务的生命周期。在 Web 框架中使用依赖注入时有三个主要范围

### `singleton` scope

  
单例服务仅创建一次，整个应用程序的生存期内将重用同一个实例。这是未指定范围时的默认范围。

    from injector import Module, Binder, singleton
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=singleton)
    

### `transient` scope

  
每次请求都会创建一个临时服务。每个请求都会创建一个新实例。对于不维护状态的服务或不应在多个请求之间共享的服务，这很有用。

    from injector import Module, Binder, noscope
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=noscope)
    

### `scoped`

  
范围服务在每个请求中创建一次。对于每个传入请求都会创建一个新实例，并在同一请求内依赖它的所有组件之间共享。这对于维护请求特定状态的服务很有用。

  
目前，Ninja扩展不支持 `scoped` 范围服务。

  
在向依赖注入容器注册服务时，选择适当的作用域很重要。 `Singleton` 服务适用于维护应用程序范围状态的服务， `transient` 服务适用于不维护状态的服务， `scoped` 服务适用于维护请求特定状态的服务。

  
向控制器添加服务
-----------

  
Ninja额外控制器构造函数（ `__init__` ）使用来自 `injector` 库的 `inject` 函数进行装饰。这使得在构造函数中使用类型注释定义参数成为可能，并且在对象实例化期间会注入带注释的类型。

  
我们创建了一个 `BucketFileUpload` 合同和一些具体实现，让我们将其添加到控制器中。

  
让我们使用下面的代码创建一个 `controller.py`

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
    

  
现在，我们已经向 `UserProfileController` 定义了一个 `BucketFileUpload` 服务依赖。我们需要将 `FileServiceModule` 注册到设置中，以避免 Ninja 额外尝试创建对象时从注入器中获取 `UnsatisedRequirement` 异常。

**Module Registration**
-----------------------

  
在 Django 应用程序中注册注入器模块有不同的方式。

*     
    django_injector：如果你正在使用 django_inject，它有关于如何注册模块的文档。
*     
    Ninja额外功能：你可以在 `NINJA_EXTRA` 字段的 `INJECTOR_MODULES` 中提供模块字符串路径，如下所示：

###   
基于 Ninja Extra 注册

  
我们在 django 设置文件的 Ninja Extra 设置中的 `INJECTOR_MODULES` 键注册模块。

    NINJA_EXTRA = {
        'INJECTOR_MODULES': [
            'myproject.app1.modules.SomeModule',
            'myproject.app2.modules.SomeAppModule',
        ]
    }
    

  
让我们将 `FileServiceModule` 模块注册到 `NinjaExtra` 设置中

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
    

  
就是这样。我们已经将 `BucketFileUpload` 服务完全有线连接到 `UserProfileController` 。

  
!!! 警告 您不仅可以使用没有注释的参数覆盖您的 APIController 构造函数 更多 Python 注入器

Using `service_resolver`
------------------------

  
`service_resolver` 是一个实用类，用于解析在 `injector` 实例中注册的类型。当我们需要在控制器外部解析服务时，可以使用它。

For example:

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service = service_resolver(BucketFileUpload)
    bucket_service.upload_file_to_s3('/path/to/file')
    

  
我们也可以一次解决多个服务，并且会返回一个元组结果。

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service, service_a, service_b = service_resolver(BucketFileUpload, AnotherServiceA, AnotherServiceB)
    bucket_service.upload_file_to_s3('/path/to/file')
    
    service_a.do_something()
    service_b.do_something()
    
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
