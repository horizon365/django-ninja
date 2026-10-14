  
Django Ninja Extra は、リクエストのライフサイクル全体を通じて利用可能な RouteContext オブジェクトを提供します。このオブジェクトは、リクエストを処理する route ハンドラにとって重要な属性を保持しています。これらの属性には、Django の `HttpRequest` オブジェクト、route ハンドラのパーミッションクラスのリスト、Django-Ninja が最終的なレスポンスを構築するために使用する一時的なレスポンスオブジェクト、そして route 関数を呼び出すために必要な kwargs と args が含まれます。

  
これらの属性はリクエストの開始時に設定されるのではなく、route 関数の実行に至るまでのさまざまな段階をリクエストが進むにつれて利用可能になることに注意してください。

    from pydantic import BaseModel as PydanticModel, Field
    
    class RouteContext(PydanticModel):
        """
        APIController Context which will be available to the class instance when handling request
        """
    
        class Config:
            arbitrary_types_allowed = True
    
        permission_classes: PermissionType = Field([])
        request: Union[Any, HttpRequest, None] = None
        response: Union[Any, HttpResponse, None] = None
        args: List[Any] = Field([])
        kwargs: DictStrAny = Field({})
    

`RouteContext` へのアクセス方法
--------------------

  
Django Ninja Extra では、コントローラクラス内で `self.context` 属性を使って `RouteContext` オブジェクトにアクセスできます。この属性はコントローラクラスのインスタンスレベルで利用可能であり、`RouteContext` オブジェクトの属性やメソッドに簡単にアクセスできます。

たとえば、

    from ninja_extra import ControllerBase, api_controller, route
    from django.db import transaction
    from ninja_extra.permissions import IsAuthenticated
    from ninja_jwt.authentication import JWTAuth
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    
    @api_controller("/books", auth=JWTAuth(), permissions=[IsAuthenticated])
    class StoryBookSubscribeController(ControllerBase):
        @route.get(
            "/context",
            url_name="subscribe",
        )
        @transaction.atomic
        def subscribe(self):
            user = self.context.request.user
            return {'message': 'Authenticated User From context', 'email': user.email}
        
        @route.post(
            "/context",
            url_name="subscribe",
        )
        @transaction.atomic
        def subscribe_with_response_change(self):
            res = self.context.response
            res.headers.setdefault('x-custom-header', 'welcome to custom header in response')
            return {'message': 'Authenticated User From context and Response header modified', 'email': self.context.request.user.email}
    

  
この例では、コントローラクラス内で利用可能な request オブジェクトの `self.context` 属性から、認証済みの `user` オブジェクトにアクセスできます。これにより、認証されたユーザーの情報に簡単にアクセスできます。

###   
RouteContext を使ってレスポンスヘッダーを変更する

  
`RouteContext` オブジェクトは、クライアントに返される前にレスポンスデータを操作するために必要な属性とメソッドを提供します。RouteContext オブジェクトを通じて、特定のリクエストに対して返されるレスポンス内のヘッダー、ステータス、Cookie データを簡単に変更できます。

  
たとえば、新しいエンドポイントで追加の `header` 情報を加えてみましょう。以下のようになります。

    from ninja_extra import ControllerBase, api_controller, route
    from django.db import transaction
    from ninja_extra.permissions import IsAuthenticated
    from ninja_jwt.authentication import JWTAuth
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    
    @api_controller("/books", auth=JWTAuth(), permissions=[IsAuthenticated])
    class StoryBookSubscribeController(ControllerBase):
        @route.post(
            "/context-response",
            url_name="response",
        )
        @transaction.atomic
        def subscribe_with_response_change(self):
            res = self.context.response
            res.headers['x-custom-header'] = 'welcome to custom header in response'
            return {'message': 'Authenticated User From context and Response header modified', 'email': self.context.request.user.email}
    

Schema 内で `RouteContext` を使う
----------------------

  
schema のバリデーション中に、request オブジェクトにアクセスする必要がある状況が生じることがあります。Django Ninja Extra は、リクエスト中に `RouteContext` オブジェクトを解決する方法を提供することで、これを容易にします。これにより、request オブジェクトやその他必要な属性にアクセスできるようになります。これにより、バリデーションプロセス中にリクエストのコンテキストを利用でき、より柔軟で強力になります。

たとえば：

    from typing import Optional
    from django.urls import reverse
    from ninja_extra import service_resolver
    from ninja_extra.controllers import RouteContext
    from ninja import ModelSchema
    from pydantic import AnyHttpUrl, validator
    
    
    class StoreBookSchema(ModelSchema):
        borrowed_by: Optional[UserRetrieveSchema]
        store: AnyHttpUrl
        book: BookSchema
    
        class Config:
            model = StoreBook
            model_fields = ['borrowed_by', 'store', 'book']
    
        @validator("store", pre=True, check_fields=False)
        def store_validate(cls, value_data):
            context: RouteContext = service_resolver(RouteContext)
            value = reverse("store:detail", kwargs=dict(store_id=value_data.id))
            return context.request.build_absolute_uri(value)
    

  
上記の例では、依存性注入のユーティリティ関数である `service_resolver` を使って `RouteContext` オブジェクトを解決しました。これにより request オブジェクトにアクセスでき、それを使ってストア詳細の完全な URL を構築しています。`service_resolver` を使って route コンテキストにアクセスすることで、request オブジェクトに容易にアクセスし、バリデーションプロセス中に必要な情報を収集することができます。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
