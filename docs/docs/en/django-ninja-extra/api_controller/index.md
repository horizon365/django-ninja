**Controller**
==============

  
The Ninja-Extra API controller is responsible for handling incoming requests and returning responses to the client.

  
In Ninja-Extra, there are several main components to creating a controller model:

*   ControllerBase
*   APIController decorator

ControllerBase
--------------

  
The `ControllerBase` class is the base class for all controllers in Django Ninja Extra. It provides the core functionality for handling requests, validating input, and returning responses in a class-based manner.

  
This class includes attributes and methods common to all controllers, such as the `request` object, `permission_classes`, and the `response` object, which are part of the `RouteContext`. The request object contains information about the incoming request, such as headers, query parameters, and body data. The permission_classes attribute is used to define the permissions required to access the controller's routes, while the response object is used to build the final response returned to the client.

  
In addition to the core attributes, the `ControllerBase` class also contains utility methods that can be used to handle common tasks such as object permission checks (`check_object_permission`), creating quick responses (`create_response`), and fetching data from the database (`get_object_or_exception`). These methods can be overridden in subclasses to provide custom behavior.

  
The controller base class also includes a dependency injection system that allows easy access to other services and objects in the application, such as repository services.

    from ninja_extra import ControllerBase, api_controller
    
    @api_controller('/users')
    class UserControllerBase(ControllerBase):
        ...
    

APIController decorator
------------------

  
The `api_controller` decorator is used to define class-based controllers in Django Ninja Extra. It is applied to ControllerBase classes and accepts multiple parameters to configure the controller's routing and functionality.

  
The first parameter, `prefix_or_class`, is either a prefix string for all routes registered under the grouped controller, or the class object the decorator is applied to.

  
The second parameter, `auth`, is a list of all Django Ninja Auth classes that should be applied to the controller's routes.

  
The third parameter, `tags`, is a list of strings used for OPENAPI tagging purposes.

  
The fourth parameter, `permissions`, is a list of all permissions that should be applied to the controller's routes.

  
The fifth parameter, `auto_import`, defaults to true and automatically adds your controller to the auto-import list.

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
    

  
In the above code, we defined a controller named `UsersController` using the `api_controller` decorator. The decorator is applied to the class and accepts two arguments, the URL endpoint `/users` and the `auth` and `permission` classes. `get_users` and `create_user` are route functions that handle incoming GET `/users` and POST `/users/create` requests.

  
!!!info Inheriting from the ControllerBase class gives you more IDE IntelliSense support.

Quick Example
-------------

  
Let's create an APIController to properly manage the Django user model

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
    

  
In the example above, the `UsersController` class defines several methods corresponding to different HTTP methods, such as `create_user`, `update_user`, `delete_user`, `list_user`, and `get_user_by_id`. These methods are decorated with the `http_post`, `http_generic`, `http_delete`, and `http_get` decorators respectively.

  
The `create_user` method uses the `http_post` decorator and accepts a user parameter of type `UserSchema`, which is a `ModelSchema` used to validate and serialize input data. This method is used to create a new user in the system and returns the user's `ID`.

  
The `update_user` method uses the `http_generic` decorator and accepts a `user_id` parameter of type int. The decorator is configured to handle `PUT` and `PATCH` methods and provides a response parameter of type `UserSchema` used to serialize the user object.

  
The `delete_user` method uses the `http_delete` decorator and accepts a `user_id` parameter of type int and a response parameter of type Detail, which will return a 204 status code with an empty body on success.

  
The `list_user` method uses the `http_get` decorator and is decorated with the `pagination.paginate` decorator, which uses the `PageNumberPaginationExtra` class to paginate the method's results with 50 results per page. It also provides a response parameter of type `pagination.PaginatedResponseSchema[UserSchema]`, which will be used to serialize and paginate the list of users returned by the method.

  
The `get_user_by_id` method uses the `http_get` decorator and accepts a `user_id` parameter of type int and a response parameter of type UserSchema, which will be used to serialize the user object.

  
The user controller also uses `self.get_object_or_exception(self.user_model, id=user_id)`, a helper method that raises an exception if the user object cannot be found.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
