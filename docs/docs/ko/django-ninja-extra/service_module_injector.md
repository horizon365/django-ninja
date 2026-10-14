의존성 주입
=====
  
Django Ninja Extra APIController의 핵심 기능 중 하나는 Injector를 사용한 의존성 주입 지원입니다.

  
예를 들어, AuthService라는 서비스가 있고 이를 `UsersController` 클래스에서 사용하려면, 클래스 생성자의 매개변수로 추가하고 해당 타입으로 어노테이션을 지정하기만 하면 됩니다.

    class UsersController(ControllerBase):
        def __init__(self, auth_service: AuthService):
            self.auth_service = auth_service
    

  
그런 다음 애플리케이션 설정에서 이 서비스와 그 스코프(scope)를 등록할 수 있습니다. 기본적으로 서비스는 별도로 지정하지 않는 한 싱글톤(singleton) 스코프로 등록됩니다.

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    

  
서비스의 스코프를 직접 지정할 수도 있습니다. 이는 동일한 서비스에 대해 요청마다 다른 인스턴스를 사용하고 싶을 때 유용합니다.

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=noscope)
    

  
이렇게 하면 컨트롤러에 서비스를 쉽게 주입하고 애플리케이션 전반에서 사용할 수 있습니다. 덕분에 컨트롤러를 테스트하기 쉬워지고, 애플리케이션의 다른 부분에 영향을 주지 않고도 서비스 구현체를 변경할 수 있습니다.

  
!!! info Django-Ninja-Extra는 django_injector를 지원합니다. 별도의 추가 설정이 필요하지 않습니다.

서비스 만들기
------------------

  
서비스는 애플리케이션의 여러 부분에서 재사용할 수 있는 자체 완결적인 모듈 또는 기능 단위입니다. 서비스는 일반적으로 비즈니스 로직을 캡슐화하거나 공유 리소스(예: 데이터베이스 또는 외부 API)에 대한 접근을 제공하는 데 사용됩니다. 서비스는 보통 클래스로 구현되며 객체 지향 인터페이스를 통해 접근할 수 있습니다. 서비스는 연산을 수행하고, 외부 시스템과 상호작용하며, 계산을 처리하는 데 사용될 수 있습니다. 서비스는 일반적으로 다른 객체들이 상호작용할 수 있는 public 메서드와 프로퍼티를 갖습니다. 서비스는 애플리케이션 로직을 인프라로부터 분리하여, 애플리케이션 로직을 독립적으로 재사용하고 테스트하고 유지보수할 수 있도록 하는 데 흔히 사용됩니다.

  
간단한 S3 버킷 서비스를 만들어 보겠습니다. 프로젝트에 `service.py`를 만들고 다음을 추가합니다

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
    

### 모듈 만들기

  
Python Injector에서 모듈(module)은 의존성 주입 컨테이너를 설정하는 데 사용되는 클래스 또는 함수입니다. 모듈은 서비스를 구현체에 바인딩하고 서비스의 스코프를 구성하는 역할을 담당합니다.

  
모듈은 의존성 주입 컨테이너를 구성하는 데 사용되는 `configure(binder: Binder)` 함수를 정의할 수 있습니다. `binder` 매개변수는 서비스를 구현체에 바인딩하는 데 사용되는 Binder 클래스의 인스턴스입니다.

  
모듈은 서비스 인스턴스를 생성하는 데 사용되는 하나 이상의 프로바이더(provider) 함수를 정의할 수도 있습니다. 이러한 함수들은 `@inject` 데코레이터로 데코레이트하여 해결해야 할 의존성을 지정할 수 있고, `@provider` 데코레이터로 데코레이트하여 서비스 인스턴스를 생성하는 데 사용되어야 함을 나타낼 수 있습니다.

예를 들어:

    from injector import Binder, singleton, inject, provider
    
    class MyModule:
        def configure(self, binder: Binder) -> Binder:
            binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    
        @provider
        @inject
        def provide_user_service(self, auth_service: AuthService) -> UserService:
            return UserService(auth_service)
    

  
위 예제에서 `MyModule` 클래스는 `AuthService`를 바인딩하고 스코프를 `singleton`으로 설정하는 `configure` 메서드와, `@provider` 및 `@inject`로 데코레이트되어 `AuthService`를 의존성으로 주입받아 `UserService`를 제공하는 `provide_user_service`를 갖고 있습니다.

  
Ninja Extra 설정에 모듈을 등록하면, 해당 모듈에 정의된 모든 서비스, 프로바이더, 설정이 Injector에 추가되며, 이 서비스들은 애플리케이션 전반에서 해결(resolve)되어 사용될 수 있습니다.

  
앞서 만든 `BucketFileUpload` 서비스를 위한 모듈을 만들어 보겠습니다. 프로젝트에 `module.py`를 만들고 다음 코드를 추가합니다.

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
    

  
`BucketFileUpload`를 `InMemoryBucketFileUpload`에 바인딩하는 `FileServiceModule`을 만들었습니다. 애플리케이션에서 `BucketFileUpload`를 resolve하면 인젝터가 제공하는 `InMemoryBucketFileUpload` 인스턴스를 얻게 됩니다. 또한 `inject` 데코레이터를 사용하여 injector로부터 django 설정을 `InMemoryBucketFileUpload` 서비스에 주입했습니다.

  
`InMemoryBucketFileUpload` 구체 클래스는 간단한 개발용 클래스입니다. 실제 운영 환경에서는 파일을 AWS S3 버킷에 저장하는 더 나은 서비스를 작성하고 싶을 수 있습니다.

