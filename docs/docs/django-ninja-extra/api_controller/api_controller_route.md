**API 控制器路由装饰器**
===================

  
`route` 类是一个函数装饰器，用于将 Controller 类函数注释为具有特定 HTTP 方法的端点。

For instance:

    from ninja_extra import route, api_controller
    
    @api_controller
    class MyController:
        @route.get('/test')
        def test(self):
            return {'message': 'test'}
    

  
`route` 提供了预定义的方法，这些方法简化了各种操作的创建，并且它们的名称与相应的 HTTP 方法对齐：

*   GET: `route.get`
*   POST: `route.post`
*   PUT: `route.put`
*   DELETE: `route.delete`
*   PATCH: `route.patch`
*     
    通用 - 用于操作组合，例如 `route.generic(methods=['POST', 'PATCH'])`

**  
初始化参数**
------------

  
以下是 NinjaExtra 中 `route` 类的参数的概述描述：

*     
    `path` ：必需的唯一终结点路径字符串。
    
*     
    `methods` ：端点所需的 HTTP 方法集合，例如 `['POST', 'PUT']` 。
    
*     
    `auth` ：定义端点的身份验证方法。默认： `NOT_SET`
    
*     
    `response` ：定义响应格式为 `dict[status_code, schema]` 或 `Schema` 。用于验证返回的响应。默认： `NOT_SET`
    
*     
    `operation_id` ：可选的唯一标识符，用于区分路径视图中的操作。默认： `NOT_SET`
    
*     
    `summary` ：可选的摘要，用于描述端点。默认值： `None`
    
*     
    `description` ：可选描述，提供有关端点的其他详细信息。默认值： `None`
    
*     
    `tags` ：用于按文档目的对端点进行分组的字符串列表。默认： `None`
    
*     
    `deprecated` ：一个可选的布尔参数，表示端点是否已弃用。默认值： `None`
    
*     
    `by_alias` ：应用于筛选 `response` 架构对象的可选参数。默认： `False`
    
*     
    `exclude_unset` ：应用于筛选 `response` 架构对象的可选参数。默认： `False`
    
*     
    `exclude_defaults` ：应用于筛选 `response` 架构对象的可选参数。默认值： `False`
    
*     
    `exclude_none` ：应用于筛选 `response` 架构对象的可选参数。默认值： `False`
    
*     
    `include_in_schema` ：表示端点是否应出现在 Swagger 文档中。默认值： `True`
    
*     
    `url_name` ：为可以使用 Django 中的 `reverse` 函数解析的端点提供名称。默认值： `None`
    
*     
    `permissions` ：定义了终结点的路由权限类集合。默认： `None`
    

  
这些参数的作用类似于在 Django-Ninja 中创建端点时使用的那些参数，但已被抽象出来适用于 NinjaExtra 中的控制器类。

**异步路由定义**
-----------

  
在 Django-Ninja-Extra 中， `route` 类支持定义异步端点，类似于 Django-Ninja。此功能适用于大于 3.0 的 Django 版本。

For example:

    import asyncio
    from ninja_extra import http_get, api_controller
    
    @api_controller
    class MyController:
        @http_get("/say-after")
        async def say_after(self, delay: int, word: str):
            await asyncio.sleep(delay)
            return {'saying': word}
    

  
在这个插图中， `say_after` 端点被定义为一个使用 `async` 关键字的异步函数，允许在端点内进行异步操作。

  
!!! 信息 阅读更多关于 Django-Ninja 异步支持的内容

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
