**コントローラ**
==============

  
Ninja-Extra の API コントローラは、受信したリクエストを処理し、クライアントへレスポンスを返す役割を担います。

  
Ninja-Extra には、コントローラモデルを作成するための主要なコンポーネントがいくつかあります：

*   ControllerBase
*   APIController デコレータ

ControllerBase
--------------

  
`ControllerBase` クラスは、Django Ninja Extra におけるすべてのコントローラの基底クラスです。リクエストの処理、入力の検証、レスポンスの返却といったコア機能を、クラスベースの方法で提供します。

  
このクラスには、すべてのコントローラに共通する属性とメソッドが含まれています。たとえば `request` オブジェクト、`permission_classes`、`response` オブジェクトなどで、これらは `RouteContext` の一部です。request オブジェクトには、ヘッダー、クエリパラメータ、ボディデータといった受信リクエストの情報が含まれます。permission_classes 属性は、コントローラのルートにアクセスするために必要なパーミッションを定義するために使用され、response オブジェクトはクライアントに返される最終的なレスポンスを構築するために使用されます。

  
コア属性に加えて、`ControllerBase` クラスには、オブジェクトパーミッションのチェック（`check_object_permission`）、クイックレスポンスの作成（`create_response`）、データベースからのデータ取得（`get_object_or_exception`）といった共通タスクを処理するために使用できるユーティリティメソッドも含まれています。これらのメソッドは、サブクラスでオーバーライドしてカスタムの挙動を提供できます。

  
コントローラの基底クラスには、リポジトリサービスのようなアプリケーション内の他のサービスやオブジェクトに容易にアクセスできる依存性注入システムも含まれています。

    from ninja_extra import ControllerBase, api_controller
    
    @api_controller('/users')
    class UserControllerBase(ControllerBase):
        ...
    

APIController デコレータ
------------------

  
`api_controller` デコレータは、Django Ninja Extra でクラスベースのコントローラを定義するために使用されます。ControllerBase クラスに適用され、コントローラのルーティングと機能を設定するための複数のパラメータを受け入れます。

  
最初のパラメータ `prefix_or_class` は、グループ化されたコントローラの下に登録されるすべてのルートのプレフィックス文字列、またはデコレータが適用されるクラスオブジェクトのいずれかです。

  
2 番目のパラメータ `auth` は、コントローラのルートに適用されるべきすべての Django Ninja Auth クラスのリストです。

  
3 番目のパラメータ `tags` は、OPENAPI のタグ付けに使用される文字列のリストです。

  
4 番目のパラメータ `permissions` は、コントローラのルートに適用されるべきすべてのパーミッションのリストです。

  
5 番目のパラメータ `auto_import` はデフォルトで true であり、コントローラを自動インポートリストに自動的に追加します。

たとえば：

    import typing
    from ninja_extra import api_controller, ControllerBase, permissions, route
    from django.contrib.auth.models import User
    from ninja.security import APIKeyQuery
    from ninja import ModelSchema
    
    
    class UserSchema(ModelSchema):
        class Config:
            model = User
            model_fields = ['username', 'email', 'first_name']
    
    
    @api_controller('users/', auth=[APIKeyQuery()], permissions=[permissions.IsAuthenticated])
    class UsersController(ControllerBase):
        @route.get('', response={200: typing.List[UserSchema]})
        def get_users(self):
            # Logic to handle GET request to the /users endpoint
            users = User.objects.all()
            return users
    
        @route.post('create/', response={200: UserSchema})
        def create_user(self, payload: UserSchema):
            # Logic to handle POST request to the /users endpoint
            new_user = User.objects.create(
                username=payload.username,
                email=payload.email,
                first_name=payload.first_name,
            )
            new_user.set_password('password')
            return new_user
    

  
上記のコードでは、`api_controller` デコレータを使って `UsersController` という名前のコントローラを定義しました。デコレータはクラスに適用され、URL エンドポイント `/users` と `auth` クラスおよび `permission` クラスという 2 つの引数を受け入れています。`get_users` と `create_user` は、GET `/users` と POST `/users/create` のリクエストを処理する route 関数です。

  
!!!info ControllerBase クラスを継承すると、より多くの IDE インテリセンスのサポートが得られます。

