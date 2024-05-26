# API 文档

## OpenAPI 文档

一旦你配置了你的 Ninja API 并启动了 runserver - 请访问<a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

你将看到自动的、交互式的 API 文档(由<a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a> 提供)


## CDN 与静态文件

你不需要把django ninja 放入`INSTALLED_APPS`。在这种情况下，交互式用户界面将由 CDN 托管。

要从你自己的服务器托管文档(Js/css) - 只需将"ninja" 放入INSTALLED_APPS - 在这种情况下，标准的django 静态文件托管机制将托管它。

## 切换到Redoc


```python
from ninja import Redoc

api = NinjaAPI(docs=Redoc())

```
然后你将看到另一个自动生成的文档(由<a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a> 提供).

## 更改文档显示设置
要为 Swagger 或 Redocs 设定一些自定义设置，你可以使用 docs 类上的`settings` 参数。

```python
from ninja import Redoc, Swagger

api = NinjaAPI(docs=Swagger(settings={"persistAuthorization": True}))
...
api = NinjaAPI(docs=Redoc(settings={"disableSearch": True}))

```

其它设置请参考文档:

 - [Swagger configuration](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)
 - [Redoc configuration](https://redocly.com/docs/api-reference-docs/configuration/functionality/)



## 隐藏文档

如果你不需要显示交互式文档- 将 `docs_url` 参数设置为 `None`

```python
api = NinjaAPI(docs_url=None)
```

## 保护文档

要使用身份验证(或其它目的的装饰器)，请用`docs_decorator` 参数:

```python
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(docs_decorator=staff_member_required)
```

## 扩展 OpenAPI 规范与自定义属性

你可以使用自定义属性扩展 OpenAPI 规范，例如添加 `termsOfService`

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

## 解析文档的 URL

可以通过引用视图的名称 `openapi-view` 来反转 API 的文档视图的 URL。

在 Python 代码中，例如:
```python
from django.urls import reverse

reverse('api-1.0.0:openapi-view')

>>> '/api/docs'
```

在 Django 模板中，例如:
```Html
<a href="{% url 'api-1.0.0:openapi-view' %}">API Docs</a>

<a href="/api/docs">API Docs</a>
```

## 创建自定义文档查看器

要创建自己的 OpenAPI 视图 - 创建一个继承自 DocsBase 的类并覆盖 `render_page` 方法：



```python
form ninja.openapi.docs import DocsBase

class MyDocsViewer(DocsBase)
    def render_page(self, request, api):
        ... # return http response

...

api = NinjaAPI(docs=MyDocsViewer())

```
