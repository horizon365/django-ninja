**Pengaturan**
=======

  
Django-Ninja-Extra memiliki beberapa pengaturan yang dapat di-override dengan menambahkan field `NINJA_EXTRA` di `settings.py` Django dan menambahkan beberapa pasangan key-value, seperti yang ditunjukkan di bawah ini:

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
    

  
Anda hanya perlu meng-override yang Anda butuhkan. Tidak perlu meng-override semuanya.

`PAGINATION_CLASS`
------------------

  
Pengaturan ini mendefinisikan kelas paginator default yang digunakan oleh fungsi dekorator `paginate` ketika tidak ada kelas paginator yang didefinisikan. Default: `ninja_extra.pagination.LimitOffsetPagination`

`PAGINATION_PER_PAGE`
---------------------

  
Pengaturan ini mendefinisikan ukuran halaman (page size) default yang diteruskan ke `PAGINATION_CLASS` saat dibuat (instansiasi). Nilai default: `100`

`INJECTOR_MODULES`
------------------

  
Pengaturan ini berisi daftar string yang mendefinisikan path menuju `Module` injector. Nilai default: `[]`

`THROTTLE_CLASSES`
------------------

  
Pengaturan ini berisi daftar string yang mendefinisikan path menuju kelas throttle default. Default: `[ "ninja_extra.throttling.AnonRateThrottle", "ninja_extra.throttling.UserRateThrottle", ]`

`THROTTLE_RATES`
----------------

  
Pengaturan ini berisi pasangan key-value dengan tingkat throttle yang berbeda yang diterapkan pada `THROTTLING_CLASSES` yang berbeda. Default: `{ 'user': '1000/day', 'anon': '100/day', }`

`ORDERING_CLASS`
----------------

  
Pengaturan ini mendefinisikan kelas ordering default yang digunakan oleh fungsi dekorator `ordering` ketika tidak ada kelas ordering yang didefinisikan. Default: `ninja_extra.ordering.Ordering`

`SEARCHING_CLASS`
-----------------

  
Pengaturan ini mendefinisikan kelas searching default yang digunakan oleh fungsi dekorator `searching` ketika tidak ada kelas searching yang didefinisikan. Default: `ninja_extra.searching.Searching`

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
