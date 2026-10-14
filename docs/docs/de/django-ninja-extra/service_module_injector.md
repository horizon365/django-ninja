Dependency Injection
=====

  
Eine der Kernfunktionen des Django Ninja Extra APIController ist die Unterstützung von Dependency Injection mit Injector.

  
Wenn Sie beispielsweise einen Dienst namens AuthService haben und ihn in Ihrer Klasse `UsersController` verwenden möchten, können Sie ihn einfach als Parameter im Klassenkonstruktor hinzufügen und mit seinem Typ annotieren.

    class UsersController(ControllerBase):
        def __init__(self, auth_service: AuthService):
            self.auth_service = auth_service
    

  
In Ihrer Anwendungskonfiguration können Sie dann diesen Dienst und seinen Scope registrieren. Standardmäßig sind Dienste singleton-scoped, sofern nichts anderes angegeben ist.

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    

  
Sie können auch den Scope des Dienstes angeben. Dies ist nützlich, wenn Sie unterschiedliche Instanzen desselben Dienstes für unterschiedliche Requests verwenden möchten.

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=noscope)
    

  
Auf diese Weise können Sie Dienste problemlos in Controller injizieren und sie in der gesamten Anwendung verwenden. Dies erleichtert das Testen von Controllern und das Austauschen von Dienst-Implementierungen, ohne andere Teile der Anwendung zu beeinträchtigen.

  
!!! info Django-Ninja-Extra unterstützt django_injector. Es ist keine zusätzliche Konfiguration erforderlich.

Einen Dienst erstellen
------------------

  
Ein Dienst ist ein in sich geschlossenes Modul oder eine Funktionseinheit, die in verschiedenen Teilen einer Anwendung wiederverwendet werden kann. Dienste werden typischerweise verwendet, um Geschäftslogik zu kapseln oder den Zugriff auf gemeinsam genutzte Ressourcen (z. B. Datenbanken oder externe APIs) bereitzustellen. Dienste werden in der Regel als Klassen implementiert und können über eine objektorientierte Schnittstelle aufgerufen werden. Dienste können verwendet werden, um Operationen auszuführen, mit externen Systemen zu interagieren und Berechnungen durchzuführen. Sie verfügen üblicherweise über einige öffentliche Methoden und Eigenschaften, die es anderen Objekten ermöglichen, mit ihnen zu interagieren. Dienste werden häufig verwendet, um Anwendungslogik von der Infrastruktur zu trennen, sodass Anwendungslogik unabhängig wiederverwendet, getestet und gewartet werden kann.

  
Erstellen wir einen einfachen S3-Bucket-Dienst. Erstellen Sie eine `service.py` in Ihrem Projekt und fügen Sie Folgendes hinzu

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
    

### Ein Modul erstellen

  
In Python Injector ist ein Modul eine Klasse oder Funktion, die zur Konfiguration des Dependency-Injection-Containers verwendet wird. Ein Modul ist dafür verantwortlich, Dienste an ihre Implementierungen zu binden und den Scope der Dienste zu konfigurieren.

  
Ein Modul kann eine Funktion `configure(binder: Binder)` definieren, die zur Konfiguration des Dependency-Injection-Containers verwendet wird. Der Parameter `binder` ist eine Instanz der Klasse Binder, die zum Binden von Diensten an ihre Implementierungen verwendet wird.

  
Ein Modul kann auch eine oder mehrere Provider-Funktionen definieren, die zum Erstellen von Instanzen von Diensten verwendet werden. Diese Funktionen können mit `@inject` dekoriert werden, um die Abhängigkeiten anzugeben, die sie auflösen müssen, und mit `@provider`, um anzuzeigen, dass sie zum Erstellen von Instanzen des Dienstes verwendet werden sollen.

Zum Beispiel:

    from injector import Binder, singleton, inject, provider
    
    class MyModule:
        def configure(self, binder: Binder) -> Binder:
            binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    
        @provider
        @inject
        def provide_user_service(self, auth_service: AuthService) -> UserService:
            return UserService(auth_service)
    

  
Im obigen Beispiel hat die Klasse `MyModule` eine Methode `configure`, die `AuthService` bindet und den Scope auf `singleton` setzt, sowie `provide_user_service`, das mit `@provider` und `@inject` dekoriert ist, um `UserService` bereitzustellen, wobei `AuthService` als Abhängigkeit injiziert wird.

  
Durch die Registrierung eines Moduls in den Ninja-Extra-Einstellungen werden alle in diesem Modul definierten Dienste, Provider und Konfigurationen zum Injector hinzugefügt, und diese Dienste können in der gesamten Anwendung aufgelöst und verwendet werden.

  
Erstellen wir ein Modul für den zuvor erstellten Dienst `BucketFileUpload`. Erstellen Sie eine `module.py` in Ihrem Projekt und fügen Sie den folgenden Code hinzu.

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
    

  
Wir haben ein `FileServiceModule` erstellt, das `BucketFileUpload` an `InMemoryBucketFileUpload` bindet. In unserer Anwendung erhalten wir beim Auflösen von `BucketFileUpload` eine Instanz von `InMemoryBucketFileUpload`, die vom Injector bereitgestellt wird. Außerdem haben wir den Decorator `inject` verwendet, um die Django-Einstellungen über den `injector` in den Dienst `InMemoryBucketFileUpload` zu injizieren.

  
Die konkrete Klasse `InMemoryBucketFileUpload` ist eine einfache Entwicklungsklasse. In der Produktion möchten Sie möglicherweise einen besseren Dienst schreiben, der Dateien in Ihrem AWS-S3-Bucket speichert.

