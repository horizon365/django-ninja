**Controller**
==============

  
API-контроллер Ninja-Extra отвечает за обработку входящих запросов и возврат ответов клиенту.

  
В Ninja-Extra есть несколько основных компонентов для создания модели контроллера:

*   ControllerBase
*   Декоратор APIController

ControllerBase
--------------

  
Класс `ControllerBase` является базовым классом для всех контроллеров в Django Ninja Extra. Он предоставляет основную функциональность для обработки запросов, валидации входных данных и возврата ответов в классовом стиле.

  
Этот класс включает атрибуты и методы, общие для всех контроллеров, такие как объект `request`, `permission_classes` и объект `response`, которые являются частью `RouteContext`. Объект запроса содержит информацию о входящем запросе, такую как заголовки, параметры query и данные тела. Атрибут permission_classes используется для определения разрешений, необходимых для доступа к маршрутам контроллера, а объект response используется для построения финального ответа, возвращаемого клиенту.

  
Помимо основных атрибутов, класс `ControllerBase` также содержит служебные методы, которые можно использовать для выполнения общих задач, таких как проверка разрешений на объект (`check_object_permission`), создание быстрых ответов (`create_response`) и выборка данных из базы данных (`get_object_or_exception`). Эти методы можно переопределять в подклассах для предоставления кастомного поведения.

  
Базовый класс контроллера также включает систему внедрения зависимостей, которая обеспечивает лёгкий доступ к другим сервисам и объектам приложения, например к сервисам репозиториев.

    from ninja_extra import ControllerBase, api_controller
    
    @api_controller('/users')
    class UserControllerBase(ControllerBase):
        ...
    

Декоратор APIController
------------------

  
Декоратор `api_controller` используется для определения классовых контроллеров в Django Ninja Extra. Он применяется к классам ControllerBase и принимает несколько параметров для настройки маршрутизации и функциональности контроллера.

  
Первый параметр, `prefix_or_class`, — это либо строка префикса для всех маршрутов, зарегистрированных под сгруппированным контроллером, либо объект класса, к которому применяется декоратор.

  
Второй параметр, `auth`, — это список всех классов Auth Django Ninja, которые должны применяться к маршрутам контроллера.

  
Третий параметр, `tags`, — это список строк, используемый для целей тегирования OPENAPI.

  
Четвёртый параметр, `permissions`, — это список всех разрешений, которые должны применяться к маршрутам контроллера.

  
Пятый параметр, `auto_import`, по умолчанию равен true и автоматически добавляет ваш контроллер в список автоимпорта.

например:

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
    

  
В приведённом выше коде мы определили контроллер с именем `UsersController` с помощью декоратора `api_controller`. Декоратор применяется к классу и принимает два аргумента: эндпоинт URL `/users` и классы `auth` и `permission`. `get_users` и `create_user` — это функции маршрутов, обрабатывающие входящие GET-запросы к `/users` и POST-запросы к `/users/create`.

  
!!!info Наследование от класса ControllerBase даёт вам больше поддержки IntelliSense в IDE.

Быстрый пример
-------------

  
Давайте создадим APIController для надлежащего управления моделью пользователя Django

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
    

  
В приведённом выше примере класс `UsersController` определяет несколько методов, соответствующих разным HTTP-методам, например `create_user`, `update_user`, `delete_user`, `list_user` и `get_user_by_id`. Эти методы декорированы декораторами `http_post`, `http_generic`, `http_delete` и `http_get` соответственно.

  
Метод `create_user` использует декоратор `http_post` и принимает параметр user типа `UserSchema`, который является `ModelSchema`, используемым для валидации и сериализации входных данных. Этот метод используется для создания нового пользователя в системе и возвращает его `ID`.

  
Метод `update_user` использует декоратор `http_generic` и принимает параметр `user_id` типа int. Декоратор настроен на обработку методов `PUT` и `PATCH` и предоставляет параметр response типа `UserSchema`, используемый для сериализации объекта пользователя.

  
Метод `delete_user` использует декоратор `http_delete` и принимает параметр `user_id` типа int и параметр response типа Detail, который при успехе вернёт статус-код 204 с пустым телом.

  
Метод `list_user` использует декоратор `http_get` и декорирован декоратором `pagination.paginate`, который использует класс `PageNumberPaginationExtra` для разбиения результатов метода на страницы по 50 результатов на страницу. Он также предоставляет параметр response типа `pagination.PaginatedResponseSchema[UserSchema]`, который будет использоваться для сериализации и постраничного разбиения списка пользователей, возвращаемого методом.

  
Метод `get_user_by_id` использует декоратор `http_get` и принимает параметр `user_id` типа int и параметр response типа UserSchema, который будет использоваться для сериализации объекта пользователя.

  
Контроллер пользователей также использует `self.get_object_or_exception(self.user_model, id=user_id)` — вспомогательный метод, который вызывает исключение, если объект пользователя не удаётся найти.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
