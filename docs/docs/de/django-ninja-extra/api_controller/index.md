**Controller**
==============

  
Der Ninja-Extra-API-Controller ist dafür verantwortlich, eingehende Anfragen zu verarbeiten und Antworten an den Client zurückzugeben.

  
In Ninja-Extra gibt es mehrere Hauptkomponenten für die Erstellung eines Controller-Modells:

*   ControllerBase
*   APIController-Decorator

ControllerBase
--------------

  
Die Klasse `ControllerBase` ist die Basisklasse für alle Controller in Django Ninja Extra. Sie stellt die Kernfunktionalität für die Verarbeitung von Anfragen, die Validierung von Eingaben und die Rückgabe von Antworten auf klassenbasierte Weise bereit.

  
Diese Klasse enthält Attribute und Methoden, die allen Controllern gemeinsam sind, wie das `request`-Objekt, `permission_classes` und das `response`-Objekt, die Teil des `RouteContext` sind. Das request-Objekt enthält Informationen über die eingehende Anfrage, wie Header, Query-Parameter und Body-Daten. Das Attribut permission_classes wird verwendet, um die Berechtigungen zu definieren, die für den Zugriff auf die Routen des Controllers erforderlich sind, während das response-Objekt verwendet wird, um die endgültige, an den Client zurückgegebene Antwort zu erstellen.

  
Zusätzlich zu den Kernattributen enthält die Klasse `ControllerBase` auch Hilfsmethoden, die zur Erledigung häufiger Aufgaben verwendet werden können, wie Objektberechtigungsprüfungen (`check_object_permission`), das Erstellen schneller Antworten (`create_response`) und das Abrufen von Daten aus der Datenbank (`get_object_or_exception`). Diese Methoden können in Unterklassen überschrieben werden, um benutzerdefiniertes Verhalten bereitzustellen.

  
Die Controller-Basisklasse enthält auch ein Dependency-Injection-System, das einen einfachen Zugriff auf andere Dienste und Objekte der Anwendung ermöglicht, wie zum Beispiel Repository-Dienste.

    from ninja_extra import ControllerBase, api_controller
    
    @api_controller('/users')
    class UserControllerBase(ControllerBase):
        ...
    

APIController-Decorator
------------------

  
Der Decorator `api_controller` wird verwendet, um klassenbasierte Controller in Django Ninja Extra zu definieren. Er wird auf ControllerBase-Klassen angewendet und akzeptiert mehrere Parameter, um das Routing und die Funktionalität des Controllers zu konfigurieren.

  
Der erste Parameter, `prefix_or_class`, ist entweder ein Präfix-String für alle Routen, die unter dem gruppierten Controller registriert sind, oder das Klassenobjekt, auf das der Decorator angewendet wird.

  
Der zweite Parameter, `auth`, ist eine Liste aller Django-Ninja-Auth-Klassen, die auf die Routen des Controllers angewendet werden sollen.

  
Der dritte Parameter, `tags`, ist eine Liste von Strings, die für OPENAPI-Tagging-Zwecke verwendet wird.

  
Der vierte Parameter, `permissions`, ist eine Liste aller Berechtigungen, die auf die Routen des Controllers angewendet werden sollen.

  
Der fünfte Parameter, `auto_import`, ist standardmäßig true und fügt Ihren Controller automatisch zur Auto-Import-Liste hinzu.

zum Beispiel:

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
    

  
Im obigen Code haben wir mit dem Decorator `api_controller` einen Controller namens `UsersController` definiert. Der Decorator wird auf die Klasse angewendet und akzeptiert zwei Argumente: den URL-Endpunkt `/users` sowie die Klassen `auth` und `permission`. `get_users` und `create_user` sind Routen-Funktionen, die eingehende GET-`/users`- bzw. POST-`/users/create`-Anfragen verarbeiten.

  
!!!info Die Vererbung von der Klasse ControllerBase bietet Ihnen mehr IDE-IntelliSense-Unterstützung.

Kurzes Beispiel
-------------

  
Lassen Sie uns einen APIController erstellen, um das Django-Benutzermodell ordnungsgemäß zu verwalten

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
    

  
Im obigen Beispiel definiert die Klasse `UsersController` mehrere Methoden, die verschiedenen HTTP-Methoden entsprechen, wie `create_user`, `update_user`, `delete_user`, `list_user` und `get_user_by_id`. Diese Methoden sind jeweils mit den Decorators `http_post`, `http_generic`, `http_delete` und `http_get` versehen.

  
Die Methode `create_user` verwendet den Decorator `http_post` und nimmt einen Parameter `user` vom Typ `UserSchema` entgegen, der ein `ModelSchema` ist, das zur Validierung und Serialisierung der Eingabedaten verwendet wird. Diese Methode wird verwendet, um einen neuen Benutzer im System zu erstellen, und gibt die `ID` des Benutzers zurück.

  
Die Methode `update_user` verwendet den Decorator `http_generic` und nimmt einen Parameter `user_id` vom Typ int entgegen. Der Decorator ist so konfiguriert, dass er die Methoden `PUT` und `PATCH` verarbeitet, und stellt einen Response-Parameter vom Typ `UserSchema` bereit, der zur Serialisierung des Benutzerobjekts verwendet wird.

  
Die Methode `delete_user` verwendet den Decorator `http_delete` und nimmt einen Parameter `user_id` vom Typ int sowie einen Response-Parameter vom Typ Detail entgegen; bei Erfolg wird ein Statuscode 204 mit leerem Body zurückgegeben.

  
Die Methode `list_user` verwendet den Decorator `http_get` und ist zusätzlich mit dem Decorator `pagination.paginate` versehen, der die Klasse `PageNumberPaginationExtra` verwendet, um die Ergebnisse der Methode mit 50 Ergebnissen pro Seite zu paginieren. Er stellt außerdem einen Response-Parameter vom Typ `pagination.PaginatedResponseSchema[UserSchema]` bereit, der verwendet wird, um die von der Methode zurückgegebene Benutzerliste zu serialisieren und zu paginieren.

  
Die Methode `get_user_by_id` verwendet den Decorator `http_get` und nimmt einen Parameter `user_id` vom Typ int sowie einen Response-Parameter vom Typ UserSchema entgegen, der zur Serialisierung des Benutzerobjekts verwendet wird.

  
Der Benutzer-Controller verwendet außerdem `self.get_object_or_exception(self.user_model, id=user_id)`, eine Hilfsmethode, die eine Ausnahme auslöst, wenn das Benutzerobjekt nicht gefunden werden kann.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
