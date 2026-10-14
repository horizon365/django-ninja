---
comments: true
---
# Request Body

Request body는 일반적으로 "create" 및 "update" operation(POST, PUT, PATCH)에서 사용됩니다.
예를 들어, POST나 PUT으로 리소스를 생성할 때 request body에는 일반적으로 생성할 리소스의 표현(representation)이 담깁니다.

Request body를 선언하려면 **Django Ninja의 `Schema`**를 사용해야 합니다.

!!! note
    내부적으로 **Django Ninja**는 <a href="https://pydantic.com.cn/" class="external-link" target="_blank">Pydantic</a> Model의 모든 강력한 기능을 활용합니다.
    Django models 작업 시 코드 혼란을 피하기 위해 `Schema`라는 별칭이 선택되었습니다. Pydantic의 model 클래스는 기본적으로 `Model`이라는 이름을 가지며, 이는 Django의 `Model` 클래스와 충돌하기 때문입니다.
    

## Schema 임포트

먼저 `ninja`에서 `Schema`를 임포트해야 합니다:

```python hl_lines="2"
{!./src/tutorial/body/code01.py!}
```

## 데이터 모델 만들기

그다음 `Schema`를 상속하는 클래스로 데이터 모델을 선언합니다.

모든 속성에는 표준 Python 타입을 사용하세요:

```python hl_lines="5 6 7 8 9"
{!./src/tutorial/body/code01.py!}
```

참고: 속성의 기본값을 **`None`**으로 설정하면 request body에서 선택적(optional)이 됩니다. 예를 들어 위 모델은 다음과 같은 JSON "`object`"(Python `dict`)를 선언합니다:

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...`description`은 선택적이므로(기본값이 `None`), 다음 JSON "`object`"도 유효합니다:

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```

## 파라미터로 선언하기

*path operation*에 추가하려면 path 파라미터와 query 파라미터를 선언하는 것과 동일한 방식으로 선언합니다:


```python hl_lines="13"
{!./src/tutorial/body/code01.py!}
```

... 그리고 타입을 여러분이 만든 `Item` 모델로 선언합니다.

## 결과

Python 타입 선언만으로 **Django Ninja**가 다음을 수행합니다:

* Request body를 JSON으로 읽습니다.
* 적절한 타입으로 변환합니다(필요한 경우).
* 데이터를 검증합니다.
    * 데이터가 유효하지 않으면, 잘못된 데이터의 위치와 내용을 정확히 알려주는 친절하고 의미 있는 에러를 반환합니다.
* 받은 데이터를 `item` 파라미터로 제공합니다.
    * 함수에서 타입을 `Item`으로 선언했기 때문에, 모든 속성과 그 타입에 대해 에디터 지원(자동 완성 등)도 받을 수 있습니다.
* 모델에 대한 <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> 정의를 생성하며, 프로젝트에서 필요한 어디에서든 사용할 수 있습니다.
* 이 스키마들은 생성된 OpenAPI 스키마의 일부가 되어 자동 문서 <abbr title="User Interfaces">UI</abbr>에서 사용됩니다.

## 자동 문서화

모델의 JSON Schema는 생성된 OpenAPI 스키마의 일부가 되어 인터랙티브 API 문서에 표시됩니다:

![Openapi schema](../../img/body-schema-doc.png)

...그리고 이를 필요로 하는 모든 *path operation*의 API 문서에서도 사용됩니다:

![Openapi schema](../../img/body-schema-doc2.png)

## 에디터 지원

에디터에서 함수 내부를 보면 어디에서나 타입 힌트와 자동 완성을 사용할 수 있습니다(Schema 객체 대신 `dict`를 사용하면 이런 지원을 받을 수 없습니다):

![Type hints](../../img/body-editor.gif)


위 스크린샷은 <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>를 사용한 것입니다.

<a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>과 그 외 대부분의 Python 에디터에서도 동일한 에디터 지원을 받을 수 있습니다.

## Request Body + Path 파라미터

Path 파라미터**와** request body를 동시에 선언할 수 있습니다.


**Django Ninja**는 path 파라미터와 이름이 일치하는 함수 파라미터는 **path에서** 가져와야 하고, `Schema`로 선언된 함수 파라미터는 **request body에서** 가져와야 한다는 것을 인식합니다.

```python hl_lines="11 12"
{!./src/tutorial/body/code02.py!}
```

## Request Body + Path + Query 파라미터

**Request body**, **path**, **query** 파라미터를 동시에 선언할 수도 있습니다.

**Django Ninja**는 각 파라미터를 인식하여 올바른 위치에서 데이터를 가져옵니다.

```python hl_lines="11 12"
{!./src/tutorial/body/code03.py!}
```

함수 파라미터는 다음과 같이 인식됩니다:

* 파라미터가 **path**에도 선언되어 있으면 path 파라미터로 사용됩니다.

 
* 파라미터가 **단일 타입**(`int`, `float`, `str`, `bool` 등)이면 **query** 파라미터로 해석됩니다.
* 파라미터가 **Schema**(또는 Pydantic `BaseModel`) 타입으로 선언되면 **request body**로 해석됩니다.

!!! done

    다음 챕터로 계속 진행하세요! **[폼 데이터](form-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
