**API Controller のルートデコレータ**
===================

  
`route` クラスは、Controller クラスの関数を特定の HTTP メソッドを持つエンドポイントとしてアノテーションするために使用される関数デコレータです。

たとえば：

    from ninja_extra import route, api_controller
    
    @api_controller
    class MyController:
        @route.get('/test')
        def test(self):
            return {'message': 'test'}
    

  
`route` は、さまざまな操作の作成を簡素化する定義済みメソッドを提供しており、その名前は対応する HTTP メソッドと一致しています：

*   GET: `route.get`
*   POST: `route.post`
*   PUT: `route.put`
*   DELETE: `route.delete`
*   PATCH: `route.patch`
*     
    Generic - 操作の組み合わせに使用します。例： `route.generic(methods=['POST', 'PATCH'])`

**  
初期化パラメータ**
------------

  
以下は、NinjaExtra の `route` クラスのパラメータの概要説明です：

*     
    `path`: 必須の一意なエンドポイントパス文字列。
    
*     
    `methods`: エンドポイントに必要な HTTP メソッドのコレクション。例： `['POST', 'PUT']`。
    
*     
    `auth`: エンドポイントの認証方法を定義します。デフォルト： `NOT_SET`
    
*     
    `response`: レスポンス形式を `dict[status_code, schema]` または `Schema` として定義します。返されるレスポンスの検証に使用されます。デフォルト： `NOT_SET`
    
*     
    `operation_id`: パスビュー内の操作を区別するために使用される、オプションの一意な識別子。デフォルト： `NOT_SET`
    
*     
    `summary`: エンドポイントを記述するために使用される、オプションの概要。デフォルト： `None`
    
*     
    `description`: エンドポイントに関する追加情報を提供する、オプションの説明。デフォルト： `None`
    
*     
    `tags`: ドキュメントの目的でエンドポイントをグループ化するために使用される文字列のリスト。デフォルト： `None`
    
*     
    `deprecated`: エンドポイントが非推奨かどうかを示す、オプションのブール型パラメータ。デフォルト： `None`
    
*     
    `by_alias`: `response` の schema オブジェクトをフィルタリングするために使用される、オプションのパラメータ。デフォルト： `False`
    
*     
    `exclude_unset`: `response` の schema オブジェクトをフィルタリングするために使用される、オプションのパラメータ。デフォルト： `False`
    
*     
    `exclude_defaults`: `response` の schema オブジェクトをフィルタリングするために使用される、オプションのパラメータ。デフォルト： `False`
    
*     
    `exclude_none`: `response` の schema オブジェクトをフィルタリングするために使用される、オプションのパラメータ。デフォルト： `False`
    
*     
    `include_in_schema`: エンドポイントを Swagger ドキュメントに表示するかどうかを示します。デフォルト： `True`
    
*     
    `url_name`: Django の `reverse` 関数を使って解決できるエンドポイントの名前を提供します。デフォルト： `None`
    
*     
    `permissions`: エンドポイントのルートパーミッションクラスのコレクションを定義します。デフォルト： `None`
    

  
これらのパラメータは、Django-Ninja でエンドポイントを作成する際に使用されるものと同様に機能しますが、NinjaExtra のコントローラクラスと連携できるように抽象化されています。

**非同期ルートの定義**
-----------

  
Django-Ninja-Extra では、`route` クラスは Django-Ninja と同様に非同期エンドポイントの定義をサポートしています。この機能は Django バージョン 3.0 より大きい場合に利用可能です。

たとえば：

    import asyncio
    from ninja_extra import http_get, api_controller
    
    @api_controller
    class MyController:
        @http_get("/say-after")
        async def say_after(self, delay: int, word: str):
            await asyncio.sleep(delay)
            return {'saying': word}
    

  
この例では、`say_after` エンドポイントが `async` キーワードを使って非同期関数として定義されており、エンドポイント内で非同期操作を行うことができます。

  
!!! info Django-Ninja の async サポートについて詳しく読む

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