クイック例
-------------

  
Django のユーザーモデルを適切に管理する APIController を作成してみましょう

    import uuid
    from ninja import ModelSchema
    from ninja_extra import (
        http_get, http_post, http_generic, http_delete,
        api_controller, status, ControllerBase, pagination
    )
    from ninja_extra.controllers.response import Detail
    from django.contrib.auth import get_user_model
    
    
    class UserSchema(ModelSchema):
        class Config:
            model = get_user_model()
            model_fields = ['username', 'email', 'first_name']
    
    
    @api_controller('/users')
    class UsersController(ControllerBase):
        user_model = get_user_model()
    
        @http_post()
        def create_user(self, user: UserSchema):
            # just simulating created user
            return dict(id=uuid.uuid4())
    
        @http_generic('/{int:user_id}', methods=['put', 'patch'], response=UserSchema)
        def update_user(self, user_id: int):
            """ Django Ninja will serialize Django ORM model to schema provided as `response`"""
            user = self.get_object_or_exception(self.user_model, id=user_id)
            return user
    
        @http_delete('/{int:user_id}', response=Detail(status_code=status.HTTP_204_NO_CONTENT))
        def delete_user(self, user_id: int):
            user = self.get_object_or_exception(self.user_model, id=user_id)
            user.delete()
            return self.create_response('', status_code=status.HTTP_204_NO_CONTENT)
    
        @http_get("", response=pagination.PaginatedResponseSchema[UserSchema])
        @pagination.paginate(pagination.PageNumberPaginationExtra, page_size=50)
        def list_user(self):
            return self.user_model.objects.all()
    
        @http_get('/{user_id}', response=UserSchema)
        def get_user_by_id(self, user_id: int):
            user = self.get_object_or_exception(self.user_model, id=user_id)
            return user
    

  
上記の例では、`UsersController` クラスが、`create_user`、`update_user`、`delete_user`、`list_user`、`get_user_by_id` など、異なる HTTP メソッドに対応する複数のメソッドを定義しています。これらのメソッドは、それぞれ `http_post`、`http_generic`、`http_delete`、`http_get` デコレータで装飾されています。

  
`create_user` メソッドは `http_post` デコレータを使用し、`UserSchema` 型の user パラメータを受け入れます。`UserSchema` は、入力データの検証とシリアライズに使用される `ModelSchema` です。このメソッドはシステムに新しいユーザーを作成するために使用され、ユーザーの `ID` を返します。

  
`update_user` メソッドは `http_generic` デコレータを使用し、int 型の `user_id` パラメータを受け入れます。このデコレータは `PUT` と `PATCH` メソッドを処理するように設定されており、ユーザーオブジェクトのシリアライズに使用される `UserSchema` 型の response パラメータを提供します。

  
`delete_user` メソッドは `http_delete` デコレータを使用し、int 型の `user_id` パラメータと Detail 型の response パラメータを受け入れます。成功した場合、空のボディとともに 204 ステータスコードを返します。

  
`list_user` メソッドは `http_get` デコレータを使用し、`pagination.paginate` デコレータで装飾されています。このデコレータは `PageNumberPaginationExtra` クラスを使って、メソッドの結果を 1 ページあたり 50 件でページネーションします。また、`pagination.PaginatedResponseSchema[UserSchema]` 型の response パラメータも提供されており、これがメソッドから返されるユーザーリストのシリアライズとページネーションに使用されます。

  
`get_user_by_id` メソッドは `http_get` デコレータを使用し、int 型の `user_id` パラメータと UserSchema 型の response パラメータを受け入れます。response パラメータはユーザーオブジェクトのシリアライズに使用されます。

  
ユーザーコントローラは `self.get_object_or_exception(self.user_model, id=user_id)` も使用しています。これは、ユーザーオブジェクトが見つからない場合に例外を発生させるヘルパーメソッドです。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
