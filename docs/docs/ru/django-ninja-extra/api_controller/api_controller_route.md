**Декораторы маршрутов API Controller**
===================

  
Класс `route` — это декоратор функций, используемый для аннотирования функций класса Controller как эндпоинтов с конкретным HTTP-методом.

Например:

    from ninja_extra import route, api_controller
    
    @api_controller
    class MyController:
        @route.get('/test')
        def test(self):
            return {'message': 'test'}
    

  
`route` предоставляет предопределённые методы, упрощающие создание различных операций, и их названия соответствуют соответствующим HTTP-методам:

*   GET: `route.get`
*   POST: `route.post`
*   PUT: `route.put`
*   DELETE: `route.delete`
*   PATCH: `route.patch`
*     
    Generic — используется для комбинаций операций, например `route.generic(methods=['POST', 'PATCH'])`

**  
Параметры инициализации**
------------

  
Ниже приведён обзор параметров класса `route` в NinjaExtra:

*     
    `path`: обязательная уникальная строка пути эндпоинта.
    
*     
    `methods`: набор HTTP-методов, требуемых для эндпоинта, например `['POST', 'PUT']`.
    
*     
    `auth`: определяет метод аутентификации для эндпоинта. По умолчанию: `NOT_SET`
    
*     
    `response`: определяет формат ответа как `dict[status_code, schema]` или `Schema`. Используется для валидации возвращаемого ответа. По умолчанию: `NOT_SET`
    
*     
    `operation_id`: необязательный уникальный идентификатор, используемый для различения операций в представлениях путей. По умолчанию: `NOT_SET`
    
*     
    `summary`: необязательная краткая сводка, используемая для описания эндпоинта. По умолчанию: `None`
    
*     
    `description`: необязательное описание, предоставляющее дополнительные сведения об эндпоинте. По умолчанию: `None`
    
*     
    `tags`: список строк, используемый для группировки эндпоинтов в целях документирования. По умолчанию: `None`
    
*     
    `deprecated`: необязательный логический параметр, указывающий, устарел ли эндпоинт. По умолчанию: `None`
    
*     
    `by_alias`: необязательный параметр, используемый для фильтрации объекта схемы `response`. По умолчанию: `False`
    
*     
    `exclude_unset`: необязательный параметр, используемый для фильтрации объекта схемы `response`. По умолчанию: `False`
    
*     
    `exclude_defaults`: необязательный параметр, используемый для фильтрации объекта схемы `response`. По умолчанию: `False`
    
*     
    `exclude_none`: необязательный параметр, используемый для фильтрации объекта схемы `response`. По умолчанию: `False`
    
*     
    `include_in_schema`: указывает, должен ли эндпоинт отображаться в документации Swagger. По умолчанию: `True`
    
*     
    `url_name`: задаёт имя для эндпоинта, которое можно разрешить с помощью функции `reverse` в Django. По умолчанию: `None`
    
*     
    `permissions`: определяет набор классов разрешений маршрута для эндпоинта. По умолчанию: `None`
    

  
Эти параметры работают аналогично тем, что используются при создании эндпоинтов в Django-Ninja, но были абстрагированы для работы с классами контроллеров в NinjaExtra.

**Определение асинхронных маршрутов**
-----------

  
В Django-Ninja-Extra класс `route` поддерживает определение асинхронных эндпоинтов, аналогично Django-Ninja. Эта возможность доступна для версий Django старше 3.0.

Например:

    import asyncio
    from ninja_extra import http_get, api_controller
    
    @api_controller
    class MyController:
        @http_get("/say-after")
        async def say_after(self, delay: int, word: str):
            await asyncio.sleep(delay)
            return {'saying': word}
    

  
В этом примере эндпоинт `say_after` определён как асинхронная функция с использованием ключевого слова `async`, что позволяет выполнять асинхронные операции внутри эндпоинта.

  
!!! info Read more about Django-Ninja async support

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
