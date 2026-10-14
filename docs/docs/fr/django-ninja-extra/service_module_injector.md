Injection de dépendances
=====

  
L'une des fonctionnalités principales de l'APIController de Django Ninja Extra est la prise en charge de l'injection de dépendances à l'aide d'Injector.

  
Par exemple, si vous disposez d'un service appelé AuthService et que vous souhaitez l'utiliser dans votre classe `UsersController`, vous pouvez simplement l'ajouter comme paramètre dans le constructeur de la classe et l'annoter avec son type.

    class UsersController(ControllerBase):
        def __init__(self, auth_service: AuthService):
            self.auth_service = auth_service
    

  
Ensuite, dans la configuration de votre application, vous pouvez enregistrer ce service et sa portée. Par défaut, les services ont une portée singleton, sauf spécification contraire.

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    

  
Vous pouvez également spécifier la portée du service. Cela est utile lorsque vous souhaitez utiliser différentes instances du même service pour différentes requêtes.

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=noscope)
    

  
De cette manière, vous pouvez facilement injecter des services dans les contrôleurs et les utiliser dans toute l'application. Cela facilite le test des contrôleurs et le remplacement des implémentations de services sans affecter les autres parties de l'application.

  
!!! info Django-Ninja-Extra prend en charge django_injector. Aucune configuration supplémentaire n'est requise.

Créer un service
------------------

  
Un service est un module autonome ou une unité fonctionnelle qui peut être réutilisé dans différentes parties d'une application. Les services sont généralement utilisés pour encapsuler la logique métier ou fournir un accès à des ressources partagées (telles que des bases de données ou des API externes). Les services sont généralement implémentés sous forme de classes et peuvent être accessés via une interface orientée objet. Les services peuvent être utilisés pour effectuer des opérations, interagir avec des systèmes externes et réaliser des calculs. Ils disposent généralement de méthodes et de propriétés publiques qui permettent à d'autres objets d'interagir avec eux. Les services sont couramment utilisés pour séparer la logique applicative de l'infrastructure, afin que la logique applicative puisse être réutilisée, testée et maintenue de manière indépendante.

  
Créons un service simple de bucket S3. Créez un fichier `service.py` dans votre projet et ajoutez ce qui suit

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
    

### Créer un module

  
Dans Python Injector, un module est une classe ou une fonction utilisée pour configurer le conteneur d'injection de dépendances. Un module est responsable de la liaison des services à leurs implémentations et de la configuration de la portée des services.

  
Un module peut définir une fonction `configure(binder: Binder)` utilisée pour configurer le conteneur d'injection de dépendances. Le paramètre `binder` est une instance de la classe Binder utilisée pour lier les services à leurs implémentations.

  
Un module peut également définir une ou plusieurs fonctions provider utilisées pour créer des instances de services. Ces fonctions peuvent être décorées avec `@inject` pour spécifier les dépendances qu'elles doivent résoudre, et avec `@provider` pour indiquer qu'elles doivent être utilisées pour créer des instances du service.

Par exemple :

    from injector import Binder, singleton, inject, provider
    
    class MyModule:
        def configure(self, binder: Binder) -> Binder:
            binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    
        @provider
        @inject
        def provide_user_service(self, auth_service: AuthService) -> UserService:
            return UserService(auth_service)
    

  
Dans l'exemple ci-dessus, la classe `MyModule` possède une méthode `configure` qui lie `AuthService` et définit la portée sur `singleton`, ainsi que `provide_user_service`, qui est décorée avec `@provider` et `@inject` pour fournir `UserService`, avec `AuthService` injecté comme dépendance.

  
En enregistrant un module dans les settings de Ninja Extra, tous les services, providers et configurations définis dans ce module seront ajoutés à l'Injector, et ces services pourront être résolus et utilisés dans toute l'application.

  
Créons un module pour le service `BucketFileUpload` que nous avons créé précédemment. Créez un fichier `module.py` dans votre projet et ajoutez le code suivant.

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
    

  
Nous avons créé un `FileServiceModule` qui lie `BucketFileUpload` à `InMemoryBucketFileUpload`. Dans notre application, lors de la résolution de `BucketFileUpload`, nous obtiendrons une instance de `InMemoryBucketFileUpload` fournie par l'injector. Nous avons également utilisé le décorateur `inject` pour injecter les django settings dans le service `InMemoryBucketFileUpload` à partir de l'`injector`.

  
La classe concrète `InMemoryBucketFileUpload` est une classe simple destinée au développement. En production, vous souhaiterez peut-être écrire un meilleur service pour enregistrer des fichiers dans votre bucket AWS S3.

