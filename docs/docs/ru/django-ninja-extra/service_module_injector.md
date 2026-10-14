Внедрение зависимостей
=====

  
Одной из ключевых возможностей APIController в Django Ninja Extra является поддержка внедрения зависимостей с использованием Injector.

  
Например, если у вас есть сервис с именем AuthService и вы хотите использовать его в своём классе `UsersController`, вы можете просто добавить его как параметр в конструктор класса и аннотировать его соответствующим типом.

    class UsersController(ControllerBase):
        def __init__(self, auth_service: AuthService):
            self.auth_service = auth_service
    

  
Затем в конфигурации вашего приложения вы можете зарегистрировать этот сервис и его область видимости (scope). По умолчанию сервисы регистрируются со scope `singleton`, если не указано иное.

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    

  
Вы также можете указать область видимости (scope) сервиса. Это полезно, когда вы хотите использовать разные экземпляры одного и того же сервиса для разных запросов.

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=noscope)
    

  
Таким образом, вы можете легко внедрять сервисы в контроллеры и использовать их во всём приложении. Это упрощает тестирование контроллеров и замену реализаций сервисов без воздействия на другие части приложения.

  
!!! info Django-Ninja-Extra поддерживает django_injector. Дополнительная настройка не требуется.

Создание сервиса
------------------

  
Сервис — это автономный модуль или функциональный блок, который может повторно использоваться в разных частях приложения. Сервисы обычно используются для инкапсуляции бизнес-логики или предоставления доступа к общим ресурсам (таким как базы данных или внешние API). Сервисы, как правило, реализуются в виде классов и могут быть доступны через объектно-ориентированный интерфейс. Сервисы могут использоваться для выполнения операций, взаимодействия с внешними системами и выполнения вычислений. Обычно они имеют ряд публичных методов и свойств, которые позволяют другим объектам взаимодействовать с ними. Сервисы часто применяются для отделения логики приложения от инфраструктуры, чтобы логика приложения могла независимо использоваться повторно, тестироваться и поддерживаться.

  
Давайте создадим простой сервис для работы с S3-бакетом. Создайте файл `service.py` в своём проекте и добавьте в него следующее

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
    

### Создание модуля

  
В Python Injector модуль — это класс или функция, используемые для настройки контейнера внедрения зависимостей. Модуль отвечает за привязку сервисов к их реализациям и настройку области видимости (scope) сервисов.

  
Модуль может определять функцию `configure(binder: Binder)`, используемую для настройки контейнера внедрения зависимостей. Параметр `binder` — это экземпляр класса Binder, который используется для привязки сервисов к их реализациям.

  
Модуль также может определять одну или несколько функций-провайдеров, используемых для создания экземпляров сервисов. Эти функции могут быть декорированы с помощью `@inject`, чтобы указать зависимости, которые необходимо разрешить, и с помощью `@provider`, чтобы указать, что они должны использоваться для создания экземпляров сервиса.

Например:

    from injector import Binder, singleton, inject, provider
    
    class MyModule:
        def configure(self, binder: Binder) -> Binder:
            binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    
        @provider
        @inject
        def provide_user_service(self, auth_service: AuthService) -> UserService:
            return UserService(auth_service)
    

  
В приведённом выше примере класс `MyModule` имеет метод `configure`, который привязывает `AuthService` и устанавливает область видимости `singleton`, а также `provide_user_service`, который декорирован `@provider` и `@inject` и предоставляет `UserService` с внедрённой зависимостью `AuthService`.

  
Зарегистрировав модуль в настройках Ninja Extra, все сервисы, провайдеры и конфигурации, определённые в этом модуле, будут добавлены в Injector, и эти сервисы можно будет разрешать и использовать во всём приложении.

  
Давайте создадим модуль для сервиса `BucketFileUpload`, который мы создали ранее. Создайте файл `module.py` в своём проекте и добавьте в него следующий код.

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
    

  
Мы создали `FileServiceModule`, который привязывает `BucketFileUpload` к `InMemoryBucketFileUpload`. В нашем приложении при разрешении `BucketFileUpload` мы получим экземпляр `InMemoryBucketFileUpload`, предоставленный инжектором. Мы также использовали декоратор `inject`, чтобы внедрить настройки Django в сервис `InMemoryBucketFileUpload` из `injector`.

  
Конкретный класс `InMemoryBucketFileUpload` — это простой класс для разработки. В production-окружении вам, возможно, захочется написать более качественный сервис для сохранения файлов в ваш AWS S3-бакет.

