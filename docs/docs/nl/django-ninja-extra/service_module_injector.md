Dependency Injection
=====

  
Een van de kernfuncties van de Django Ninja Extra APIController is de ondersteuning voor dependency injection met behulp van Injector.

  
Als je bijvoorbeeld een service genaamd AuthService hebt en deze wilt gebruiken in je `UsersController`-klasse, kun je deze eenvoudig als parameter toevoegen in de klasseconstructor en annoteren met het bijbehorende type.

    class UsersController(ControllerBase):
        def __init__(self, auth_service: AuthService):
            self.auth_service = auth_service
    

  
Vervolgens kun je in je applicatieconfiguratie deze service en de bijbehorende scope registreren. Standaard hebben services een singleton-scope, tenzij anders gespecificeerd.

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    

  
Je kunt ook de scope van de service specificeren. Dit is handig wanneer je verschillende instanties van dezelfde service voor verschillende verzoeken wilt gebruiken.

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=noscope)
    

  
Op deze manier kun je eenvoudig services injecteren in controllers en ze in de hele applicatie gebruiken. Dit maakt het gemakkelijk om controllers te testen en service-implementaties te wijzigen zonder andere delen van de applicatie te beïnvloeden.

  
!!! info Django-Ninja-Extra ondersteunt django_injector. Er is geen aanvullende configuratie vereist.

Een service maken
------------------

  
Een service is een zelfstandige module of functionele eenheid die kan worden hergebruikt in verschillende delen van een applicatie. Services worden doorgaans gebruikt om bedrijfslogica in te kapselen of om toegang te bieden tot gedeelde bronnen (zoals databases of externe API's). Services worden meestal geïmplementeerd als klassen en kunnen worden benaderd via een objectgeoriënteerde interface. Services kunnen worden gebruikt om bewerkingen uit te voeren, met externe systemen te interageren en berekeningen uit te voeren. Ze hebben doorgaans enkele publieke methoden en eigenschappen waarmee andere objecten ermee kunnen interageren. Services worden vaak gebruikt om applicatielogica te scheiden van infrastructuur, zodat applicatielogica onafhankelijk kan worden hergebruikt, getest en onderhouden.

  
Laten we een eenvoudige S3 bucket-service maken. Maak een `service.py` aan in je project en voeg het volgende toe

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
    

### Een module maken

  
In Python Injector is een module een klasse of functie die wordt gebruikt om de dependency injection-container te configureren. Een module is verantwoordelijk voor het binden van services aan hun implementaties en voor het configureren van de scope van services.

  
Een module kan een `configure(binder: Binder)`-functie definiëren die wordt gebruikt om de dependency injection-container te configureren. De parameter `binder` is een instantie van de klasse Binder die wordt gebruikt om services aan hun implementaties te binden.

  
Een module kan ook een of meer providerfuncties definiëren die worden gebruikt om instanties van services aan te maken. Deze functies kunnen worden gedecoreerd met `@inject` om de afhankelijkheden die ze moeten oplossen te specificeren, en met `@provider` om aan te geven dat ze moeten worden gebruikt om instanties van de service aan te maken.

Bijvoorbeeld:

    from injector import Binder, singleton, inject, provider
    
    class MyModule:
        def configure(self, binder: Binder) -> Binder:
            binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    
        @provider
        @inject
        def provide_user_service(self, auth_service: AuthService) -> UserService:
            return UserService(auth_service)
    

  
In het bovenstaande voorbeeld heeft de klasse `MyModule` een `configure`-methode die `AuthService` bindt en de scope instelt op `singleton`, en `provide_user_service`, die is gedecoreerd met `@provider` en `@inject` om `UserService` te leveren, met `AuthService` geïnjecteerd als afhankelijkheid.

  
Door een module te registreren in de Ninja Extra-instellingen worden alle services, providers en configuraties die in die module zijn gedefinieerd toegevoegd aan de Injector, en kunnen deze services in de hele applicatie worden opgelost en gebruikt.

  
Laten we een module maken voor de service `BucketFileUpload` die we eerder hebben gemaakt. Maak een `module.py` aan in je project en voeg de volgende code toe.

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
    

  
We hebben een `FileServiceModule` gemaakt die `BucketFileUpload` bindt aan `InMemoryBucketFileUpload`. In onze applicatie krijgen we, wanneer we `BucketFileUpload` oplossen, een instantie van `InMemoryBucketFileUpload` geleverd door de injector. We hebben ook de decorator `inject` gebruikt om django-instellingen vanuit de `injector` te injecteren in de service `InMemoryBucketFileUpload`.

  
De concrete klasse `InMemoryBucketFileUpload` is een eenvoudige ontwikkelklasse. In productie wil je mogelijk een betere service schrijven om bestanden op te slaan in je AWS S3 bucket.

Service-scope
-------------

  
De scope definieert de levenscyclus van aangemaakte services. Er zijn drie hoofdscopes bij het gebruik van dependency injection in webframeworks.

### `singleton` scope

  
Een singleton-service wordt slechts één keer aangemaakt en dezelfde instantie wordt hergebruikt gedurende de volledige levensduur van de applicatie. Dit is de standaardscope wanneer er geen scope is gespecificeerd.

    from injector import Module, Binder, singleton
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=singleton)
    

