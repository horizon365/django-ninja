---
comments: true
---
# 필터링

사용자가 여러 다양한 속성으로 queryset을 필터링할 수 있게 하려면, 필터를 `FilterSchema` 클래스로 캡슐화하는 것이 좋습니다.
`FilterSchema`는 일반 `Schema`이므로 Pydantic의 필요한 모든 기능을 사용하지만, 사용자 대상 필터링 파라미터를 데이터베이스 쿼리로 쉽게 변환할 수 있는 몇 가지 편의 기능도 추가합니다.

먼저 `FilterSchema`의 서브클래스를 정의합니다:

```python hl_lines="6 7 8"
from ninja import FilterSchema, Field
from typing import Optional


class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    author: Optional[str] = None
    created_after: Optional[datetime] = None
```


다음으로, API 핸들러에서 이 스키마를 `Query`와 함께 사용합니다:
```python hl_lines="2"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

[Schema를 사용한 Query 파라미터 정의](./query-params.md#using-schema)에서 설명한 것처럼, Django Ninja는 `BookFilterSchema`에 정의된 필드를 query 파라미터로 변환합니다.
한 줄짜리 축약 메서드 `.filter()`를 사용하여 이 필터들을 queryset에 적용할 수 있습니다:
```python hl_lines="4"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

내부적으로 `FilterSchema`는 자신의 필드를 [Q 표현식](https://docs.djangoproject.com/en/3.1/topics/db/queries/#complex-lookups-with-q-objects)으로 변환한 후, 이를 결합하여 queryset을 필터링하는 데 사용합니다.


`.filter` 메서드를 사용하는 대신, 준비된 `Q` 표현식을 받아 직접 필터링을 수행할 수도 있습니다.
API를 통해 사용자에게 노출하는 필터링 위에 추가적인 queryset 필터링이 필요한 경우에 유용합니다:
```python hl_lines="5 8"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):

    # Never serve books from inactive publishers and authors
    q = Q(author__is_active=True) | Q(publisher__is_active=True)
    
    # But allow filtering the rest of the books
    q &= filters.get_filter_expression()
    return Book.objects.filter(q)
```

기본적으로 필터는 다음과 같이 동작합니다:

* `None` 값은 무시되며 필터링이 적용되지 않습니다;
* `None`이 아닌 각 필드는 각 필드의 `Field` 정의에 따라 `Q` 표현식으로 변환됩니다;
* 모든 `Q` 표현식은 `AND` 논리 연산자로 하나로 결합됩니다;
* 최종 `Q` 표현식이 queryset 필터링에 사용되며, `.filter` 절이 적용된 queryset이 반환됩니다.

## 커스텀 필드
기본적으로 `FilterSet`은 필드 이름을 사용해 Q 표현식을 생성합니다:
```python
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
```
`name` 필드는 `Q(name=...)` 표현식으로 변환됩니다.

데이터베이스 lookup이 이보다 더 복잡한 경우, 필드 정의에서 `"q"` 키워드 인자로 명시적으로 지정할 수 있습니다:
```python hl_lines="2"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains') 
```
여러 lookup 키워드 인자 이름을 리스트로 지정할 수도 있습니다:
```python hl_lines="2 3 4"
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains',
                                     'author__name__icontains',
                                     'publisher__name__icontains']) 
```
기본적으로 필드 레벨 표현식은 `"OR"` 커넥터로 결합되므로, 위 설정에서 query 파라미터 `?search=foobar`는 이름, 저자, 출판사 중 하나라도 "foobar"를 포함하는 책을 검색합니다.


## 표현식 결합
기본적으로,

* 필드 레벨 표현식은 `OR` 연산자로 결합됩니다.
* 필드 자체들은 `AND` 연산자로 결합됩니다.

따라서 다음 `FilterSchema`에 대해...
```python
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains', 'author__name__icontains'])
    popular: Optional[bool] = None
```
...사용자가 다음 query 파라미터를 보내면
```
http://localhost:8000/api/books?search=harry&popular=true
```
`FilterSchema` 인스턴스는 책의 이름 _또는_ 저자의 이름에 `harry`가 포함되고, 인기 있는 책을 찾습니다.


필드 레벨과 클래스 레벨 정의 모두에서 `expression_connector` 파라미터를 사용해 이 동작을 커스터마이즈할 수 있습니다:
```python hl_lines="3 7"
class BookFilterSchema(FilterSchema):
    active: Optional[bool] = Field(None, q=['is_active', 'publisher__is_active'],
                                   expression_connector='AND')
    name: Optional[str] = Field(None, q='name__icontains')
    
    class Config:
        expression_connector = 'OR'
```

expression 커넥터는 `"OR"`, `"AND"`, `"XOR"` 값을 가질 수 있지만, 마지막 것은 Django 4.1에서만 [지원됩니다](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#xor).

이제 다음 query 파라미터가 포함된 요청은
```
http://localhost:8000/api/books?name=harry&active=true
```
...이름에 `harry`가 있거나 _또는_ 스스로 활성 상태이며 활성 출판사에서 출판된 책을 찾습니다.


## None으로 필터링
`FilterSchema`가 `None`을 필터링이 수행되어야 하는 유효한 값으로 취급하게 만들 수 있습니다.

필드 레벨에서는 `ignore_none` 키워드 인자를 통해 수행할 수 있습니다:
```python hl_lines="3"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
```

이렇게 하면 사용자가 `"tag"`에 다른 값을 제공하지 않을 때 필터가 항상 `tag=None` 조건을 포함합니다.

설정에서 모든 필드에 대해 한 번에 지정할 수도 있습니다:
```python hl_lines="6"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
    
    class Config:
        ignore_none = False
```


## 커스텀 표현식
때로는 단일 필드 어노테이션으로 처리할 수 없는 복잡한 필터링 시나리오가 있을 수 있습니다.
이런 경우 필드 필터링 로직을 커스텀 메서드로 구현할 수 있습니다. 필터링 값을 받아 Q 표현식을 반환하는 `filter_<fieldname>` 이름의 메서드를 정의하기만 하면 됩니다:

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    tag: Optional[str] = None
    popular: Optional[bool] = None
    
    def filter_popular(self, value: bool) -> Q:
        return Q(view_count__gt=1000) | Q(download_count__gt=100) if value else Q()
```
이런 필드 메서드는 해당 필드의 `Field()` 정의에 지정된 내용보다 우선합니다.
그것만으로 충분하지 않다면, `custom_expression` 메서드에서 전체 `FilterSet` 클래스에 대한 커스텀 필터링 로직을 구현할 수 있습니다:

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    popular: Optional[bool] = None

    def custom_expression(self) -> Q:
        q = Q()
        if self.name:
            q &= Q(name__icontains=self.name)
        if self.popular:
            q &= (
                Q(view_count__gt=1000) |
                Q(downloads__gt=100) |
                Q(tag='popular')
            )
        return q
```
`custom_expression` 메서드는 `filter_<fieldname>` 메서드를 포함해 위에서 설명한 다른 모든 정의보다 우선합니다.

!!! done

    입력 파라미터 시리즈가 완료되었습니다! 다음 섹션 **[응답 처리](../response/index.md)**로 계속 진행하세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
