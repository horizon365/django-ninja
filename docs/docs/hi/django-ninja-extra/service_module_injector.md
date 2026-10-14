Dependency Injection
=====
 
  
Django Ninja Extra APIController की एक core विशेषता Injector के माध्यम से dependency injection का समर्थन है।

  
उदाहरण के लिए, यदि आपके पास AuthService नाम की एक service है और आप इसे अपनी `UsersController` class में उपयोग करना चाहते हैं, तो आप इसे class constructor में एक parameter के रूप में जोड़ सकते हैं और उसके type के साथ annotate कर सकते हैं।

    class UsersController(ControllerBase):
        def __init__(self, auth_service: AuthService):
            self.auth_service = auth_service
    

  
फिर अपने application configuration में, आप इस service और उसके scope को register कर सकते हैं। डिफ़ॉल्ट रूप से, services singleton scoped होती हैं जब तक कि अलग से निर्दिष्ट न किया जाए।

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    

  
आप service का scope भी निर्दिष्ट कर सकते हैं। यह तब उपयोगी होता है जब आप अलग-अलग requests के लिए उसी service के अलग-अलग instances का उपयोग करना चाहते हैं।

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=noscope)
    

  
इस तरह, आप controllers में आसानी से services inject कर सकते हैं और उन्हें पूरे application में उपयोग कर सकते हैं। इससे controllers को test करना और application के अन्य हिस्सों को प्रभावित किए बिना service implementations बदलना आसान हो जाता है।

  
!!! info Django-Ninja-Extra django_injector को support करता है। किसी अतिरिक्त configuration की आवश्यकता नहीं है।

Creating a Service
------------------

  
Service एक self-contained module या functional unit होती है जिसे application के विभिन्न हिस्सों में पुनः उपयोग किया जा सकता है। Services का उपयोग आमतौर पर business logic को encapsulate करने या shared resources (जैसे databases या external APIs) तक access प्रदान करने के लिए किया जाता है। Services आमतौर पर classes के रूप में implement की जाती हैं और इन्हें object-oriented interface के माध्यम से access किया जा सकता है। Services का उपयोग operations करने, external systems के साथ interact करने और computations करने के लिए किया जा सकता है। इनमें आमतौर पर कुछ public methods और properties होती हैं जो अन्य objects को उनके साथ interact करने की अनुमति देती हैं। Services का उपयोग आमतौर पर application logic को infrastructure से अलग करने के लिए किया जाता है, ताकि application logic को स्वतंत्र रूप से पुनः उपयोग, test और maintain किया जा सके।

  
आइए एक सरल S3 bucket service बनाएं। अपने project में एक `service.py` बनाएं और निम्नलिखित जोड़ें

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

  
Python Injector में, module एक class या function होता है जिसका उपयोग dependency injection container को configure करने के लिए किया जाता है। Module services को उनके implementations के साथ bind करने और services के scope को configure करने के लिए जिम्मेदार होता है।

  
एक module `configure(binder: Binder)` function define कर सकता है जिसका उपयोग dependency injection container को configure करने के लिए किया जाता है। `binder` parameter Binder class का एक instance है जिसका उपयोग services को उनके implementations के साथ bind करने के लिए किया जाता है।

  
एक module एक या अधिक provider functions भी define कर सकता है जिनका उपयोग services के instances बनाने के लिए किया जाता है। इन functions को `@inject` से decorate किया जा सकता है ताकि वे dependencies निर्दिष्ट कर सकें जिन्हें उन्हें resolve करने की आवश्यकता है, और `@provider` से decorate किया जा सकता है यह बताने के लिए कि उनका उपयोग service के instances बनाने के लिए किया जाना चाहिए।

उदाहरण के लिए:

    from injector import Binder, singleton, inject, provider
    
    class MyModule:
        def configure(self, binder: Binder) -> Binder:
            binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    
        @provider
        @inject
        def provide_user_service(self, auth_service: AuthService) -> UserService:
            return UserService(auth_service)
    

  
ऊपर दिए गए उदाहरण में, `MyModule` class में एक `configure` method है जो `AuthService` को bind करता है और scope को `singleton` सेट करता है, और `provide_user_service`, जिसे `@provider` और `@inject` से decorate किया गया है ताकि `UserService` प्रदान किया जा सके, जिसमें dependency के रूप में `AuthService` inject किया गया है।

  
Ninja Extra settings में एक module register करने पर, उस module में परिभाषित सभी services, providers और configurations Injector में जुड़ जाएंगे, और इन services को पूरे application में resolve और उपयोग किया जा सकता है।

  
आइए हमारे द्वारा पहले बनाई गई `BucketFileUpload` service के लिए एक module बनाएं। अपने project में एक `module.py` बनाएं और निम्नलिखित code जोड़ें।

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
    

  
हमने एक `FileServiceModule` बनाया जो `BucketFileUpload` को `InMemoryBucketFileUpload` के साथ bind करता है। हमारे application में, `BucketFileUpload` को resolve करते समय, हमें injector द्वारा प्रदान किया गया `InMemoryBucketFileUpload` का एक instance मिलेगा। हमने `inject` decorator का भी उपयोग किया ताकि `injector` से django settings को `InMemoryBucketFileUpload` service में inject किया जा सके।

  
`InMemoryBucketFileUpload` concrete class एक सरल development class है। Production में, आप शायद एक बेहतर service लिखना चाहेंगे जो फ़ाइलों को आपके AWS S3 bucket में सहेती हो।