Portée des services
-------------

  
La portée définit le cycle de vie des services créés. Il existe trois portées principales lors de l'utilisation de l'injection de dépendances dans les frameworks web.

### Portée `singleton`

  
Un service singleton n'est créé qu'une seule fois, et la même instance est réutilisée tout au long de la durée de vie de l'application entière. Il s'agit de la portée par défaut lorsqu'aucune portée n'est spécifiée.

    from injector import Module, Binder, singleton
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=singleton)
    

### Portée `transient`

  
Un service transient est créé à chaque requête. Chaque requête crée une nouvelle instance. Cela est utile pour les services qui ne maintiennent pas d'état ou qui ne doivent pas être partagés entre plusieurs requêtes.

    from injector import Module, Binder, noscope
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=noscope)
    

### Portée `scoped`

  
Un service scoped est créé une fois par requête. Une nouvelle instance est créée pour chaque requête entrante et partagée entre tous les composants qui en dépendent au sein de la même requête. Cela est utile pour les services qui maintiennent un état spécifique à la requête.

  
Actuellement, Ninja Extra ne prend pas en charge les services avec la portée `scoped`.

  
Lors de l'enregistrement de services dans le conteneur d'injection de dépendances, le choix de la portée appropriée est important. Les services `Singleton` conviennent aux services qui maintiennent un état à l'échelle de l'application, les services `transient` conviennent aux services qui ne maintiennent pas d'état, et les services `scoped` conviennent aux services qui maintiennent un état spécifique à la requête.

  
Ajouter des services aux contrôleurs
-----------

  
Le constructeur du contrôleur Ninja Extra (`__init__`) est décoré avec la fonction `inject` de la bibliothèque `injector`. Cela permet de définir des paramètres avec des annotations de type dans le constructeur, et les types annotés seront injectés lors de l'instanciation de l'objet.

  
Nous avons créé un contrat `BucketFileUpload` et quelques implémentations concrètes, ajoutons-le à un contrôleur.

  
Créons un fichier `controller.py` avec le code suivant

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
    

  
Maintenant, nous avons défini une dépendance au service `BucketFileUpload` pour le `UserProfileController`. Nous devons enregistrer le `FileServiceModule` dans les settings pour éviter une exception `UnsatisfiedRequirement` de la part de l'injector lorsque Ninja Extra essaie de créer l'objet.

**Enregistrement des modules**
-----------------------

  
Il existe différentes manières d'enregistrer des modules injector dans une application Django.

*     
    django_injector : si vous utilisez django_injector, sa documentation explique comment enregistrer des modules.
*     
    Ninja Extra : vous pouvez fournir les chemins des modules sous forme de chaînes dans `INJECTOR_MODULES` au sein du champ `NINJA_EXTRA`, comme indiqué ci-dessous :

###   
Enregistrement basé sur Ninja Extra

  
Nous enregistrons les modules dans la clé `INJECTOR_MODULES` au sein des settings de Ninja Extra dans le fichier de settings Django.

    NINJA_EXTRA = {
        'INJECTOR_MODULES': [
            'myproject.app1.modules.SomeModule',
            'myproject.app2.modules.SomeAppModule',
        ]
    }
    

  
Enregistrons le module `FileServiceModule` dans les settings `NinjaExtra`

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
    

  
Et voilà. Nous avons entièrement câblé le service `BucketFileUpload` au `UserProfileController`.

  
!!! warning Vous pouvez également redéfinir le constructeur de votre APIController avec des paramètres non annotés. Plus d'informations sur Python Injector

Utilisation de `service_resolver`
------------------------

  
`service_resolver` est une classe utilitaire utilisée pour résoudre les types enregistrés dans l'instance `injector`. Nous pouvons l'utiliser lorsque nous avons besoin de résoudre des services en dehors d'un contrôleur.

Par exemple :

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service = service_resolver(BucketFileUpload)
    bucket_service.upload_file_to_s3('/path/to/file')
    

  
Nous pouvons également résoudre plusieurs services à la fois, et un résultat sous forme de tuple sera renvoyé.

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service, service_a, service_b = service_resolver(BucketFileUpload, AnotherServiceA, AnotherServiceB)
    bucket_service.upload_file_to_s3('/path/to/file')
    
    service_a.do_something()
    service_b.do_something()
    
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
