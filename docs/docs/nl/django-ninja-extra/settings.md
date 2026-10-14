**Instellingen**
=======

  
Django-Ninja-Extra heeft enkele instellingen die kunnen worden overschreven door een veld `NINJA_EXTRA` toe te voegen in Django `settings.py`, samen met enkele sleutel-waardeparen, zoals hieronder weergegeven:

    # Django project settings.py
    
    
    NINJA_EXTRA = {
        'PAGINATION_CLASS':"ninja_extra.pagination.PageNumberPaginationExtra",
        'PAGINATION_PER_PAGE': 100,
        'INJECTOR_MODULES': [],
        'THROTTLE_CLASSES': [
            "ninja_extra.throttling.AnonRateThrottle",
            "ninja_extra.throttling.UserRateThrottle",
        ],
        'THROTTLE_RATES': {
            'user': '1000/day',
            'anon': '100/day',
        },
        'NUM_PROXIES': None,
        'ORDERING_CLASS':"ninja_extra.ordering.Ordering",
        'SEARCHING_CLASS':"ninja_extra.searching.Search",
    }
    

  
Je hoeft alleen te overschrijven wat je nodig hebt. Er is geen noodzaak om alles te overschrijven.

`PAGINATION_CLASS`
------------------

  
Het definieert de standaard paginator-klasse die wordt gebruikt door de decoratorfunctie `paginate` wanneer er geen paginator-klasse is gedefinieerd. Standaard: `ninja_extra.pagination.LimitOffsetPagination`

`PAGINATION_PER_PAGE`
---------------------

  
Het definieert de standaard paginagrootte die wordt doorgegeven aan `PAGINATION_CLASS` bij instantiëring. Standaardwaarde: `100`

`INJECTOR_MODULES`
------------------

  
Het bevat een lijst met strings die de paden definiëren naar de injector-`Module`s. Standaardwaarde: `[]`

`THROTTLE_CLASSES`
------------------

  
Het bevat een lijst met strings die de paden definiëren naar de standaard throttle-klassen. Standaard: `[ "ninja_extra.throttling.AnonRateThrottle", "ninja_extra.throttling.UserRateThrottle", ]`

`THROTTLE_RATES`
----------------

  
Het bevat sleutel-waardeparen met verschillende throttle-tarieven die worden toegepast op verschillende `THROTTLING_CLASSES`. Standaard: `{ 'user': '1000/day', 'anon': '100/day', }`

`ORDERING_CLASS`
----------------

  
Het definieert de standaard ordering-klasse die wordt gebruikt door de decoratorfunctie `ordering` wanneer er geen ordering-klasse is gedefinieerd. Standaard: `ninja_extra.ordering.Ordering`

`SEARCHING_CLASS`
-----------------

  
Het definieert de standaard searching-klasse die wordt gebruikt door de decoratorfunctie `searching` wanneer er geen searching-klasse is gedefinieerd. Standaard: `ninja_extra.searching.Searching`

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
