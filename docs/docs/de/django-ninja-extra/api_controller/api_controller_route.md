**API-Controller-Route-Decorators**
===================

  
Die Klasse `route` ist ein Funktions-Decorator, der verwendet wird, um Funktionen einer Controller-Klasse als Endpunkte mit einer bestimmten HTTP-Methode zu annotieren.

Zum Beispiel:

    from ninja_extra import route, api_controller
    
    @api_controller
    class MyController:
        @route.get('/test')
        def test(self):
            return {'message': 'test'}
    

  
`route` bietet vordefinierte Methoden, die die Erstellung verschiedener Operationen vereinfachen; ihre Namen entsprechen den jeweiligen HTTP-Methoden:

*   GET: `route.get`
*   POST: `route.post`
*   PUT: `route.put`
*   DELETE: `route.delete`
*   PATCH: `route.patch`
*     
    Generic - wird für Operationenkombinationen verwendet, z. B. `route.generic(methods=['POST', 'PATCH'])`

**  
Initialisierungsparameter**
------------

  
Nachfolgend eine Übersicht über die Parameter der Klasse `route` in NinjaExtra:

*     
    `path`: Der erforderliche, eindeutige Pfad-String des Endpunkts.
    
*     
    `methods`: Die Sammlung der für den Endpunkt erforderlichen HTTP-Methoden, z. B. `['POST', 'PUT']`.
    
*     
    `auth`: Definiert die Authentifizierungsmethode für den Endpunkt. Standard: `NOT_SET`
    
*     
    `response`: Definiert das Antwortformat als `dict[status_code, schema]` oder `Schema`. Wird verwendet, um die zurückgegebene Antwort zu validieren. Standard: `NOT_SET`
    
*     
    `operation_id`: Eine optionale, eindeutige Kennung zur Unterscheidung von Operationen in Pfad-Views. Standard: `NOT_SET`
    
*     
    `summary`: Eine optionale Zusammenfassung, die den Endpunkt beschreibt. Standard: `None`
    
*     
    `description`: Eine optionale Beschreibung mit weiteren Details zum Endpunkt. Standard: `None`
    
*     
    `tags`: Eine Liste von Strings, die zum Gruppieren von Endpunkten für Dokumentationszwecke verwendet wird. Standard: `None`
    
*     
    `deprecated`: Ein optionaler boolescher Parameter, der angibt, ob der Endpunkt als veraltet gilt. Standard: `None`
    
*     
    `by_alias`: Ein optionaler Parameter zum Filtern des `response`-Schemaobjekts. Standard: `False`
    
*     
    `exclude_unset`: Ein optionaler Parameter zum Filtern des `response`-Schemaobjekts. Standard: `False`
    
*     
    `exclude_defaults`: Ein optionaler Parameter zum Filtern des `response`-Schemaobjekts. Standard: `False`
    
*     
    `exclude_none`: Ein optionaler Parameter zum Filtern des `response`-Schemaobjekts. Standard: `False`
    
*     
    `include_in_schema`: Gibt an, ob der Endpunkt in der Swagger-Dokumentation erscheinen soll. Standard: `True`
    
*     
    `url_name`: Gibt dem Endpunkt einen Namen, der mit der Funktion `reverse` in Django aufgelöst werden kann. Standard: `None`
    
*     
    `permissions`: Definiert die Sammlung der Berechtigungsklassen für die Route des Endpunkts. Standard: `None`
    

  
Diese Parameter funktionieren ähnlich wie diejenigen, die beim Erstellen von Endpunkten in Django-Ninja verwendet werden, wurden jedoch so abstrahiert, dass sie mit Controller-Klassen in NinjaExtra arbeiten.

**Definition asynchroner Routen**
-----------

  
In Django-Ninja-Extra unterstützt die Klasse `route` die Definition asynchroner Endpunkte, ähnlich wie Django-Ninja. Diese Funktion ist für Django-Versionen größer als 3.0 verfügbar.

Zum Beispiel:

    import asyncio
    from ninja_extra import http_get, api_controller
    
    @api_controller
    class MyController:
        @http_get("/say-after")
        async def say_after(self, delay: int, word: str):
            await asyncio.sleep(delay)
            return {'saying': word}
    

  
In dieser Darstellung ist der Endpunkt `say_after` als asynchrone Funktion mit dem Schlüsselwort `async` definiert, was asynchrone Operationen innerhalb des Endpunkts ermöglicht.

  
!!! info Weitere Informationen zur async-Unterstützung von Django-Ninja

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
