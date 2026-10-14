---
comments: true
---
# API ドキュメント

## OpenAPI ドキュメント

Ninja API を設定して runserver を起動したら - <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a> にアクセスしてください

自動生成されたインタラクティブな API ドキュメント（<a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a> による）が表示されます


## CDN と静的ファイル

django ninja を `INSTALLED_APPS` に追加する必要はありません。この場合、インタラクティブな UI は CDN からホストされます。

ドキュメント（Js/css）を自分のサーバーからホストするには - 単に `"ninja"` を INSTALLED_APPS に追加するだけです - この場合、Django の標準的な静的ファイルホスティングの仕組みによってホストされます。

## Redoc への切り替え


```python
from ninja import Redoc

api = NinjaAPI(docs=Redoc())

```
すると、別の自動生成ドキュメント（<a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a> による）が表示されます。

## ドキュメントの表示設定を変更する

Swagger や Redoc にカスタム設定を指定するには、docs クラスの `settings` 引数を使用します。

```python
from ninja import Redoc, Swagger

api = NinjaAPI(docs=Swagger(settings={"persistAuthorization": True}))
...
api = NinjaAPI(docs=Redoc(settings={"disableSearch": True}))

```

その他の設定については、ドキュメントを参照してください:

 - [Swagger の設定](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)
 - [Redoc の設定](https://redocly.com/docs/api-reference-docs/configuration/functionality/)



## ドキュメントを非表示にする

インタラクティブなドキュメントを表示する必要がない場合は - `docs_url` 引数を `None` に設定してください

```python
api = NinjaAPI(docs_url=None)
```

## ドキュメントを保護する

認証（または他の目的のための任意のデコレータ）を使用するには、`docs_decorator` 引数を使用します:

```python
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(docs_decorator=staff_member_required)
```

## OpenAPI スキーマをカスタム属性で拡張する

OpenAPI スキーマをカスタム属性で拡張できます。たとえば `termsOfService` を追加する場合は次のようになります

```python
api = NinjaAPI(
   openapi_extra={
       "info": {
           "termsOfService": "https://example.com/terms/",
       }
   },
   title="Demo API",
   description="This is a demo API with dynamic OpenAPI info section"
)
```

## ドキュメント URL の解決

API のドキュメントビューの URL は、ビュー名 `openapi-view` を参照して逆引きできます。

Python コードでは、たとえば次のようにします:
```python
from django.urls import reverse

reverse('api-1.0.0:openapi-view')

>>> '/api/docs'
```

Django テンプレートでは、たとえば次のようにします:
```Html
<a href="{% url 'api-1.0.0:openapi-view' %}">API Docs</a>

<a href="/api/docs">API Docs</a>
```

## カスタムドキュメントビューアを作成する

独自の OpenAPI ビューを作成するには - DocsBase を継承したクラスを作成し、`render_page` メソッドをオーバーライドします:



```python
from ninja.openapi.docs import DocsBase

class MyDocsViewer(DocsBase):
    def render_page(self, request, api):
        ... # return http response

...

api = NinjaAPI(docs=MyDocsViewer())

```

!!! success

    次のセクション **[エラーハンドリング](errors.md)** に進みましょう

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
