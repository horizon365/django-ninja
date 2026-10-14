**Settings**
=======

  
Django-Ninja-Extra में कुछ settings हैं जिन्हें Django `settings.py` में एक `NINJA_EXTRA` field जोड़कर और कुछ key-value pairs जोड़कर override किया जा सकता है, जैसा कि नीचे दिखाया गया है:

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
    

  
आप केवल वही override कर सकते हैं जिसकी आपको आवश्यकता है। सब कुछ override करने की कोई आवश्यकता नहीं है।

`PAGINATION_CLASS`
------------------

  
यह डिफ़ॉल्ट paginator class define करता है जिसका उपयोग `paginate` decorator function तब करता है जब कोई paginator class define नहीं की गई हो। डिफ़ॉल्ट: `ninja_extra.pagination.LimitOffsetPagination`

`PAGINATION_PER_PAGE`
---------------------

  
यह डिफ़ॉल्ट page size define करता है जो `PAGINATION_CLASS` को instantiate करते समय पास किया जाता है। डिफ़ॉल्ट मान: `100`

`INJECTOR_MODULES`
------------------

  
इसमें strings की एक list होती है जो injector `Module` के paths define करती है। डिफ़ॉल्ट मान: `[]`

`THROTTLE_CLASSES`
------------------

  
इसमें strings की एक list होती है जो डिफ़ॉल्ट throttle classes के paths define करती है। डिफ़ॉल्ट: `[ "ninja_extra.throttling.AnonRateThrottle", "ninja_extra.throttling.UserRateThrottle", ]`

`THROTTLE_RATES`
----------------

  
इसमें key-value pairs होते हैं जिनमें विभिन्न `THROTTLING_CLASSES` पर लागू विभिन्न throttle rates होते हैं। डिफ़ॉल्ट: `{ 'user': '1000/day', 'anon': '100/day', }`

`ORDERING_CLASS`
----------------

  
यह डिफ़ॉल्ट ordering class define करता है जिसका उपयोग `ordering` decorator function तब करता है जब कोई ordering class define नहीं की गई हो। डिफ़ॉल्ट: `ninja_extra.ordering.Ordering`

`SEARCHING_CLASS`
-----------------

  
यह डिफ़ॉल्ट searching class define करता है जिसका उपयोग `searching` decorator function तब करता है जब कोई searching class define नहीं की गई हो। डिफ़ॉल्ट: `ninja_extra.searching.Searching`

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
