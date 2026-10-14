**Einstellungen**
=======

  
Django-Ninja-Extra verfügt über einige Einstellungen, die überschrieben werden können, indem ein Feld `NINJA_EXTRA` in der Django-Datei `settings.py` hinzugefügt und einige Schlüssel-Wert-Paare ergänzt werden, wie unten gezeigt:

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
    

  
Sie können nur überschreiben, was Sie benötigen. Es ist nicht nötig, alles zu überschreiben.

`PAGINATION_CLASS`
------------------

  
Er definiert die standardmäßig verwendete Paginator-Klasse der Decorator-Funktion `paginate`, wenn keine Paginator-Klasse definiert ist. Standard: `ninja_extra.pagination.LimitOffsetPagination`

`PAGINATION_PER_PAGE`
---------------------

  
Er definiert die standardmäßig übergebene Seitengröße, wenn `PAGINATION_CLASS` instanziiert wird. Standardwert: `100`

`INJECTOR_MODULES`
------------------

  
Er enthält eine Liste von Strings, die die Pfade zu den Injector-`Module`n definieren. Standardwert: `[]`

`THROTTLE_CLASSES`
------------------

  
Er enthält eine Liste von Strings, die die Pfade zu den Standard-Throttle-Klassen definieren. Standard: `[ "ninja_extra.throttling.AnonRateThrottle", "ninja_extra.throttling.UserRateThrottle", ]`

`THROTTLE_RATES`
----------------

  
Er enthält Schlüssel-Wert-Paare mit unterschiedlichen Throttle-Raten, die auf verschiedene `THROTTLING_CLASSES` angewendet werden. Standard: `{ 'user': '1000/day', 'anon': '100/day', }`

`ORDERING_CLASS`
----------------

  
Er definiert die standardmäßig verwendete Ordering-Klasse der Decorator-Funktion `ordering`, wenn keine Ordering-Klasse definiert ist. Standard: `ninja_extra.ordering.Ordering`

`SEARCHING_CLASS`
-----------------

  
Er definiert die standardmäßig verwendete Searching-Klasse der Decorator-Funktion `searching`, wenn keine Searching-Klasse definiert ist. Standard: `ninja_extra.searching.Searching`

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