Service Scope
-------------

  
Scope बनाई गई services का lifecycle define करता है। Web frameworks में dependency injection का उपयोग करते समय तीन मुख्य scopes होते हैं।

### `singleton` scope

  
एक singleton service केवल एक बार बनाई जाती है, और पूरे application के lifetime के दौरान वही instance दोबारा उपयोग किया जाता है। जब कोई scope निर्दिष्ट नहीं किया जाता, तो यह डिफ़ॉल्ट scope होता है।

    from injector import Module, Binder, singleton
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=singleton)
    

### `transient` scope

  
एक transient service हर request पर बनाई जाती है। प्रत्येक request एक नया instance बनाती है। यह उन services के लिए उपयोगी है जो state बनाए नहीं रखतीं या जिन्हें कई requests के बीच share नहीं किया जाना चाहिए।

    from injector import Module, Binder, noscope
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=noscope)
    

### `scoped`

  
एक scoped service प्रति request एक बार बनाई जाती है। प्रत्येक incoming request के लिए एक नया instance बनाया जाता है और उसे उसी request के भीतर उस पर निर्भर सभी components के बीच share किया जाता है। यह उन services के लिए उपयोगी है जो request-specific state बनाए रखती हैं।

  
वर्तमान में, Ninja Extra `scoped` scope वाली services का समर्थन नहीं करता है।

  
Dependency injection container के साथ services register करते समय, उपयुक्त scope चुनना महत्वपूर्ण है। `Singleton` services उन services के लिए उपयुक्त हैं जो application-wide state बनाए रखती हैं, `transient` services उन services के लिए उपयुक्त हैं जो state नहीं रखतीं, और `scoped` services उन services के लिए उपयुक्त हैं जो request-specific state बनाए रखती हैं।

  
Adding Services to Controllers
-----------

  
Ninja Extra controller constructor (`__init__`) को `injector` library के `inject` function से decorate किया जाता है। इससे constructor में type annotations के साथ parameters define करना संभव होता है, और annotated types object instantiation के दौरान inject किए जाएंगे।

  
हमने एक `BucketFileUpload` contract और कुछ concrete implementations बनाए हैं, आइए इसे एक controller में जोड़ें।

  
आइए निम्नलिखित code के साथ एक `controller.py` बनाएं

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
    

  
अब, हमने `UserProfileController` के लिए `BucketFileUpload` service dependency define कर दी है। हमें injector से एक `UnsatisfiedRequirement` exception से बचने के लिए `FileServiceModule` को settings में register करने की आवश्यकता है, जब Ninja Extra object बनाने का प्रयास करता है।

**Module Registration**
-----------------------

  
एक Django application में injector modules को register करने के विभिन्न तरीके हैं।

*     
    django_injector: यदि आप django_injector का उपयोग कर रहे हैं, तो इसमें modules को register करने के तरीके पर documentation है।
*     
    Ninja Extra: आप `NINJA_EXTRA` field के भीतर `INJECTOR_MODULES` में module string paths प्रदान कर सकते हैं, जैसा कि नीचे दिखाया गया है:

###   
Ninja Extra-based Registration

  
हम django settings फ़ाइल में Ninja Extra settings के भीतर `INJECTOR_MODULES` key में modules register करते हैं।

    NINJA_EXTRA = {
        'INJECTOR_MODULES': [
            'myproject.app1.modules.SomeModule',
            'myproject.app2.modules.SomeAppModule',
        ]
    }
    

  
आइए `NinjaExtra` settings में `FileServiceModule` module को register करें

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
    

  
बस इतना ही। हमने `BucketFileUpload` service को पूरी तरह `UserProfileController` से जोड़ दिया है।

  
!!! warning आप अपने APIController constructor को ऐसे parameters के साथ भी override कर सकते हैं जो annotated नहीं हैं। Python Injector के बारे में अधिक जानकारी

Using `service_resolver`
------------------------

  
`service_resolver` एक utility class है जिसका उपयोग `injector` instance में register किए गए types को resolve करने के लिए किया जाता है। जब हमें controller के बाहर services को resolve करने की आवश्यकता होती है, तब हम इसका उपयोग कर सकते हैं।

उदाहरण के लिए:

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service = service_resolver(BucketFileUpload)
    bucket_service.upload_file_to_s3('/path/to/file')
    

  
हम एक साथ कई services को भी resolve कर सकते हैं, और एक tuple result लौटाया जाएगा।

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service, service_a, service_b = service_resolver(BucketFileUpload, AnotherServiceA, AnotherServiceB)
    bucket_service.upload_file_to_s3('/path/to/file')
    
    service_a.do_something()
    service_b.do_something()
    
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
