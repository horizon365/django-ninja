---
comments: true
---
# 페이지네이션

**Django Ninja**는 페이지네이션 지원을 기본 제공합니다. 이를 통해 큰 결과 집합을 별도의 페이지로 나눌 수 있습니다.


함수에 페이지네이션을 적용하려면 - `paginate` 데코레이터를 적용하기만 하면 됩니다:

```python hl_lines="1 4"
from ninja.pagination import paginate

@api.get('/users', response=List[UserSchema])
@paginate
def list_users(request):
    return User.objects.all()
```


이것으로 끝입니다!

이제 `limit`과 `offset` GET 파라미터를 사용해 users를 조회할 수 있습니다

```
/api/users?limit=10&offset=0
```

기본적으로 limit은 `100`으로 설정됩니다(settings.py에서 `NINJA_PAGINATION_PER_PAGE`를 사용해 변경할 수 있습니다)


## 내장 페이지네이션 클래스

### LimitOffsetPagination (기본값)

이것이 기본 페이지네이션 클래스입니다(settings.py에서 `NINJA_PAGINATION_CLASS`를 클래스의 경로로 지정하여 변경할 수 있습니다)

```python hl_lines="1 4"
from ninja.pagination import paginate, LimitOffsetPagination

@api.get('/users', response=List[UserSchema])
@paginate(LimitOffsetPagination)
def list_users(request):
    return User.objects.all()
```

쿼리 예제:
```
/api/users?limit=10&offset=0
```

이 클래스에는 두 개의 입력 파라미터가 있습니다:

 - `limit` - 한 페이지의 queryset 수를 정의합니다 (기본값 = 100, NINJA_PAGINATION_PER_PAGE로 변경 가능)
 - `offset` - 페이지 윈도우의 오프셋을 설정합니다 (기본값: 0, 인덱싱은 0부터 시작)


### PageNumberPagination
```python hl_lines="1 4"
from ninja.pagination import paginate, PageNumberPagination

@api.get('/users', response=List[UserSchema])
@paginate(PageNumberPagination)
def list_users(request):
    return User.objects.all()
```

쿼리 예제:
```
/api/users?page=2
```

이 클래스는 `page`라는 하나의 파라미터를 가지며, 기본적으로 페이지당 100개의 queryset을 출력합니다(settings.py로 변경 가능)

페이지 번호는 1부터 시작합니다.

각 뷰에 개별적으로 커스텀 페이지 크기 값을 설정할 수도 있습니다:

```python hl_lines="2"
@api.get("/users")
@paginate(PageNumberPagination, page_size=50)
def list_users(...
```



## 뷰 함수에서 페이지네이션 파라미터 접근

뷰 함수에서 페이지네이션에 사용된 `Input` 파라미터에 접근해야 하는 경우 - `pass_parameter` 인자를 사용하세요

이 경우 입력 데이터는 `**kwargs`에서 사용할 수 있습니다:

```python hl_lines="2 4"
@api.get("/someview")
@paginate(pass_parameter="pagination_info")
def someview(request, **kwargs):
    page = kwargs["pagination_info"].page
    return ...
```


## 커스텀 페이지네이션 클래스 만들기

커스텀 페이지네이션 클래스를 만들려면 `ninja.pagination.PaginationBase`를 상속하고 `Input`과 `Output` 스키마 클래스, 그리고 `paginate_queryset(self, queryset, request, **params)` 메서드를 오버라이드해야 합니다:

 - `Input` 스키마는 페이지네이터에 전달되어야 하는 파라미터(예: 페이지 번호 또는 limit/offset 값)를 기술하는 스키마 클래스입니다.
 - `Output` 스키마는 페이지 출력의 스키마(예: count/next/items 등)를 기술합니다.
 - `paginate_queryset` 메서드는 초기 queryset을 받으며, 요청된 페이지의 데이터만 포함하는 iterable을 반환해야 합니다. 이 메서드는 다음 파라미터를 받습니다:
    - `queryset`: API 함수가 반환한 queryset(또는 iterable).
    - `pagination` - paginator.Input 파라미터 (파싱 및 검증됨)
    - `**params`: 데코레이션된 함수가 받는 모든 인자를 포함하는 키워드 인자.


예제:

```python hl_lines="7 11 16 26"
from ninja.pagination import paginate, PaginationBase
from ninja import Schema


class CustomPagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        skip: int
        

    class Output(Schema):
        items: List[Any] # `items` is a default attribute
        total: int
        per_page: int

    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        return {
            'items': queryset[skip : skip + 5],
            'total': queryset.count(),
            'per_page': 5,
        }


@api.get('/users', response=List[UserSchema])
@paginate(CustomPagination)
def list_users(request):
    return User.objects.all()
```

팁: 파라미터에서 request 객체를 얻을 수 있습니다:

```python
def paginate_queryset(self, queryset, pagination: Input, **params):
    request = params["request"]
```

#### 비동기 페이지네이션

표준 **Django Ninja** 페이지네이션 클래스는 async를 지원합니다. 커스텀 페이지네이션 클래스로 비동기 요청을 처리하려면 `ninja.pagination.AsyncPaginationBase`를 상속하고 `apaginate_queryset(self, queryset, request, **params)` 메서드를 오버라이드해야 합니다.

### Output 속성

기본적으로 페이지 아이템은 `'items'` 속성에 배치됩니다. 이 동작을 오버라이드하려면 `items_attribute`를 사용할 수 있습니다:

```python hl_lines="4 8"
class CustomPagination(PaginationBase):
    ...
    class Output(Schema):
        results: List[Any]
        total: int
        per_page: int
    
    items_attribute: str = "results"

```


## 여러 operation에 한 번에 페이지네이션 적용

queryset이나 리스트를 반환하는 모든 뷰에 페이지네이션을 추가해야 하는 경우가 종종 있습니다

내장 라우터 클래스(`RouterPaginated`)를 사용할 수 있습니다. 이는 `response=List[SomeSchema]`로 정의된 모든 operation에 자동으로 페이지네이션을 주입합니다:

```python hl_lines="1 3 6 10"
from ninja.pagination import RouterPaginated

router = RouterPaginated()


@router.get("/items", response=List[MySchema])
def items(request):
    return MyModel.objects.all()

@router.get("/other-items", response=List[OtherSchema])
def ohter_items(request):
    return OtherModel.objects.all()

```

이 예제에서 두 operation 모두 페이지네이션이 활성화됩니다.

메인 `api` 인스턴스에 페이지네이션을 적용하려면 `default_router` 인자를 사용할 수 있습니다:


```python
api = NinjaAPI(default_router=RouterPaginated())

@api.get(...
```

!!! done

    다음 챕터로 계속 진행하세요! **[Response Renderer](response-renderers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
