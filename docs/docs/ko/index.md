---
title: Django Ninja - 빠른 Django REST 프레임워크
template: home.html
comments: true
---

Django Ninja는 Django와 Python 3.6+ 타입 힌트를 사용하여 API를 구축하기 위한 웹 프레임워크입니다.

주요 특징:

 - **이해하기 쉬움**: 사용하기 쉽고 직관적이 되도록 설계되었습니다.
 - **빠른 실행 속도**: **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>**과 **<a href="guides/async-support/">async support</a>** 덕분에 매우 높은 성능을 자랑합니다.
 - **빠른 코딩**: Django Ninja는 Django와 Python 3.6+ 타입 힌트를 사용하여 API를 구축하기 위한 웹 프레임워크입니다.
 - **표준 기반**: **OpenAPI** (구 Swagger)와 **JSON Schema** 표준을 기반으로 합니다.
 - **Django 친화적**: (당연하게도) Django 코어 및 ORM과 잘 통합됩니다.
 - **프로덕션 준비 완료**: 여러 회사가 실제 프로젝트에서 사용하고 있습니다 (Django Ninja를 사용 중이시고 피드백을 공유하고 싶으시다면 ppr.vitaly@gmail.com으로 이메일을 보내주세요).

<a href="https://github.com/vitalik/django-ninja-benchmarks" target="_blank">벤치마크</a>:

![Django Ninja REST Framework](img/benchmark.png)

## 설치

```
pip install django-ninja
```

## 간단한 예제

새 Django 프로젝트를 시작합니다 (또는 기존 프로젝트를 사용하세요)
```
django-admin startproject apidemo
```

`urls.py`에서

```python hl_lines="3 5 8 9 10 15"
{!./src/index001.py!}
```

이제 평소처럼 실행합니다:
```
./manage.py runserver
```

참고: Django Ninja가 동작하도록 installed apps에 추가할 필요는 없습니다.

## 확인해 보기

브라우저에서 <a href="http://127.0.0.1:8000/api/add?a=1&b=2" target="_blank">http://127.0.0.1:8000/api/add?a=1&b=2</a>를 열어보세요.

다음과 같은 JSON 응답을 볼 수 있습니다:
```JSON
{"result": 3}
```
이제 방금 만든 API는:

 - `/api/add` 경로로 HTTP GET 요청을 받고
 - GET 파라미터 `a`와 `b`를 받아 검증하고 타입을 변환하며
 - 결과를 JSON으로 인코딩하고
 - 정의된 operation에 대한 OpenAPI schema를 생성합니다

## 인터랙티브 API 문서

이제 <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>로 이동해 보세요.

자동 생성된 인터랙티브 API 문서를 볼 수 있습니다 (<a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a> 또는 <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a> 제공):

![Swagger UI](img/index-swagger-ui.png)


## 요약

요약하면, 파라미터, request body 등의 타입을 함수 인자로 **한 번만** 선언하면 됩니다.

표준적이고 현대적인 Python 타입을 사용하여 이를 수행합니다.

새로운 문법이나 특정 라이브러리의 메서드나 클래스 등을 배울 필요가 없습니다.

그저 표준 **Python 3.6+**만 있으면 됩니다.

예를 들어, `int`의 경우:

```python
a: int
```

또는, 더 복잡한 `Item` 모델의 경우:

```python
class Item(Schema):
    foo: str
    bar: float

def operation(a: Item):
    ...
```

...이 한 번의 선언만으로 다음을 얻을 수 있습니다:

* 다음을 포함한 에디터 지원:
    * 자동 완성
    * 타입 검사
* 데이터 검증:
    * 데이터가 유효하지 않을 때 명확하고 자동적인 에러
    * 깊게 중첩된 JSON 객체에 대한 검증까지 지원
* 네트워크 입력 데이터의 <abbr title="serialization, parsing, marshalling이라고도 함">직렬화</abbr> 및 Python 데이터 출력으로 변환, 다음으로부터 읽기:
    * JSON
    * Path 파라미터
    * Query 파라미터
    * Cookies
    * Headers
    * Forms
    * Files
* 자동 생성되는 인터랙티브 API 문서

이 프로젝트는 <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a>로부터 큰 영감을 받았습니다.

!!! note

    빠르게 시작하려면 **[튜토리얼](tutorial/index.md)**을 확인해 보세요.

    Django Ninja를 둘러싼 생태계:

    1. [django-ninja](index.md): Django를 기반으로 Django의 장점을 살리고 Pydantic의 강력함과 결합한 프레임워크 — 보안과 편의성의 교차점에서 최적의 선택입니다.

    2. [django-ninja-crud](django-ninja-crud/index.md): django-ninja 위에 구축되어 CRUD 인터페이스 개발을 단순화하고, 선언적 model viewset과 시나리오 기반 테스트 방법을 제공하는 프레임워크입니다.

    3. [django-ninja-extra](django-ninja-extra/index.md): 개발자가 방대한 Django 문서를 건너뛰고 최소한의 코드로 강력한 웹 애플리케이션과 현대적인 API 인터페이스를 빠르게 구축할 수 있게 해주는 도구입니다.

    4. [django-ninja-jwt](django-ninja-jwt/index.md): django-ninja를 위한 JSON Web Token 플러그인으로, 인증 및 관련 기능을 구현하며 인기 있는 Django Rest Framework 플러그인에서 포크되었습니다.
