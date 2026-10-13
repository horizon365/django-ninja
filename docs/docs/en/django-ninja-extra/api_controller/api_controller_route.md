**API Controller Route Decorators**
===================

  
The `route` class is a function decorator used to annotate Controller class functions as endpoints with a specific HTTP method.

For instance:

    from ninja_extra import route, api_controller
    
    @api_controller
    class MyController:
        @route.get('/test')
        def test(self):
            return {'message': 'test'}
    

  
`route` provides predefined methods that simplify the creation of various operations, and their names align with the corresponding HTTP methods:

*   GET: `route.get`
*   POST: `route.post`
*   PUT: `route.put`
*   DELETE: `route.delete`
*   PATCH: `route.patch`
*     
    Generic - used for operation combinations, e.g., `route.generic(methods=['POST', 'PATCH'])`

**  
Initialization Parameters**
------------

  
Below is an overview description of the parameters of the `route` class in NinjaExtra:

*     
    `path`: The required unique endpoint path string.
    
*     
    `methods`: The collection of HTTP methods required for the endpoint, e.g., `['POST', 'PUT']`.
    
*     
    `auth`: Defines the authentication method for the endpoint. Default: `NOT_SET`
    
*     
    `response`: Defines the response format as `dict[status_code, schema]` or `Schema`. Used to validate the returned response. Default: `NOT_SET`
    
*     
    `operation_id`: An optional unique identifier used to distinguish operations in path views. Default: `NOT_SET`
    
*     
    `summary`: An optional summary used to describe the endpoint. Default: `None`
    
*     
    `description`: An optional description providing additional details about the endpoint. Default: `None`
    
*     
    `tags`: A list of strings used to group endpoints for documentation purposes. Default: `None`
    
*     
    `deprecated`: An optional boolean parameter indicating whether the endpoint is deprecated. Default: `None`
    
*     
    `by_alias`: An optional parameter used to filter the `response` schema object. Default: `False`
    
*     
    `exclude_unset`: An optional parameter used to filter the `response` schema object. Default: `False`
    
*     
    `exclude_defaults`: An optional parameter used to filter the `response` schema object. Default: `False`
    
*     
    `exclude_none`: An optional parameter used to filter the `response` schema object. Default: `False`
    
*     
    `include_in_schema`: Indicates whether the endpoint should appear in Swagger documentation. Default: `True`
    
*     
    `url_name`: Provides a name for the endpoint that can be resolved using the `reverse` function in Django. Default: `None`
    
*     
    `permissions`: Defines the collection of route permission classes for the endpoint. Default: `None`
    

  
These parameters function similarly to those used when creating endpoints in Django-Ninja, but have been abstracted to work with controller classes in NinjaExtra.

**Async Route Definition**
-----------

  
In Django-Ninja-Extra, the `route` class supports defining async endpoints, similar to Django-Ninja. This feature is available for Django versions greater than 3.0.

For example:

    import asyncio
    from ninja_extra import http_get, api_controller
    
    @api_controller
    class MyController:
        @http_get("/say-after")
        async def say_after(self, delay: int, word: str):
            await asyncio.sleep(delay)
            return {'saying': word}
    

  
In this illustration, the `say_after` endpoint is defined as an asynchronous function using the `async` keyword, allowing asynchronous operations within the endpoint.

  
!!! info Read more about Django-Ninja async support

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
