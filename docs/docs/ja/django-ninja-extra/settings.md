**設定**
=======

  
Django-Ninja-Extra には、Django の `settings.py` に `NINJA_EXTRA` フィールドを追加し、いくつかのキーと値のペアを記述することで上書きできる設定があります。以下の通りです：

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
    

  
必要なものだけを上書きすればよく、すべてを上書きする必要はありません。

`PAGINATION_CLASS`
------------------

  
ページネータクラスが明示的に指定されなかった場合に、`paginate` デコレータ関数が使用するデフォルトのページネータクラスを定義します。デフォルト： `ninja_extra.pagination.LimitOffsetPagination`

`PAGINATION_PER_PAGE`
---------------------

  
`PAGINATION_CLASS` のインスタンス生成時に渡されるデフォルトのページサイズを定義します。デフォルト値： `100`

`INJECTOR_MODULES`
------------------

  
インジェクタの `Module` へのパスを定義する文字列のリストです。デフォルト値： `[]`

`THROTTLE_CLASSES`
------------------

  
デフォルトのスロットリングクラスへのパスを定義する文字列のリストです。デフォルト： `[ "ninja_extra.throttling.AnonRateThrottle", "ninja_extra.throttling.UserRateThrottle", ]`

`THROTTLE_RATES`
----------------

  
異なる `THROTTLING_CLASSES` に適用される異なるスロットルレートのキーと値のペアです。デフォルト： `{ 'user': '1000/day', 'anon': '100/day', }`

`ORDERING_CLASS`
----------------

  
オーダリングクラスが明示的に指定されなかった場合に、`ordering` デコレータ関数が使用するデフォルトのオーダリングクラスを定義します。デフォルト： `ninja_extra.ordering.Ordering`

`SEARCHING_CLASS`
-----------------

  
サーチングクラスが明示的に指定されなかった場合に、`searching` デコレータ関数が使用するデフォルトのサーチングクラスを定義します。デフォルト： `ninja_extra.searching.Searching`

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
