依存性注入（Dependency Injection）
=====

  
Django Ninja Extra の APIController のコア機能のひとつが、Injector を使った依存性注入のサポートです。

  
たとえば、`AuthService` というサービスがあり、それを `UsersController` クラスで使いたい場合は、クラスのコンストラクタにパラメータとして追加し、その型でアノテーションするだけです。

    class UsersController(ControllerBase):
        def __init__(self, auth_service: AuthService):
            self.auth_service = auth_service
    

  
次に、アプリケーションの設定で、このサービスとそのスコープを登録します。特に指定しない限り、サービスはデフォルトでシングルトンスコープになります。

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    

  
サービスのスコープを明示的に指定することもできます。これは、同じサービスの異なるインスタンスをリクエストごとに使い分けたい場合に便利です。

    def configure(binder: Binder) -> Binder:
        binder.bind(AuthService, to=AuthServiceImpl, scope=noscope)
    

  
このようにして、コントローラにサービスを簡単に注入し、アプリケーション全体で利用できるようになります。これにより、アプリケーションの他の部分に影響を与えることなく、コントローラのテストやサービス実装の差し替えが容易になります。

  
!!! info Django-Ninja-Extra は django_injector をサポートしています。追加の設定は不要です。

サービスの作成
------------------

  
サービスとは、アプリケーションのさまざまな部分で再利用できる自己完結型のモジュールまたは機能ユニットです。サービスは通常、ビジネスロジックをカプセル化したり、共有リソース（データベースや外部 API など）へのアクセスを提供したりするために使われます。サービスは通常クラスとして実装され、オブジェクト指向のインターフェースを通じてアクセスできます。サービスは、操作の実行、外部システムとの連携、計算処理の実行に利用できます。サービスは一般に、他のオブジェクトがやり取りできる公開メソッドやプロパティをいくつか持っています。サービスはアプリケーションロジックをインフラストラクチャから分離するために使われることが多く、これによりアプリケーションロジックを独立して再利用・テスト・メンテナンスできるようになります。

  
簡単な S3 バケットサービスを作成してみましょう。プロジェクトに `service.py` を作成し、以下を追加してください。

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
    

### モジュールの作成

  
Python Injector において、モジュールとは依存性注入コンテナを設定するために使われるクラスや関数のことです。モジュールは、サービスとその実装を結び付け（バインドし）、サービスのスコープを設定する役割を担います。

  
モジュールには、依存性注入コンテナを設定するための `configure(binder: Binder)` 関数を定義できます。`binder` パラメータは Binder クラスのインスタンスで、サービスとその実装をバインドするために使われます。

  
モジュールにはまた、サービスのインスタンスを生成するためのプロバイダ関数を 1 つ以上定義することもできます。これらの関数には、解決が必要な依存関係を指定するために `@inject` を、サービスのインスタンス生成に使われることを示すために `@provider` を付与できます。

例：

    from injector import Binder, singleton, inject, provider
    
    class MyModule:
        def configure(self, binder: Binder) -> Binder:
            binder.bind(AuthService, to=AuthServiceImpl, scope=singleton)
    
        @provider
        @inject
        def provide_user_service(self, auth_service: AuthService) -> UserService:
            return UserService(auth_service)
    

  
上の例では、`MyModule` クラスに `AuthService` をバインドしスコープを `singleton` に設定する `configure` メソッドと、`@provider` と `@inject` でデコレートされ、`AuthService` を依存関係として注入されて `UserService` を提供する `provide_user_service` があります。

  
Ninja Extra の設定にモジュールを登録すると、そのモジュールで定義されたすべてのサービス・プロバイダ・設定が Injector に追加され、これらのサービスはアプリケーション全体で解決・利用できるようになります。

  
先ほど作成した `BucketFileUpload` サービス用のモジュールを作成してみましょう。プロジェクトに `module.py` を作成し、以下のコードを追加してください。

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
    

  
ここでは、`BucketFileUpload` を `InMemoryBucketFileUpload` にバインドする `FileServiceModule` を作成しました。アプリケーション内で `BucketFileUpload` を解決すると、インジェクタから提供される `InMemoryBucketFileUpload` のインスタンスが取得されます。また、`inject` デコレータを使って、`injector` から Django の設定を `InMemoryBucketFileUpload` サービスに注入しました。

  
`InMemoryBucketFileUpload` という具象クラスはシンプルな開発用クラスです。本番環境では、ファイルを AWS S3 バケットに保存するより堅牢なサービスを実装することになるでしょう。

