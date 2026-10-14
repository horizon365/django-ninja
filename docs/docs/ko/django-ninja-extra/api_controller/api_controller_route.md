**API 컨트롤러 라우트 데코레이터**
===================

  
`route` 클래스는 특정 HTTP 메서드를 가진 엔드포인트로서 컨트롤러 클래스 함수를 어노테이션하는 데 사용되는 함수 데코레이터입니다.

예를 들어:

    from ninja_extra import route, api_controller
    
    @api_controller
    class MyController:
        @route.get('/test')
        def test(self):
            return {'message': 'test'}
    

  
`route`는 다양한 작업의 생성을 단순화하는 사전 정의된 메서드를 제공하며, 그 이름은 해당 HTTP 메서드와 일치합니다:

*   GET: `route.get`
*   POST: `route.post`
*   PUT: `route.put`
*   DELETE: `route.delete`
*   PATCH: `route.patch`
*     
    Generic - 작업 조합에 사용됩니다, 예: `route.generic(methods=['POST', 'PATCH'])`

**  
초기화 파라미터**
------------

  
다음은 NinjaExtra의 `route` 클래스 파라미터에 대한 개요 설명입니다:

*     
    `path`: 필수 고유 엔드포인트 경로 문자열.
    
*     
    `methods`: 엔드포인트에 필요한 HTTP 메서드 컬렉션, 예: `['POST', 'PUT']`.
    
*     
    `auth`: 엔드포인트의 인증 방법을 정의합니다. 기본값: `NOT_SET`
    
*     
    `response`: 응답 형식을 `dict[status_code, schema]` 또는 `Schema`로 정의합니다. 반환된 응답을 검증하는 데 사용됩니다. 기본값: `NOT_SET`
    
*     
    `operation_id`: 경로 뷰에서 작업을 구별하는 데 사용되는 선택적 고유 식별자. 기본값: `NOT_SET`
    
*     
    `summary`: 엔드포인트를 설명하는 데 사용되는 선택적 요약. 기본값: `None`
    
*     
    `description`: 엔드포인트에 대한 추가 세부 정보를 제공하는 선택적 설명. 기본값: `None`
    
*     
    `tags`: 문서화 목적으로 엔드포인트를 그룹화하는 데 사용되는 문자열 목록. 기본값: `None`
    
*     
    `deprecated`: 엔드포인트가 더 이상 사용되지 않는지 여부를 나타내는 선택적 불리언 파라미터. 기본값: `None`
    
*     
    `by_alias`: `response` 스키마 객체를 필터링하는 데 사용되는 선택적 파라미터. 기본값: `False`
    
*     
    `exclude_unset`: `response` 스키마 객체를 필터링하는 데 사용되는 선택적 파라미터. 기본값: `False`
    
*     
    `exclude_defaults`: `response` 스키마 객체를 필터링하는 데 사용되는 선택적 파라미터. 기본값: `False`
    
*     
    `exclude_none`: `response` 스키마 객체를 필터링하는 데 사용되는 선택적 파라미터. 기본값: `False`
    
*     
    `include_in_schema`: 엔드포인트가 Swagger 문서에 표시되어야 하는지 여부를 나타냅니다. 기본값: `True`
    
*     
    `url_name`: Django의 `reverse` 함수를 사용하여 해석할 수 있는 엔드포인트의 이름을 제공합니다. 기본값: `None`
    
*     
    `permissions`: 엔드포인트의 라우트 권한 클래스 컬렉션을 정의합니다. 기본값: `None`
    

  
이러한 파라미터는 Django-Ninja에서 엔드포인트를 생성할 때 사용되는 파라미터와 유사하게 기능하지만, NinjaExtra의 컨트롤러 클래스와 함께 작동하도록 추상화되었습니다.

**비동기 라우트 정의**
-----------

  
Django-Ninja-Extra에서 `route` 클래스는 Django-Ninja와 유사하게 비동기 엔드포인트 정의를 지원합니다. 이 기능은 Django 버전 3.0 이상에서 사용할 수 있습니다.

예를 들어:

    import asyncio
    from ninja_extra import http_get, api_controller
    
    @api_controller
    class MyController:
        @http_get("/say-after")
        async def say_after(self, delay: int, word: str):
            await asyncio.sleep(delay)
            return {'saying': word}
    

  
이 그림에서 `say_after` 엔드포인트는 `async` 키워드를 사용하여 비동기 함수로 정의되어 엔드포인트 내에서 비동기 작업을 허용합니다.

  
!!! info Django-Ninja 비동기 지원에 대해 자세히 알아보기

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