### `transient` scope

  
Een transient-service wordt bij elk verzoek aangemaakt. Elk verzoek maakt een nieuwe instantie aan. Dit is nuttig voor services die geen status bijhouden of niet gedeeld moeten worden over meerdere verzoeken.

    from injector import Module, Binder, noscope
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=noscope)
    

### `scoped`

  
Een scoped service wordt één keer per verzoek aangemaakt. Voor elk binnenkomend verzoek wordt een nieuwe instantie gemaakt die wordt gedeeld met alle componenten die er binnen hetzelfde verzoek van afhankelijk zijn. Dit is nuttig voor services die verzoekspecifieke status bijhouden.

  
Momenteel ondersteunt Ninja Extra geen services met de `scoped`-scope.

  
Bij het registreren van services bij de dependency injection-container is het belangrijk om de juiste scope te kiezen. `Singleton`-services zijn geschikt voor services die applicatiebrede status bijhouden, `transient`-services zijn geschikt voor services die geen status bijhouden, en `scoped`-services zijn geschikt voor services die verzoekspecifieke status bijhouden.

  
Services toevoegen aan controllers
-----------

  
De constructor (`__init__`) van de Ninja Extra-controller is gedecoreerd met de functie `inject` uit de `injector`-bibliotheek. Hierdoor is het mogelijk om parameters met type-annotaties in de constructor te definiëren, en de geannoteerde types worden geïnjecteerd tijdens het instantiëren van het object.

  
We hebben een `BucketFileUpload`-contract en enkele concrete implementaties gemaakt, laten we deze toevoegen aan een controller.

  
Laten we een `controller.py` maken met de volgende code

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
    

  
Nu hebben we een serviceafhankelijkheid `BucketFileUpload` gedefinieerd voor de `UserProfileController`. We moeten de `FileServiceModule` registreren in de instellingen om te voorkomen dat de injector een `UnsatisfiedRequirement`-uitzondering genereert wanneer Ninja Extra het object probeert aan te maken.

**Module-registratie**
-----------------------

  
Er zijn verschillende manieren om injector-modules te registreren in een Django-applicatie.

*     
    django_injector: Als je django_injector gebruikt, bevat het documentatie over hoe je modules kunt registreren.
*     
    Ninja Extra: Je kunt module-stringpaden opgeven in `INJECTOR_MODULES` binnen het veld `NINJA_EXTRA`, zoals hieronder weergegeven:

###   
Registratie op basis van Ninja Extra

  
We registreren modules in de sleutel `INJECTOR_MODULES` binnen de Ninja Extra-instellingen in het django-instellingenbestand.

    NINJA_EXTRA = {
        'INJECTOR_MODULES': [
            'myproject.app1.modules.SomeModule',
            'myproject.app2.modules.SomeAppModule',
        ]
    }
    

  
Laten we de module `FileServiceModule` registreren in de `NinjaExtra`-instellingen

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
    

  
Dat is alles. We hebben de service `BucketFileUpload` volledig gekoppeld aan de `UserProfileController`.

  
!!! warning Je kunt de constructor van je APIController ook overschrijven met parameters die niet geannoteerd zijn. Meer over Python Injector

Gebruik van `service_resolver`
------------------------

  
`service_resolver` is een hulpklasse die wordt gebruikt om types op te lossen die zijn geregistreerd in de `injector`-instantie. We kunnen deze gebruiken wanneer we services buiten een controller moeten oplossen.

Bijvoorbeeld:

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service = service_resolver(BucketFileUpload)
    bucket_service.upload_file_to_s3('/path/to/file')
    

  
We kunnen ook meerdere services tegelijk oplossen, en er wordt een tuple als resultaat teruggegeven.

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service, service_a, service_b = service_resolver(BucketFileUpload, AnotherServiceA, AnotherServiceB)
    bucket_service.upload_file_to_s3('/path/to/file')
    
    service_a.do_something()
    service_b.do_something()
    
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
