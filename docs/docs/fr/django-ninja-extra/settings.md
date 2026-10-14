**Paramètres**
=======

  
Django-Ninja-Extra dispose de certains paramètres qui peuvent être redéfinis en ajoutant un champ `NINJA_EXTRA` dans le fichier `settings.py` de Django et en y ajoutant des paires clé-valeur, comme indiqué ci-dessous :

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
    

  
Vous ne pouvez redéfinir que ce dont vous avez besoin. Il n'est pas nécessaire de tout redéfinir.

`PAGINATION_CLASS`
------------------

  
Il définit la classe de pagination par défaut utilisée par la fonction décoratrice `paginate` lorsqu'aucune classe de pagination n'est définie. Par défaut : `ninja_extra.pagination.LimitOffsetPagination`

`PAGINATION_PER_PAGE`
---------------------

  
Il définit la taille de page par défaut transmise à `PAGINATION_CLASS` lors de son instanciation. Valeur par défaut : `100`

`INJECTOR_MODULES`
------------------

  
Il contient une liste de chaînes définissant les chemins vers les `Module`s injector. Valeur par défaut : `[]`

`THROTTLE_CLASSES`
------------------

  
Il contient une liste de chaînes définissant les chemins vers les classes de throttling par défaut. Par défaut : `[ "ninja_extra.throttling.AnonRateThrottle", "ninja_extra.throttling.UserRateThrottle", ]`

`THROTTLE_RATES`
----------------

  
Il contient des paires clé-valeur avec différents taux de throttling appliqués aux différentes `THROTTLING_CLASSES`. Par défaut : `{ 'user': '1000/day', 'anon': '100/day', }`

`ORDERING_CLASS`
----------------

  
Il définit la classe de tri par défaut utilisée par la fonction décoratrice `ordering` lorsqu'aucune classe de tri n'est définie. Par défaut : `ninja_extra.ordering.Ordering`

`SEARCHING_CLASS`
-----------------

  
Il définit la classe de recherche par défaut utilisée par la fonction décoratrice `searching` lorsqu'aucune classe de recherche n'est définie. Par défaut : `ninja_extra.searching.Searching`

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
