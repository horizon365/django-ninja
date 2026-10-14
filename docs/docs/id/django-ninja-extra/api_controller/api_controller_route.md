**Decorator Route API Controller**
===================

  
Class `route` adalah function decorator yang digunakan untuk menganotasi fungsi-fungsi class Controller sebagai endpoint dengan HTTP method tertentu.

Misalnya:

    from ninja_extra import route, api_controller
    
    @api_controller
    class MyController:
        @route.get('/test')
        def test(self):
            return {'message': 'test'}
    

  
`route` menyediakan metode-metode yang telah didefinisikan sebelumnya (predefined) yang menyederhanakan pembuatan berbagai operasi, dan namanya selaras dengan HTTP method yang sesuai:

*   GET: `route.get`
*   POST: `route.post`
*   PUT: `route.put`
*   DELETE: `route.delete`
*   PATCH: `route.patch`
*     
    Generic - digunakan untuk kombinasi operasi, misalnya, `route.generic(methods=['POST', 'PATCH'])`

**  
Parameter Inisialisasi**
------------

  
Berikut adalah deskripsi ringkas dari parameter-parameter class `route` di NinjaExtra:

*     
    `path`: String path endpoint unik yang wajib diisi.
    
*     
    `methods`: Kumpulan HTTP method yang dibutuhkan untuk endpoint tersebut, misalnya, `['POST', 'PUT']`.
    
*     
    `auth`: Mendefinisikan metode autentikasi untuk endpoint. Default: `NOT_SET`
    
*     
    `response`: Mendefinisikan format respons sebagai `dict[status_code, schema]` atau `Schema`. Digunakan untuk memvalidasi respons yang dikembalikan. Default: `NOT_SET`
    
*     
    `operation_id`: Identifier unik opsional yang digunakan untuk membedakan operasi di path views. Default: `NOT_SET`
    
*     
    `summary`: Ringkasan opsional yang digunakan untuk mendeskripsikan endpoint. Default: `None`
    
*     
    `description`: Deskripsi opsional yang memberikan detail tambahan tentang endpoint. Default: `None`
    
*     
    `tags`: List berisi string yang digunakan untuk mengelompokkan endpoint untuk keperluan dokumentasi. Default: `None`
    
*     
    `deprecated`: Parameter boolean opsional yang menunjukkan apakah endpoint tersebut deprecated. Default: `None`
    
*     
    `by_alias`: Parameter opsional yang digunakan untuk memfilter objek schema `response`. Default: `False`
    
*     
    `exclude_unset`: Parameter opsional yang digunakan untuk memfilter objek schema `response`. Default: `False`
    
*     
    `exclude_defaults`: Parameter opsional yang digunakan untuk memfilter objek schema `response`. Default: `False`
    
*     
    `exclude_none`: Parameter opsional yang digunakan untuk memfilter objek schema `response`. Default: `False`
    
*     
    `include_in_schema`: Menunjukkan apakah endpoint tersebut sebaiknya muncul di dokumentasi Swagger. Default: `True`
    
*     
    `url_name`: Memberikan nama bagi endpoint yang dapat di-resolve menggunakan fungsi `reverse` di Django. Default: `None`
    
*     
    `permissions`: Mendefinisikan kumpulan class permission route untuk endpoint. Default: `None`
    

  
Parameter-parameter ini berfungsi serupa dengan parameter yang digunakan saat membuat endpoint di Django-Ninja, tetapi telah diabstraksi agar dapat bekerja dengan class controller di NinjaExtra.

**Definisi Route Async**
-----------

  
Di Django-Ninja-Extra, class `route` mendukung pendefinisian endpoint async, serupa dengan Django-Ninja. Fitur ini tersedia untuk versi Django yang lebih besar dari 3.0.

Sebagai contoh:

    import asyncio
    from ninja_extra import http_get, api_controller
    
    @api_controller
    class MyController:
        @http_get("/say-after")
        async def say_after(self, delay: int, word: str):
            await asyncio.sleep(delay)
            return {'saying': word}
    

  
Dalam ilustrasi ini, endpoint `say_after` didefinisikan sebagai fungsi asinkron menggunakan keyword `async`, memungkinkan operasi asinkron di dalam endpoint tersebut.

  
!!! info Baca lebih lanjut tentang dukungan async Django-Ninja

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
