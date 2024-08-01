**设置**
=======

  
Django-Ninja-Extra 有一些设置可以通过在 Django `settings.py` 中添加一个 `NINJA_EXTRA` 字段并添加一些键值对来覆盖，如下所示：

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
    

  
你可以覆盖你不需要的东西。没有必要覆盖所有东西。

`PAGINATION_CLASS`
------------------

  
它定义了 `paginate` 装饰器函数使用的默认分页器类，如果没有定义分页器类的话。默认： `ninja_extra.pagination.LimitOffsetPagination`

`PAGINATION_PER_PAGE`
---------------------

  
它定义了在实例化时传递给 `PAGINATION_CLASS` 的默认页面大小。默认值： `100`

`INJECTOR_MODULES`
------------------

  
它包含一个字符串列表，该列表定义了注入器 `Module` 的路径。默认值： `[]`

`THROTTLE_CLASSES`
------------------

  
它包含一个字符串列表，用于定义路径默认节流类。默认： `[ "ninja_extra.throttling.AnonRateThrottle", "ninja_extra.throttling.UserRateThrottle", ]`

`THROTTLE_RATES`
----------------

  
它包含一个键值对，其中包含应用于不同 `THROTTLING_CLASSES` 的不同节流率。默认： `{ 'user': '1000/day', 'anon': '100/day', }`

`ORDERING_CLASS`
----------------

  
它定义了 `ordering` 装饰器函数使用的默认排序类，如果没有定义排序类的话。默认： `ninja_extra.ordering.Ordering`

`SEARCHING_CLASS`
-----------------

  
它定义了 `searching` 装饰器函数使用的默认搜索类，如果没有定义搜索类的话。默认： `ninja_extra.searching.Searching`

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