Service Scope
-------------

  
Der Scope definiert den Lebenszyklus erstellter Dienste. Es gibt drei Haupt-Scopes bei der Verwendung von Dependency Injection in Web-Frameworks.

### `singleton`-Scope

  
Ein Singleton-Dienst wird nur einmal erstellt, und dieselbe Instanz wird während der gesamten Lebensdauer der gesamten Anwendung wiederverwendet. Dies ist der Standard-Scope, wenn kein Scope angegeben ist.

    from injector import Module, Binder, singleton
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=singleton)
    

### `transient`-Scope

  
Ein transienter Dienst wird bei jedem Request erstellt. Jeder Request erzeugt eine neue Instanz. Dies ist nützlich für Dienste, die keinen Zustand halten oder nicht über mehrere Requests hinweg geteilt werden sollen.

    from injector import Module, Binder, noscope
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=noscope)
    

### `scoped`

  
Ein scoped-Dienst wird einmal pro Request erstellt. Für jeden eingehenden Request wird eine neue Instanz erstellt und mit allen Komponenten geteilt, die innerhalb desselben Requests von ihr abhängen. Dies ist nützlich für Dienste, die request-spezifischen Zustand halten.

  
Derzeit unterstützt Ninja Extra keine Dienste mit `scoped`-Scope.

  
Bei der Registrierung von Diensten im Dependency-Injection-Container ist die Wahl des geeigneten Scopes wichtig. `Singleton`-Dienste eignen sich für Dienste, die anwendungsweiten Zustand halten, `transient`-Dienste eignen sich für Dienste, die keinen Zustand halten, und `scoped`-Dienste eignen sich für Dienste, die request-spezifischen Zustand halten.

  
Dienste zu Controllern hinzufügen
-----------

  
Der Konstruktor des Ninja-Extra-Controllers (`__init__`) ist mit der Funktion `inject` aus der Bibliothek `injector` dekoriert. Dies ermöglicht es, Parameter mit Typannotationen im Konstruktor zu definieren, und die annotierten Typen werden bei der Objektinstanziierung injiziert.

  
Wir haben einen `BucketFileUpload`-Contract und einige konkrete Implementierungen erstellt. Fügen wir ihn zu einem Controller hinzu.

  
Erstellen wir eine `controller.py` mit dem folgenden Code

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
    

  
Jetzt haben wir eine `BucketFileUpload`-Dienstabhängigkeit für den `UserProfileController` definiert. Wir müssen das `FileServiceModule` in den Einstellungen registrieren, um eine `UnsatisfiedRequirement`-Ausnahme des Injectors zu vermeiden, wenn Ninja Extra versucht, das Objekt zu erstellen.

**Modulregistrierung**
-----------------------

  
Es gibt verschiedene Möglichkeiten, Injector-Module in einer Django-Anwendung zu registrieren.

*     
    django_injector: Wenn Sie django_injector verwenden, finden Sie in dessen Dokumentation, wie Module registriert werden.
*     
    Ninja Extra: Sie können String-Pfade von Modulen in `INJECTOR_MODULES` innerhalb des Felds `NINJA_EXTRA` angeben, wie unten gezeigt:

###   
Registrierung auf Basis von Ninja Extra

  
Wir registrieren Module im Schlüssel `INJECTOR_MODULES` innerhalb der Ninja-Extra-Einstellungen in der Django-Settings-Datei.

    NINJA_EXTRA = {
        'INJECTOR_MODULES': [
            'myproject.app1.modules.SomeModule',
            'myproject.app2.modules.SomeAppModule',
        ]
    }
    

  
Registrieren wir das Modul `FileServiceModule` in den `NinjaExtra`-Einstellungen

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
    

  
Das war es. Wir haben den Dienst `BucketFileUpload` vollständig mit dem `UserProfileController` verdrahtet.

  
!!! warning Sie können den Konstruktor Ihres APIController auch mit Parametern überschreiben, die nicht annotiert sind. Mehr zu Python Injector

Verwendung von `service_resolver`
------------------------

  
`service_resolver` ist eine Hilfsklasse, die zum Auflösen von Typen verwendet wird, die in der `injector`-Instanz registriert sind. Wir können sie verwenden, wenn wir Dienste außerhalb eines Controllers auflösen müssen.

Zum Beispiel:

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service = service_resolver(BucketFileUpload)
    bucket_service.upload_file_to_s3('/path/to/file')
    

  
Wir können auch mehrere Dienste gleichzeitig auflösen; das Ergebnis wird als Tupel zurückgegeben.

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service, service_a, service_b = service_resolver(BucketFileUpload, AnotherServiceA, AnotherServiceB)
    bucket_service.upload_file_to_s3('/path/to/file')
    
    service_a.do_something()
    service_b.do_something()
    
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
