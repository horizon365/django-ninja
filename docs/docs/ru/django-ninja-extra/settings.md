**Настройки**
=======

  
Django-Ninja-Extra имеет ряд настроек, которые можно переопределить, добавив поле `NINJA_EXTRA` в `settings.py` Django и указав несколько пар «ключ-значение», как показано ниже:

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
    

  
Вы можете переопределить только то, что вам нужно. Переопределять всё необязательно.

`PAGINATION_CLASS`
------------------

  
Определяет класс пагинатора по умолчанию, используемый функцией-декоратором `paginate`, когда класс пагинатора не задан. По умолчанию: `ninja_extra.pagination.LimitOffsetPagination`

`PAGINATION_PER_PAGE`
---------------------

  
Определяет размер страницы по умолчанию, передаваемый в `PAGINATION_CLASS` при его создании. Значение по умолчанию: `100`

`INJECTOR_MODULES`
------------------

  
Содержит список строк, определяющих пути к `Module` injector. Значение по умолчанию: `[]`

`THROTTLE_CLASSES`
------------------

  
Содержит список строк, определяющих пути к классам троттлинга по умолчанию. По умолчанию: `[ "ninja_extra.throttling.AnonRateThrottle", "ninja_extra.throttling.UserRateThrottle", ]`

`THROTTLE_RATES`
----------------

  
Содержит пары «ключ-значение» с различными лимитами троттлинга, применяемыми к разным `THROTTLING_CLASSES`. По умолчанию: `{ 'user': '1000/day', 'anon': '100/day', }`

`ORDERING_CLASS`
----------------

  
Определяет класс сортировки по умолчанию, используемый функцией-декоратором `ordering`, когда класс сортировки не задан. По умолчанию: `ninja_extra.ordering.Ordering`

`SEARCHING_CLASS`
-----------------

  
Определяет класс поиска по умолчанию, используемый функцией-декоратором `searching`, когда класс поиска не задан. По умолчанию: `ninja_extra.searching.Searching`

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
