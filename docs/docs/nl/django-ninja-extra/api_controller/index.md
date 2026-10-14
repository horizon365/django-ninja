**Controller**
==============

  
De Ninja-Extra API-controller is verantwoordelijk voor het afhandelen van inkomende requests en het teruggeven van responses aan de client.

  
In Ninja-Extra zijn er verschillende hoofdcomponenten voor het creëren van een controllermodel:

*   ControllerBase
*   APIController-decorator

ControllerBase
--------------

  
De klasse `ControllerBase` is de basisklasse voor alle controllers in Django Ninja Extra. Het biedt de kernfunctionaliteit voor het afhandelen van requests, het valideren van invoer en het teruggeven van responses op een class-based manier.

  
Deze klasse bevat attributen en methoden die gebruikelijk zijn voor alle controllers, zoals het `request`-object, `permission_classes` en het `response`-object, die deel uitmaken van de `RouteContext`. Het request-object bevat informatie over het inkomende request, zoals headers, queryparameters en body-gegevens. Het attribuut permission_classes wordt gebruikt om de machtigingen te definiëren die nodig zijn voor toegang tot de routes van de controller, terwijl het response-object wordt gebruikt om de uiteindelijke response op te bouwen die aan de client wordt teruggegeven.

  
Naast de kernattributen bevat de klasse `ControllerBase` ook hulpmethoden die kunnen worden gebruikt voor veelvoorkomende taken, zoals objectmachtigingscontroles (`check_object_permission`), het maken van snelle responses (`create_response`) en het ophalen van gegevens uit de database (`get_object_or_exception`). Deze methoden kunnen worden overschreven in subklassen om aangepast gedrag te bieden.

  
De controllerbasisklasse bevat ook een dependency injectionsysteem dat gemakkelijke toegang geeft tot andere diensten en objecten in de applicatie, zoals repository-services.

    from ninja_extra import ControllerBase, api_controller
    
    @api_controller('/users')
    class UserControllerBase(ControllerBase):
        ...
    

APIController-decorator
------------------

  
De decorator `api_controller` wordt gebruikt om class-based controllers te definiëren in Django Ninja Extra. Hij wordt toegepast op ControllerBase-klassen en accepteert meerdere parameters om de routering en functionaliteit van de controller te configureren.

  
De eerste parameter, `prefix_or_class`, is ofwel een prefix-string voor alle routes die onder de gegroepeerde controller worden geregistreerd, ofwel het klasseobject waarop de decorator wordt toegepast.

  
De tweede parameter, `auth`, is een lijst van alle Django Ninja Auth-klassen die moeten worden toegepast op de routes van de controller.

  
De derde parameter, `tags`, is een lijst met strings die worden gebruikt voor OPENAPI-tagging.

  
De vierde parameter, `permissions`, is een lijst van alle machtigingen die moeten worden toegepast op de routes van de controller.

  
De vijfde parameter, `auto_import`, staat standaard op true en voegt je controller automatisch toe aan de auto-importlijst.

bijvoorbeeld:

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
    

  
In de bovenstaande code hebben we een controller genaamd `UsersController` gedefinieerd met de decorator `api_controller`. De decorator wordt toegepast op de klasse en accepteert twee argumenten: het URL-endpoint `/users` en de klassen `auth` en `permission`. `get_users` en `create_user` zijn routefuncties die inkomende GET `/users`- en POST `/users/create`-requests afhandelen.

  
!!!info Door te erven van de ControllerBase-klasse krijg je meer IDE IntelliSense-ondersteuning.

Snel voorbeeld
-------------

  
Laten we een APIController maken om het Django-gebruikersmodel goed te beheren

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
    

  
In het bovenstaande voorbeeld definieert de klasse `UsersController` verschillende methoden die overeenkomen met verschillende HTTP-methoden, zoals `create_user`, `update_user`, `delete_user`, `list_user` en `get_user_by_id`. Deze methoden zijn respectievelijk gedecoreerd met de decorators `http_post`, `http_generic`, `http_delete` en `http_get`.

  
De methode `create_user` gebruikt de decorator `http_post` en accepteert een user-parameter van het type `UserSchema`, een `ModelSchema` die wordt gebruikt om invoergegevens te valideren en te serialiseren. Deze methode wordt gebruikt om een nieuwe gebruiker in het systeem aan te maken en geeft de `ID` van de gebruiker terug.

  
De methode `update_user` gebruikt de decorator `http_generic` en accepteert een parameter `user_id` van het type int. De decorator is geconfigureerd om de methoden `PUT` en `PATCH` af te handelen en biedt een response-parameter van het type `UserSchema` die wordt gebruikt om het gebruikersobject te serialiseren.

  
De methode `delete_user` gebruikt de decorator `http_delete` en accepteert een parameter `user_id` van het type int en een response-parameter van het type Detail, die bij succes een 204-statuscode met een lege body teruggeeft.

  
De methode `list_user` gebruikt de decorator `http_get` en is gedecoreerd met de decorator `pagination.paginate`, die de klasse `PageNumberPaginationExtra` gebruikt om de resultaten van de methode te pagineren met 50 resultaten per pagina. Hij biedt ook een response-parameter van het type `pagination.PaginatedResponseSchema[UserSchema]`, die wordt gebruikt om de door de methode teruggegeven lijst met gebruikers te serialiseren en te pagineren.

  
De methode `get_user_by_id` gebruikt de decorator `http_get` en accepteert een parameter `user_id` van het type int en een response-parameter van het type UserSchema, die wordt gebruikt om het gebruikersobject te serialiseren.

  
De gebruikerscontroller gebruikt ook `self.get_object_or_exception(self.user_model, id=user_id)`, een hulpmethode die een uitzondering genereert als het gebruikersobject niet kan worden gevonden.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
