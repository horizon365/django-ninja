**설정**
=======

  
Django-Ninja-Extra에는 Django `settings.py`에 `NINJA_EXTRA` 필드를 추가하고 아래와 같이 키-값 쌍을 넣어 재정의할 수 있는 설정들이 있습니다:

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
    

  
필요한 것만 재정의하면 됩니다. 모든 것을 재정의할 필요는 없습니다.

`PAGINATION_CLASS`
------------------

  
`paginate` 데코레이터 함수가 페이징 클래스가 정의되지 않았을 때 사용할 기본 페이저(paginator) 클래스를 정의합니다. 기본값: `ninja_extra.pagination.LimitOffsetPagination`

`PAGINATION_PER_PAGE`
---------------------

  
`PAGINATION_CLASS`가 인스턴스화될 때 전달되는 기본 페이지 크기를 정의합니다. 기본값: `100`

`INJECTOR_MODULES`
------------------

  
injector `Module`들의 경로를 정의하는 문자열 목록을 담습니다. 기본값: `[]`

`THROTTLE_CLASSES`
------------------

  
기본 스로틀(throttle) 클래스들의 경로를 정의하는 문자열 목록을 담습니다. 기본값: `[ "ninja_extra.throttling.AnonRateThrottle", "ninja_extra.throttling.UserRateThrottle", ]`

`THROTTLE_RATES`
----------------

  
서로 다른 `THROTTLING_CLASSES`에 적용되는 서로 다른 스로틀 비율의 키-값 쌍을 담습니다. 기본값: `{ 'user': '1000/day', 'anon': '100/day', }`

`ORDERING_CLASS`
----------------

  
`ordering` 데코레이터 함수가 ordering 클래스가 정의되지 않았을 때 사용할 기본 ordering 클래스를 정의합니다. 기본값: `ninja_extra.ordering.Ordering`

`SEARCHING_CLASS`
-----------------

  
`searching` 데코레이터 함수가 searching 클래스가 정의되지 않았을 때 사용할 기본 searching 클래스를 정의합니다. 기본값: `ninja_extra.searching.Searching`

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
