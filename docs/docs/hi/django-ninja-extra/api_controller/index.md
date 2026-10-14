**Controller**
==============

  
Ninja-Extra API controller incoming requests को handle करने और client को responses return करने के लिए जिम्मेदार है।

  
Ninja-Extra में, एक controller model बनाने के लिए कई मुख्य components हैं:

*   ControllerBase
*   APIController decorator

ControllerBase
--------------

  
`ControllerBase` class Django Ninja Extra में सभी controllers के लिए base class है। यह requests को handle करने, input को validate करने, और responses को class-based तरीके से return करने की core functionality प्रदान करती है।

  
इस class में सभी controllers के लिए common attributes और methods शामिल हैं, जैसे `request` object, `permission_classes`, और `response` object, जो `RouteContext` का हिस्सा हैं। Request object में incoming request के बारे में जानकारी होती है, जैसे headers, query parameters, और body data। Permission_classes attribute का उपयोग controller की routes तक पहुँचने के लिए आवश्यक permissions परिभाषित करने के लिए किया जाता है, जबकि response object का उपयोग client को return किए जाने वाले अंतिम response को बनाने के लिए किया जाता है।

  
Core attributes के अलावा, `ControllerBase` class में utility methods भी शामिल हैं जिनका उपयोग common tasks को handle करने के लिए किया जा सकता है, जैसे object permission checks (`check_object_permission`), quick responses बनाना (`create_response`), और database से data प्राप्त करना (`get_object_or_exception`)। इन methods को custom व्यवहार प्रदान करने के लिए subclasses में override किया जा सकता है।

  
Controller base class में dependency injection system भी शामिल है जो application में अन्य services और objects तक आसान पहुँच की अनुमति देता है, जैसे repository services।

    from ninja_extra import ControllerBase, api_controller
    
    @api_controller('/users')
    class UserControllerBase(ControllerBase):
        ...
    

APIController decorator
------------------

  
`api_controller` decorator Django Ninja Extra में class-based controllers परिभाषित करने के लिए उपयोग किया जाता है। इसे ControllerBase classes पर लागू किया जाता है और यह controller की routing और functionality को configure करने के लिए कई parameters स्वीकार करता है।

  
पहला parameter, `prefix_or_class`, या तो grouped controller के अंतर्गत registered सभी routes के लिए एक prefix string है, या वह class object जिस पर decorator लागू किया जाता है।

  
दूसरा parameter, `auth`, सभी Django Ninja Auth classes की एक list है जिन्हें controller की routes पर लागू किया जाना चाहिए।

  
तीसरा parameter, `tags`, strings की एक list है जिसका उपयोग OPENAPI tagging उद्देश्यों के लिए किया जाता है।

  
चौथा parameter, `permissions`, सभी permissions की एक list है जिन्हें controller की routes पर लागू किया जाना चाहिए।

  
पाँचवाँ parameter, `auto_import`, डिफ़ॉल्ट रूप से true होता है और आपके controller को auto-import list में स्वचालित रूप से जोड़ देता है।

उदाहरण के लिए:

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
    

  
ऊपर दिए गए कोड में, हमने `api_controller` decorator का उपयोग करके `UsersController` नामक एक controller परिभाषित किया। Decorator को class पर लागू किया जाता है और यह दो arguments स्वीकार करता है, URL endpoint `/users` और `auth` तथा `permission` classes। `get_users` और `create_user` route functions हैं जो incoming GET `/users` और POST `/users/create` requests को handle करते हैं।

  
!!!info ControllerBase class से inherit करने पर आपको अधिक IDE IntelliSense support मिलता है।

Quick Example
-------------

  
चलिए Django user model को ठीक से manage करने के लिए एक APIController बनाते हैं

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
    

  
ऊपर दिए गए उदाहरण में, `UsersController` class विभिन्न HTTP methods के अनुरूप कई methods परिभाषित करती है, जैसे `create_user`, `update_user`, `delete_user`, `list_user`, और `get_user_by_id`। इन methods को क्रमशः `http_post`, `http_generic`, `http_delete`, और `http_get` decorators से decorate किया गया है।

  
`create_user` method `http_post` decorator का उपयोग करती है और `UserSchema` type का एक user parameter स्वीकार करती है, जो एक `ModelSchema` है जिसका उपयोग input data को validate और serialize करने के लिए किया जाता है। इस method का उपयोग system में एक नया user बनाने के लिए किया जाता है और यह user का `ID` return करती है।

  
`update_user` method `http_generic` decorator का उपयोग करती है और int type का एक `user_id` parameter स्वीकार करती है। Decorator को `PUT` और `PATCH` methods को handle करने के लिए configure किया गया है और यह `UserSchema` type का एक response parameter प्रदान करता है जिसका उपयोग user object को serialize करने के लिए किया जाता है।

  
`delete_user` method `http_delete` decorator का उपयोग करती है और int type का एक `user_id` parameter तथा Detail type का एक response parameter स्वीकार करती है, जो सफलता पर खाली body के साथ 204 status code return करेगा।

  
`list_user` method `http_get` decorator का उपयोग करती है और `pagination.paginate` decorator से decorate की जाती है, जो `PageNumberPaginationExtra` class का उपयोग करके method के results को 50 results प्रति page के हिसाब से paginate करता है। यह `pagination.PaginatedResponseSchema[UserSchema]` type का एक response parameter भी प्रदान करती है, जिसका उपयोग method द्वारा return की गई users की list को serialize और paginate करने के लिए किया जाएगा।

  
`get_user_by_id` method `http_get` decorator का उपयोग करती है और int type का एक `user_id` parameter तथा UserSchema type का एक response parameter स्वीकार करती है, जिसका उपयोग user object को serialize करने के लिए किया जाएगा।

  
User controller `self.get_object_or_exception(self.user_model, id=user_id)` का भी उपयोग करता है, जो एक helper method है जो यदि user object नहीं मिलता तो एक exception raise करती है।

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
