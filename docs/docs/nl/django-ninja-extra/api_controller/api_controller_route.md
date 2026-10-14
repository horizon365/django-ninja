**API Controller-route-decorators**
===================

  
De klasse `route` is een functiedecorator die wordt gebruikt om functies van Controller-klassen te annoteren als endpoints met een specifieke HTTP-methode.

Bijvoorbeeld:

    from ninja_extra import route, api_controller
    
    @api_controller
    class MyController:
        @route.get('/test')
        def test(self):
            return {'message': 'test'}
    

  
`route` biedt vooraf gedefinieerde methoden die het creëren van verschillende operaties vereenvoudigen, en hun namen komen overeen met de bijbehorende HTTP-methoden:

*   GET: `route.get`
*   POST: `route.post`
*   PUT: `route.put`
*   DELETE: `route.delete`
*   PATCH: `route.patch`
*     
    Generic — gebruikt voor combinaties van operaties, bijv. `route.generic(methods=['POST', 'PATCH'])`

**  
Initialisatieparameters**
------------

  
Hieronder een overzicht van de parameters van de klasse `route` in NinjaExtra:

*     
    `path`: de vereiste unieke endpoint-padstring.
    
*     
    `methods`: de verzameling HTTP-methoden die voor het endpoint vereist is, bijv. `['POST', 'PUT']`.
    
*     
    `auth`: definieert de authenticatiemethode voor het endpoint. Standaard: `NOT_SET`
    
*     
    `response`: definieert het responsformaat als `dict[status_code, schema]` of `Schema`. Wordt gebruikt om de geretourneerde response te valideren. Standaard: `NOT_SET`
    
*     
    `operation_id`: een optionele unieke identificatie om operaties in path views te onderscheiden. Standaard: `NOT_SET`
    
*     
    `summary`: een optionele samenvatting om het endpoint te beschrijven. Standaard: `None`
    
*     
    `description`: een optionele beschrijving met aanvullende details over het endpoint. Standaard: `None`
    
*     
    `tags`: een lijst met strings die endpoints groeperen voor documentatiedoeleinden. Standaard: `None`
    
*     
    `deprecated`: een optionele booleaanse parameter die aangeeft of het endpoint verouderd is. Standaard: `None`
    
*     
    `by_alias`: een optionele parameter om het `response`-schemaobject te filteren. Standaard: `False`
    
*     
    `exclude_unset`: een optionele parameter om het `response`-schemaobject te filteren. Standaard: `False`
    
*     
    `exclude_defaults`: een optionele parameter om het `response`-schemaobject te filteren. Standaard: `False`
    
*     
    `exclude_none`: een optionele parameter om het `response`-schemaobject te filteren. Standaard: `False`
    
*     
    `include_in_schema`: geeft aan of het endpoint in de Swagger-documentatie moet verschijnen. Standaard: `True`
    
*     
    `url_name`: geeft het endpoint een naam die kan worden opgelost met de functie `reverse` in Django. Standaard: `None`
    
*     
    `permissions`: definieert de verzameling routemachtigingsklassen voor het endpoint. Standaard: `None`
    

  
Deze parameters werken vergelijkbaar met de parameters die worden gebruikt bij het creëren van endpoints in Django-Ninja, maar zijn geabstraheerd om te werken met controllerklassen in NinjaExtra.

**Asynchrone routedefinitie**
-----------

  
In Django-Ninja-Extra ondersteunt de klasse `route` het definiëren van async-endpoints, vergelijkbaar met Django-Ninja. Deze functie is beschikbaar voor Django-versies groter dan 3.0.

Bijvoorbeeld:

    import asyncio
    from ninja_extra import http_get, api_controller
    
    @api_controller
    class MyController:
        @http_get("/say-after")
        async def say_after(self, delay: int, word: str):
            await asyncio.sleep(delay)
            return {'saying': word}
    

  
In deze illustratie is het endpoint `say_after` gedefinieerd als een asynchrone functie met het sleutelwoord `async`, waardoor asynchrone bewerkingen binnen het endpoint mogelijk zijn.

  
!!! info Lees meer over async-ondersteuning in Django-Ninja

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