서비스 스코프
-------------

  
스코프(scope)는 생성된 서비스의 라이프사이클을 정의합니다. 웹 프레임워크에서 의존성 주입을 사용할 때는 세 가지 주요 스코프가 있습니다.

### `singleton` 스코프

  
싱글톤 서비스는 한 번만 생성되며, 애플리케이션 전체 수명 동안 동일한 인스턴스가 재사용됩니다. 스코프를 지정하지 않을 때의 기본 스코프입니다.

    from injector import Module, Binder, singleton
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=singleton)
    

### `transient` 스코프

  
transient 서비스는 요청할 때마다 생성됩니다. 각 요청마다 새로운 인스턴스가 만들어집니다. 상태를 유지하지 않거나 여러 요청 간에 공유되어서는 안 되는 서비스에 유용합니다.

    from injector import Module, Binder, noscope
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=noscope)
    

### `scoped`

  
scoped 서비스는 요청당 한 번 생성됩니다. 들어오는 각 요청마다 새 인스턴스가 만들어지고, 동일한 요청 내에서 이에 의존하는 모든 컴포넌트가 해당 인스턴스를 공유합니다. 요청별 상태를 유지하는 서비스에 유용합니다.

  
현재 Ninja Extra는 `scoped` 스코프 서비스를 지원하지 않습니다.

  
의존성 주입 컨테이너에 서비스를 등록할 때는 적절한 스코프를 선택하는 것이 중요합니다. `Singleton` 서비스는 애플리케이션 전역 상태를 유지하는 서비스에 적합하고, `transient` 서비스는 상태를 유지하지 않는 서비스에 적합하며, `scoped` 서비스는 요청별 상태를 유지하는 서비스에 적합합니다.

  
컨트롤러에 서비스 추가하기
-----------

  
Ninja Extra 컨트롤러의 생성자(`__init__`)는 `injector` 라이브러리의 `inject` 함수로 데코레이트되어 있습니다. 이 덕분에 생성자에서 타입 어노테이션이 지정된 매개변수를 정의할 수 있으며, 어노테이션된 타입들은 객체 인스턴스화 과정에서 주입됩니다.

  
`BucketFileUpload` 계약(contract)과 몇 가지 구체 구현체를 만들었으니, 이제 컨트롤러에 추가해 보겠습니다.

  
다음 코드로 `controller.py`를 만들어 보겠습니다

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
    

  
이제 `UserProfileController`를 위한 `BucketFileUpload` 서비스 의존성을 정의했습니다. Ninja Extra가 객체를 생성하려 할 때 injector로부터 `UnsatisfiedRequirement` 예외가 발생하지 않도록, `FileServiceModule`을 설정에 등록해야 합니다.

**모듈 등록**
-----------------------

  
Django 애플리케이션에 injector 모듈을 등록하는 방법은 여러 가지입니다.

*     
    django_injector: django_injector를 사용하는 경우, 모듈 등록 방법에 대한 문서를 제공합니다.
*     
    Ninja Extra: 아래와 같이 `NINJA_EXTRA` 필드 내의 `INJECTOR_MODULES`에 모듈 문자열 경로를 제공할 수 있습니다:

###   
Ninja Extra 기반 등록

  
django 설정 파일의 Ninja Extra 설정 내 `INJECTOR_MODULES` 키에 모듈을 등록합니다.

    NINJA_EXTRA = {
        'INJECTOR_MODULES': [
            'myproject.app1.modules.SomeModule',
            'myproject.app2.modules.SomeAppModule',
        ]
    }
    

  
`FileServiceModule` 모듈을 `NinjaExtra` 설정에 등록해 보겠습니다

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
    

  
이것으로 끝입니다. `BucketFileUpload` 서비스를 `UserProfileController`에 완전히 연결했습니다.

  
!!! warning 어노테이션이 지정되지 않은 매개변수로 APIController 생성자를 오버라이드할 수도 있습니다. Python Injector에 대해 더 알아보기

`service_resolver` 사용하기
------------------------

  
`service_resolver`는 `injector` 인스턴스에 등록된 타입을 resolve하는 데 사용되는 유틸리티 클래스입니다. 컨트롤러 밖에서 서비스를 resolve해야 할 때 사용할 수 있습니다.

예를 들어:

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service = service_resolver(BucketFileUpload)
    bucket_service.upload_file_to_s3('/path/to/file')
    

  
여러 서비스를 한 번에 resolve할 수도 있으며, 그 결과는 튜플로 반환됩니다.

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service, service_a, service_b = service_resolver(BucketFileUpload, AnotherServiceA, AnotherServiceB)
    bucket_service.upload_file_to_s3('/path/to/file')
    
    service_a.do_something()
    service_b.do_something()
    
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
