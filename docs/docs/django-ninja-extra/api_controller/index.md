**Controller**
==============

  
Ninja-Extra API 控制器负责处理传入的请求并向客户端返回响应。

  
在 Ninja-Extra 中，创建控制器模型有几个主要组成部分

*   ControllerBase
*   APIController 装饰器

ControllerBase
--------------

  
`ControllerBase` 类是 Django Ninja Extra 中所有控制器的基类。它提供了以类为基础的方法来处理请求、验证输入和返回响应的核心功能。

  
该类包括所有控制器共有的属性和方法，例如 `request` 对象、 `permission_classes` 和 `response` 对象，它们是 `RouteContext` 的一部分。请求对象包含有关传入请求的信息，例如标头、查询参数和正文数据。permission_classes 属性用于定义访问控制器路由所需的权限，而响应对象用于构建最终返回到客户端的响应。

  
除了核心属性外， `ControllerBase` 类还包含一些实用方法，可用于处理常见任务，如对象权限检查（ `check_object_permission` ）、创建快速响应（ `create_response` ）和从数据库获取数据（ `get_object_or_exception` ）。这些方法可以在子类中重写，以提供自定义行为。

  
控制器基类还包括一个依赖注入系统，该系统允许轻松访问应用程序中的其他服务和对象，例如存储库服务等。

    from ninja_extra import ControllerBase, api_controller
    
    @api_controller('/users')
    class UserControllerBase(ControllerBase):
        ...
    

APIController 装饰器
------------------

  
`api_controller` 装饰器用于在 Django Ninja Extra 中定义基于类的控制器。它应用于 ControllerBase 类，并接受多个参数来配置控制器的路由和功能。

  
第一个参数， `prefix_or_class` ，要么是分组控制器下注册的所有路由的前缀字符串，要么是装饰器应用的类对象。

  
第二个参数, `auth` , 是一个应应用于控制器路由的所有 Django Ninja Auth 类的列表。

  
第三个参数, `tags` , 是一个用于 OPENAPI 标签目的的字符串列表。

  
第四个参数, `permissions` , 是一个应应用于控制器路由的所有权限的列表。

  
第五个参数， `auto_import` ，默认值为 true，它会自动将你的控制器添加到自动导入列表中。

for example:

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
    

  
在上述代码中，我们使用 `api_controller` 装饰器定义了一个名为 `UsersController` 的控制器。装饰器应用于类，并接受两个参数，URL 端点 `/users` 和 `auth` 以及 `permission` 类。 `get_users` 和 `create_user` 是处理 GET `/users` 和 POST `/users/create` 传入请求的路由函数。

  
!!!info 从 ControllerBase 类继承可以为你提供更多的 IDE 智能感知支持。

Quick Example
-------------

  
让我们创建一个 APIController 来正确管理 Django 用户模型

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
    

  
在上面的示例中， `UsersController` 类定义了几个与不同 HTTP 方法相对应的方法，例如 `create_user` 、 `update_user` 、 `delete_user` 、 `list_user` 和 `get_user_by_id` 。这些方法分别使用 `http_post` 、 `http_generic` 、 `http_delete` 、 `http_get` 装饰器进行了装饰。

  
`create_user` 方法使用 `http_post` 装饰器，并接受一个类型为 `UserSchema` 的用户参数，该参数是一个 `ModelSchema` ，用于验证和序列化输入数据。该方法用于在系统中创建一个新用户，并返回用户的 `ID` 。

  
`update_user` 方法使用 `http_generic` 修饰符，并接受一个 `user_id` 类型为 int 的参数。修饰符被配置为处理 `PUT` 和 `PATCH` 方法，并提供一个 `UserSchema` 类型的响应参数，用于序列化用户对象。

  
`delete_user` 方法使用 `http_delete` 修饰符，并接受一个 `user_id` 类型为 int 的参数和一个 `user_id` 类型为 Detail 的响应参数，成功时将返回一个 204 状态码，带有空主体。

  
`list_user` 方法使用 `http_get` 装饰器，并使用 `pagination.paginate` 装饰器进行装饰，该装饰器使用 `PageNumberPaginationExtra` 类以每页 50 个结果的方式对方法的结果进行分页。它还提供了一个 `pagination.PaginatedResponseSchema[UserSchema]` 类型的响应参数，该参数将用于对方法返回的用户列表进行序列化和分页。

  
`get_user_by_id` 方法使用 `http_get` 装饰器，并接受一个 `user_id` 类型为 int 的参数和一个 `user_id` 类型为 UserSchema 的响应参数，该参数将用于序列化用户对象。

  
用户控制器还使用了 `self.get_object_or_exception(self.user_model, id=user_id)` ，这是一个辅助方法，如果找不到用户对象，它将引发异常。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
