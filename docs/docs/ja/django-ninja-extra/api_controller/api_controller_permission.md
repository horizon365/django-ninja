**API Controller のパーミッション**
================

  
パーミッションシステムの概念は、Django DRF に由来しています。

  
パーミッションチェックは、他のどのコードも実行が許可される前に、必ず route 関数の冒頭で実行されます。パーミッションチェックでは通常、`request.user` と `request.auth` 属性内の認証情報を使って、受信したリクエストを許可するかどうかを判断します。

  
パーミッションは、異なるクラスのユーザーに対して API のさまざまな部分へのアクセスを許可または拒否するために使用されます。

  
最もシンプルなパーミッションスタイルは、認証された任意のユーザーにはアクセスを許可し、認証されていないユーザーにはアクセスを拒否するものです。これは Django Ninja Extra の `IsAuthenticated` クラスに相当します。

  
もう少し緩いパーミッションスタイルは、認証されたユーザーにはフルアクセスを許可し、認証されていないユーザーには読み取り専用アクセスを許可するものです。これは Django Ninja Extra の `IsAuthenticatedOrReadOnly` クラスに相当します。

### **オブジェクトレベルパーミッションの制限**

  
リクエストを処理する際、route 関数のパーミッションリストで指定されたすべてのパーミッションに対して、`has_permission` メソッドが自動的に呼び出されます。しかし、`has_object_permission` はパーミッション検証のためにオブジェクトを必要とするため、トリガーされません。したがって、コントローラ内で `get_object_or_exception` または `get_object_or_none` メソッドを使ってオブジェクトを取得するときに、`has_object_permission` パーミッションメソッドが呼び出されることになります。

**カスタムパーミッション**
----------

  
カスタムパーミッションを実装するには、`BasePermission` を継承し、以下のメソッドの一方または両方を実装します：

    .has_permission(self, request: HttpRequest, controller: "APIController")
    .has_object_permission(self, request: HttpRequest, controller: "APIController", obj: Any)
    

例

    from ninja_extra import permissions, api_controller, http_get
    
    class ReadOnly(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.method in permissions.SAFE_METHODS
    
    @api_controller(permissions=[permissions.IsAuthenticated | ReadOnly])
    class PermissionController:
        @http_get('/must_be_authenticated', permissions=[permissions.IsAuthenticated])
        def must_be_authenticated(self, word: str):
            return dict(says=word)
    

**  
サポートされているパーミッション演算子**
---------------

*   & (and) 例： `permissions.IsAuthenticated & ReadOnly`
*   | (or) 例： `permissions.IsAuthenticated | ReadOnly`
*   ~ (not) 例： `~(permissions.IsAuthenticated & ReadOnly)`

**  
コントローラでのパーミッションオブジェクトの使用**
------------------

  
Ninja-Extra のパーミッションシステムは、パーミッションを定義する際に柔軟性を提供し、パーミッションクラスのインスタンスまたは型のいずれかとしてパーミッションを定義できるようにしています。

  
以下の例では、`ReadOnly` クラスが `permissions.BasePermission` のサブクラスとして定義され、そのインスタンスが `api_controller` デコレータの `permissions` パラメータに渡されています。

    from ninja_extra import permissions, api_controller, ControllerBase
    
    class ReadOnly(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.method in permissions.SAFE_METHODS
    
    @api_controller(permissions=[permissions.IsAuthenticated | ReadOnly()])
    class SampleController(ControllerBase):
        pass
    

  
提供されている例では、`UserWithPermission` クラスを使って、コントローラや route 関数ごとに異なるパーミッションを評価しています。

たとえば：

    from ninja_extra import permissions, api_controller, ControllerBase, http_post, http_delete
    
    class UserWithPermission(permissions.BasePermission):
        def __init__(self, permission: str) -> None:
            self._permission = permission
        
        def has_permission(self, request, view):
            return request.user.has_perm(self._permission)
    
    
    @api_controller('/blog')
    class BlogController(ControllerBase):
        @http_post('/', permissions=[permissions.IsAuthenticated & UserWithPermission('blog.add')])
        def add_blog(self):
            pass
        
        @http_delete('/', permissions=[permissions.IsAuthenticated & UserWithPermission('blog.delete')])
        def delete_blog(self):
            pass
    

  
この場合、`UserWithPermission` クラスは、ユーザーが `add_blog` アクションにアクセスするための `blog.add` パーミッションと、`delete_blog` アクションにアクセスするための `blog.delete` パーミッションを持っているかどうかを検証するために使用されています。パーミッションは各 route 関数に対して明示的に設定されており、特定のパーミッションに基づくユーザーアクセスのきめ細かい制御が可能になっています。

**AllowAny**
------------

  
`AllowAny` パーミッションクラスは、リクエストが認証されているかどうかにかかわらず、無制限のアクセスを許可します。このパーミッションクラスの使用は必須ではありません。パーミッションを空のリストまたはタプルに設定すれば同じ結果が得られるためです。しかし、`AllowAny` クラスを明示的に指定することは、無制限のアクセスを許可する意図を明確に伝えられるという点で有用です。

**IsAuthenticated**
-------------

  
`IsAuthenticated` パーミッションクラスは、認証されていないユーザーにはパーミッションを拒否し、認証されたユーザーにはパーミッションを付与します。

  
API へのアクセスを登録ユーザーのみに制限したい場合、このパーミッションが適切です。

**IsAdminUser**
---------------

  
`IsAdminUser` パーミッションクラスは、`user.is_staff` が `True` である場合を除き、すべてのユーザーに対してパーミッションを拒否します。`True` の場合にはパーミッションが付与されます。

  
API へのアクセスを特定の信頼された管理者のサブセットのみに制限したい場合、このパーミッションが適切です。

**  
IsAuthenticatedOrReadOnly**
---------------

  
`IsAuthenticatedOrReadOnly` パーミッションクラスは、認証されたユーザーには任意のリクエストを許可します。認証されていないユーザーについては、メソッドが「安全な」メソッド（つまり GET、HEAD、または OPTIONS）である場合にのみリクエストが許可されます。

  
API で匿名ユーザーに読み取りパーミッションを付与しつつ、書き込みパーミッションを認証されたユーザーに制限したい場合、このパーミッションが適切です。
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
