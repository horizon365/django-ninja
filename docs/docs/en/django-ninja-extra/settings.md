**Settings**
=======

  
Django-Ninja-Extra has some settings that can be overridden by adding a `NINJA_EXTRA` field in Django `settings.py` and adding some key-value pairs, as shown below:

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
    

  
You can override only what you need. There is no need to override everything.

`PAGINATION_CLASS`
------------------

  
It defines the default paginator class used by the `paginate` decorator function when no paginator class is defined. Default: `ninja_extra.pagination.LimitOffsetPagination`

`PAGINATION_PER_PAGE`
---------------------

  
It defines the default page size passed to `PAGINATION_CLASS` when instantiated. Default value: `100`

`INJECTOR_MODULES`
------------------

  
It contains a list of strings that define the paths to the injector `Module`s. Default value: `[]`

`THROTTLE_CLASSES`
------------------

  
It contains a list of strings that define the paths to the default throttle classes. Default: `[ "ninja_extra.throttling.AnonRateThrottle", "ninja_extra.throttling.UserRateThrottle", ]`

`THROTTLE_RATES`
----------------

  
It contains key-value pairs with different throttle rates applied to different `THROTTLING_CLASSES`. Default: `{ 'user': '1000/day', 'anon': '100/day', }`

`ORDERING_CLASS`
----------------

  
It defines the default ordering class used by the `ordering` decorator function when no ordering class is defined. Default: `ninja_extra.ordering.Ordering`

`SEARCHING_CLASS`
-----------------

  
It defines the default searching class used by the `searching` decorator function when no searching class is defined. Default: `ninja_extra.searching.Searching`

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