Область видимости сервиса (Service Scope)
-------------

  
Область видимости (scope) определяет жизненный цикл создаваемых сервисов. Существует три основных области видимости при использовании внедрения зависимостей в веб-фреймворках.

### Область видимости `singleton`

  
Сервис со scope `singleton` создаётся только один раз, и один и тот же экземпляр повторно используется на протяжении всего времени жизни всего приложения. Это область видимости по умолчанию, когда scope не указан.

    from injector import Module, Binder, singleton
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=singleton)
    

### Область видимости `transient`

  
Сервис со scope `transient` создаётся при каждом запросе. Каждый запрос создаёт новый экземпляр. Это полезно для сервисов, которые не хранят состояние или не должны разделяться между несколькими запросами.

    from injector import Module, Binder, noscope
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=noscope)
    

### `scoped`

  
Сервис со scope `scoped` создаётся один раз на запрос. Новый экземпляр создаётся для каждого входящего запроса и используется совместно всеми компонентами, зависящими от него, в рамках одного запроса. Это полезно для сервисов, которые хранят состояние, специфичное для запроса.

  
В настоящее время Ninja Extra не поддерживает сервисы с областью видимости `scoped`.

  
При регистрации сервисов в контейнере внедрения зависимостей важно выбирать подходящую область видимости. Сервисы `singleton` подходят для сервисов, которые хранят состояние на уровне всего приложения, сервисы `transient` — для сервисов, которые не хранят состояние, а сервисы `scoped` — для сервисов, которые хранят состояние, специфичное для запроса.

  
Добавление сервисов в контроллеры
-----------

  
Конструктор контроллера Ninja Extra (`__init__`) декорирован функцией `inject` из библиотеки `injector`. Это позволяет определять в конструкторе параметры с аннотациями типов, и аннотированные типы будут внедрены при создании объекта.

  
Мы создали контракт `BucketFileUpload` и несколько конкретных реализаций — теперь давайте добавим его в контроллер.

  
Давайте создадим `controller.py` со следующим кодом

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
    

  
Теперь мы определили зависимость от сервиса `BucketFileUpload` для `UserProfileController`. Нам нужно зарегистрировать `FileServiceModule` в настройках, чтобы избежать исключения `UnsatisfiedRequirement` от инжектора, когда Ninja Extra попытается создать объект.

**Регистрация модуля**
-----------------------

  
Существуют разные способы регистрации модулей injector в Django-приложении.

*     
    django_injector: если вы используете django_injector, в его документации описано, как регистрировать модули.
*     
    Ninja Extra: вы можете указать строковые пути к модулям в `INJECTOR_MODULES` внутри поля `NINJA_EXTRA`, как показано ниже:

###   
Регистрация на основе Ninja Extra

  
Мы регистрируем модули в ключе `INJECTOR_MODULES` внутри настроек Ninja Extra в файле настроек Django.

    NINJA_EXTRA = {
        'INJECTOR_MODULES': [
            'myproject.app1.modules.SomeModule',
            'myproject.app2.modules.SomeAppModule',
        ]
    }
    

  
Давайте зарегистрируем модуль `FileServiceModule` в настройках `NinjaExtra`

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
    

  
Готово. Мы полностью связали сервис `BucketFileUpload` с `UserProfileController`.

  
!!! warning Вы также можете переопределить конструктор вашего APIController параметрами без аннотаций. Подробнее о Python Injector

Использование `service_resolver`
------------------------

  
`service_resolver` — это вспомогательный класс, используемый для разрешения типов, зарегистрированных в экземпляре `injector`. Мы можем использовать его, когда нужно разрешить сервисы за пределами контроллера.

Например:

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service = service_resolver(BucketFileUpload)
    bucket_service.upload_file_to_s3('/path/to/file')
    

  
Мы также можем разрешить несколько сервисов одновременно, и в результате будет возвращён кортеж.

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service, service_a, service_b = service_resolver(BucketFileUpload, AnotherServiceA, AnotherServiceB)
    bucket_service.upload_file_to_s3('/path/to/file')
    
    service_a.do_something()
    service_b.do_something()
    
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
