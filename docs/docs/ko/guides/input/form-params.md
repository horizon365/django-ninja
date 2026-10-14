---
comments: true
---
# 폼 데이터

**Django Ninja**는 `request.POST` 데이터(`application/x-www-form-urlencoded` 또는 `multipart/form-data`)도 파싱하고 검증할 수 있습니다.

## 파라미터로서의 폼 데이터

```python hl_lines="1 4"
from ninja import NinjaAPI, Form

@api.post("/login")
def login(request, username: Form[str], password: Form[str]):
    return {'username': username, 'password': '*****'}
```

다음 사항에 유의하세요:

1) `ninja`에서 `Form` 클래스를 임포트해야 합니다
```python
from ninja import Form
```

2) 파라미터의 기본값으로 `Form`을 사용합니다:
```python
username: Form[str]
```

## Schema 사용

[Request Body](body.md#declare-it-as-a-parameter)와 유사하게, 스키마를 사용해 파라미터를 구성할 수 있습니다.

```python hl_lines="12"
{!./src/tutorial/form/code01.py!}
```

## Request 폼 + Path + Query 파라미터

[Request Body](body.md#request-body-path-query-parameters)와 유사하게, 폼 데이터를 다른 파라미터 소스와 결합할 수 있습니다.

Query 파라미터**와** path 파라미터**와** 폼 필드 **등**을 동시에 선언할 수 있습니다.

**Django Ninja**는 path 파라미터와 이름이 일치하는 함수 파라미터는 **path에서 가져와야** 하고, `Form(...)`으로 선언된 함수 파라미터는 **request 폼 필드에서 가져와야** 한다는 것을 인식합니다.

```python hl_lines="12"
{!./src/tutorial/form/code02.py!}
```
## 빈 폼 필드를 기본값으로 매핑

선택적 폼 필드는 빈 값으로 전송되는 경우가 많습니다. 이 값은 빈 문자열로 해석되므로, `int`나 `bool` 같은 필드에서는 검증에 실패할 수 있습니다.

Pydantic 문서에 설명된 것처럼, [제네릭 클래스를 타입으로 사용](https://pydantic.com.cn/usage/types/#generic-classes-as-types)하면 이 문제를 해결할 수 있습니다.

```python hl_lines="15 16 23-25"
{!./src/tutorial/form/code03.py!}
```

!!! done

    다음 챕터로 계속 진행하세요! **[파일 업로드](file-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
