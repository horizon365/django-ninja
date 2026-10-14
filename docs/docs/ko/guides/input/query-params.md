---
comments: true
---
# Query 파라미터

Path 파라미터의 일부가 아닌 함수 파라미터를 선언하면, 자동으로 "query" 파라미터로 해석됩니다.
```python hl_lines="5"
{!./src/tutorial/query/code01.py!}
```

이 operation을 조회하려면 다음과 같은 URL을 사용할 수 있습니다:

```
http://localhost:8000/api/weapons?offset=0&limit=10
```
기본적으로 모든 GET 파라미터는 문자열입니다. 함수 파라미터에 타입을 어노테이션하면 해당 타입으로 변환되고 그에 맞게 검증됩니다.

Path 파라미터에 적용되는 것과 동일한 이점이 query 파라미터에도 적용됩니다:

- 에디터 지원 (당연히)
- 데이터 "파싱"
- 데이터 검증
- 자동 문서화


!!! note
    파라미터에 타입을 어노테이션하지 않으면 `str` 타입으로 취급됩니다

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit, offset):
    # type(limit) == str
    # type(offset) == str
```

### 기본값

Query 파라미터는 path의 고정된 부분이 아니므로 선택적이며 기본값을 가질 수 있습니다:

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit: int = 10, offset: int = 0):
    return weapons[offset : offset + limit]
```

위 예제에서는 `offset=0`과 `limit=10`이라는 기본값을 설정했습니다.

따라서 다음 URL을 방문하면:
```
http://localhost:8000/api/weapons
```
다음을 방문한 것과 동일합니다:
```
http://localhost:8000/api/weapons?offset=0&limit=10
```
예를 들어 다음을 방문하면:
```
http://localhost:8000/api/weapons?offset=20
```

함수의 파라미터 값은 다음과 같습니다:

 - `offset=20` (URL에서 설정했기 때문)
 - `limit=10` (기본값이기 때문)


### 필수 및 선택 파라미터

Python 함수 파라미터를 선언하는 것과 동일한 방식으로 필수 또는 선택 GET 파라미터를 선언할 수 있습니다:

```python hl_lines="5"
{!./src/tutorial/query/code02.py!}
```

이 경우 **Django Ninja**는 GET 요청에서 전달하는 `q` 파라미터를 항상 검증하며, `offset` 파라미터는 선택적인 정수입니다.

### GET 파라미터 타입 변환

타입이 지정된 여러 파라미터를 선언해 보겠습니다:
```python hl_lines="5"
{!./src/tutorial/query/code03.py!}
```
`str` 타입은 그대로 전달됩니다.

`bool` 타입의 경우, 다음 모든 값에 대해:
```
http://localhost:8000/api/example?b=1
http://localhost:8000/api/example?b=True
http://localhost:8000/api/example?b=true
http://localhost:8000/api/example?b=on
http://localhost:8000/api/example?b=yes
```
또는 대소문자 변형(대문자, 첫 글자만 대문자 등)에 대해, 함수는 파라미터 `b`가 `bool` 값 `True`임을 인식하며, 그 외의 경우 `False`입니다.

날짜는 날짜 문자열과 정수(Unix 타임스탬프)가 될 수 있습니다:

<pre style="font-size: .85em; background-color:rgb(245, 245, 245);">
http://localhost:8000/api/example?d=<strong>1577836800</strong>  # equivalent to 2020-01-01
http://localhost:8000/api/example?d=<strong>2020-01-01</strong>
</pre>


### Schema 사용

스키마를 사용하여 GET 파라미터를 캡슐화할 수도 있습니다:

```python hl_lines="1 2  5 6 7 8"
{!./src/tutorial/query/code010.py!}
```

더 복잡한 필터링 시나리오는 [필터링](./filtering.md)을 참조하세요.

!!! done

    다음 챕터로 계속 진행하세요! **[Request Body](body.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