サービススコープ
-------------

  
スコープは、生成されたサービスのライフサイクルを定義します。Web フレームワークで依存性注入を使う場合、主に 3 つのスコープがあります。

### `singleton` スコープ

  
シングルトンサービスは 1 度だけ生成され、アプリケーション全体のライフタイムを通じて同じインスタンスが再利用されます。スコープを指定しない場合のデフォルトのスコープです。

    from injector import Module, Binder, singleton
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=singleton)
    

### `transient` スコープ

  
トランジェント（一時的）サービスはリクエストごとに生成されます。各リクエストは新しいインスタンスを作成します。状態を保持しないサービスや、複数のリクエスト間で共有すべきでないサービスに便利です。

    from injector import Module, Binder, noscope
    
    class FileServiceModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(BucketFileUpload, to=InMemoryBucketFileUpload, scope=noscope)
    

### `scoped`

  
スコープドサービスはリクエストごとに 1 度生成されます。受け付けた各リクエストに対して新しいインスタンスが作成され、同じリクエスト内でそのインスタンスに依存するすべてのコンポーネント間で共有されます。リクエスト固有の状態を保持するサービスに便利です。

  
現在、Ninja Extra は `scoped` スコープのサービスをサポートしていません。

  
依存性注入コンテナにサービスを登録する際は、適切なスコープを選ぶことが重要です。`Singleton` サービスはアプリケーション全体の状態を保持するサービスに適しており、`transient` サービスは状態を保持しないサービスに、`scoped` サービスはリクエスト固有の状態を保持するサービスに適しています。

  
コントローラへのサービス追加
-----------

  
Ninja Extra のコントローラのコンストラクタ（`__init__`）は、`injector` ライブラリの `inject` 関数でデコレートされています。そのため、コンストラクタで型アノテーション付きのパラメータを定義でき、アノテーションされた型はオブジェクト生成時に注入されます。

  
`BucketFileUpload` の契約（コントラクト）といくつかの具象実装を作成しました。これをコントローラに追加してみましょう。

  
以下のコードで `controller.py` を作成します。

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
    

  
これで、`UserProfileController` に対する `BucketFileUpload` サービスの依存関係を定義できました。Ninja Extra がオブジェクトを生成しようとしたときにインジェクタから `UnsatisfiedRequirement` 例外が発生しないよう、設定に `FileServiceModule` を登録する必要があります。

**モジュールの登録**
-----------------------

  
Django アプリケーションにインジェクタのモジュールを登録する方法はいくつかあります。

*     
    django_injector: django_injector を使っている場合は、モジュールの登録方法についてのドキュメントがあります。
*     
    Ninja Extra: `NINJA_EXTRA` フィールド内の `INJECTOR_MODULES` にモジュールの文字列パスを指定できます。以下の通りです。

###   
Ninja Extra ベースの登録

  
Django の設定ファイル内の Ninja Extra 設定にある `INJECTOR_MODULES` キーにモジュールを登録します。

    NINJA_EXTRA = {
        'INJECTOR_MODULES': [
            'myproject.app1.modules.SomeModule',
            'myproject.app2.modules.SomeAppModule',
        ]
    }
    

  
`FileServiceModule` モジュールを `NinjaExtra` の設定に登録してみましょう。

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
    

  
これで完了です。`BucketFileUpload` サービスが `UserProfileController` に完全に配線されました。

  
!!! warning アノテーションされていないパラメータで APIController のコンストラクタをオーバーライドすることもできます。詳しくは Python Injector を参照してください。

`service_resolver` の使用
------------------------

  
`service_resolver` は、`injector` インスタンスに登録された型を解決するためのユーティリティクラスです。コントローラの外側でサービスを解決する必要があるときに使えます。

例：

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service = service_resolver(BucketFileUpload)
    bucket_service.upload_file_to_s3('/path/to/file')
    

  
複数のサービスを一度に解決することもでき、その場合はタプルが返されます。

    from ninja_extra import service_resolver
    from .service import BucketFileUpload
    
    
    bucket_service, service_a, service_b = service_resolver(BucketFileUpload, AnotherServiceA, AnotherServiceB)
    bucket_service.upload_file_to_s3('/path/to/file')
    
    service_a.do_something()
    service_b.do_something()
    
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
