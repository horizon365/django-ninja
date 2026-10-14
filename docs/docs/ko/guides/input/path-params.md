---
comments: true
---
# Path 파라미터

Python 포맷 문자열과 동일한 문법(다행히 <a href="https://swagger.io/docs/specification/describing-parameters/#path-parameters" target="_blank">OpenAPI path 파라미터</a>와도 일치합니다)을 사용하여 path "파라미터"를 선언할 수 있습니다:

```python hl_lines="1 2"
{!./src/tutorial/path/code01.py!}
```

Path 파라미터 `item_id`의 값은 `item_id` 인자로 여러분의 함수에 전달됩니다.

따라서 이 예제를 실행하고 <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a> 로 이동하면 다음 응답을 볼 수 있습니다:

```JSON
{"item_id":"foo"}
```


### 타입이 있는 Path 파라미터

함수에서 표준 Python 타입 어노테이션을 사용하여 path 파라미터의 타입을 선언할 수 있습니다:

```python hl_lines="2"
{!./src/tutorial/path/code02.py!}
```

이 경우 `item_id`는 **`int`**로 선언됩니다. 이를 통해 에러 검사, 코드 자동 완성 등을 위한 에디터 및 린터 지원을 받을 수 있습니다.

브라우저에서 <a href="http://localhost:8000/api/items/3" target="_blank">http://localhost:8000/api/items/3</a> 을 사용해 이 코드를 실행하면 다음 응답을 볼 수 있습니다:
```JSON
{"item_id":3}
```

!!! tip
    함수가 받는(그리고 반환하는) 값은 Python `int`로서의 **3**이지, 문자열 `"3"`이 아니라는 점에 유의하세요.
    즉, 이 타입 선언만으로 **Django Ninja**가 자동으로 request "파싱"과 검증을 제공합니다.



### 데이터 검증

반면, 브라우저에서 <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a> <small>*(`"foo"`는 int가 아님)*</small> 를 방문하면 다음과 같은 HTTP 에러가 표시됩니다:

```JSON hl_lines="8"
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```


### Django Path 컨버터

[Django path 컨버터](https://docs.djangoproject.com/en/stable/topics/http/urls/#path-converters)를
사용하여 path 파싱을 도울 수 있습니다:

```python hl_lines="1"
@api.get("/items/{int:item_id}")
def read_item(request, item_id):
    return {"item_id": item_id}
```

이 경우 `item_id`는 **`int`**로 파싱됩니다. `item_id`가 유효한 `int`가 아니면 URL이 매칭되지 않습니다.
(예를 들어 다른 라우트가 매칭되지 않으면 404 Not Found가 반환됩니다.)

!!! tip
    **Django Ninja**는 어노테이션이 없는 파라미터에 기본 `str` 타입을 사용하므로, 위 함수가 받는(그리고 반환하는) 값은 Python `str`로서의 `"3"`이지,
    정수 **3**이 아니라는 점에 유의하세요. `int`를 받으려면 평소처럼 함수 정의에서 `item_id`를 `int` 타입 어노테이션으로 선언하기만 하면 됩니다:

    ```python hl_lines="2"
    @api.get("/items/{int:item_id}")
    def read_item(request, item_id:int):
        return {"item_id": item_id}
    ```
 
#### 슬래시가 포함된 Path 파라미터

Django의 `path` 컨버터를 사용하면 path 형태의 파라미터를 처리할 수 있습니다:

```python hl_lines="1"
@api.get('/dir/{path:value}')
def someview(request, value: str):
    return value
```
이 operation을 `/dir/some/path/with-slashes`로 조회할 수 있으며, `value`는 `some/path/with-slashes`가 됩니다

### 다중 파라미터

원하는 만큼 많은 변수를 `path`에 전달할 수 있습니다 - 고유한 이름을 사용하는 것, 그리고 함수 인자에 동일한 이름을 사용하는 것을 잊지 마세요.

```python
@api.get("/events/{year}/{month}/{day}")
def events(request, year: int, month: int, day: int):
    return {"date": [year, month, day]}
```


### Schema 사용

스키마를 사용하여 상호 의존적인 path 파라미터를 캡슐화할 수도 있습니다(그리고 그룹으로 검증할 수 있습니다):


```python hl_lines="1 2  5 6 7 8 9 10 11 15"
{!./src/tutorial/path/code010.py!}
```

!!! note
    여기서는 `Path` 소스 힌트를 사용하여 **Django Ninja**가 이 스키마가 path 파라미터에 적용될 것임을 알 수 있게 합니다.

### 문서화

이제 브라우저에서 <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a> 를 열면 자동 생성된 인터랙티브 API 문서가 표시됩니다.
![Django Ninja Swagger](../../img/tutorial-path-swagger.png)

!!! done

    다음 챕터로 계속 진행하세요! **[Query 파라미터](query-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
