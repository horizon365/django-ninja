---
comments: true
---
# 빠른 예제
## 🌞 작동 방식

대학교를 위한 시스템을 구축하고 있고 `Department`라는 모델이 있다고 상상해 봅시다. 대학의 각 학과에는 고유한 제목이 있습니다.

```python
# examples/models.py
from django.db import models

class Department(models.Model):
    title = models.CharField(max_length=255, unique=True)
```

이 데이터와 상호 작용하려면 Python 객체와 JSON과 같이 읽고 쓰기 쉬운 형식 사이를 왕복 변환하는 방법이 필요합니다. Django Ninja에서는 이를 위해 "Schema"를 사용합니다:

```python
# examples/schemas.py
from ninja import Schema

class DepartmentIn(Schema):
    title: str

class DepartmentOut(Schema):
    id: int
    title: str
```

`DepartmentIn` 스키마는 학과를 생성하거나 업데이트할 때 필요한 데이터를 정의합니다. `DepartmentOut` 스키마는 학과를 조회할 때 제공할 데이터를 정의합니다.

이제 이 패키지의 강력함이 나옵니다. 이를 사용하면 몇 줄의 코드만으로 `Department` 모델에 대한 **CRUD** 작업을 설정할 수 있습니다:


```python
# examples/views/department_views.py
from typing import List
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja_crud import views, viewsets

from examples.models import Department
from examples.schemas import DepartmentIn, DepartmentOut

api = NinjaAPI()


class DepartmentViewSet(viewsets.APIViewSet):
    api = api
    model = Department

    list_departments = views.ListView(
        response_body=List[DepartmentOut]
    )
    create_department = views.CreateView(
        request_body=DepartmentIn,
        response_body=DepartmentOut,
    )
    read_department = views.ReadView(
        response_body=DepartmentOut
    )
    update_department = views.UpdateView(
        request_body=DepartmentIn,
        response_body=DepartmentOut,
    )
    delete_department = views.DeleteView()


# In addition to the CRUD operations managed by the viewset,
# the api or router can be used in the standard Django Ninja way
@api.get("/statistics/", response=dict)
def get_department_statistics(request: HttpRequest):
    return {"total": Department.objects.count()}
```

그리고 뷰셋이 위와 같이 간단하다면 `APIViewSet` 클래스를 활용하여 기본 요청 및 응답 본문으로 더 깔끔한 방식으로 정의할 수 있습니다:
```python
# examples/views/department_views.py
from ninja import NinjaAPI
from ninja_crud import views, viewsets

from examples.models import Department
from examples.schemas import DepartmentIn, DepartmentOut

api = NinjaAPI()


class DepartmentViewSet(viewsets.APIViewSet):
    api = api
    model = Department
    default_request_body = DepartmentIn
    default_response_body = DepartmentOut

    list_departments = views.ListView()
    create_department = views.CreateView()
    read_department = views.ReadView()
    update_department = views.UpdateView()
    delete_department = views.DeleteView()
```

## ☔️ 시나리오 기반 테스팅

Django Ninja CRUD는 [Django REST Testing](https://github.com/hbakri/django-rest-testing)과 원활하게 통합되며 CRUD 엔드포인트의 포괄적인 커버리지와 견고한 검증을 보장합니다.
처음에 테스팅 프레임워크는 이 패키지의 일부였지만, 더 많은 유연성을 허용하고 Django Ninja 외에 다른 Django REST 프레임워크와 함께 사용할 수 있도록 나중에 자체 패키지로 분리되었습니다.

이 패키지를 사용하면 다음을 수행할 수 있습니다:
- **테스트 시나리오를 선언적으로 정의**: 각 시나리오에 대한 예상 요청 및 응답 세부 정보를 지정하여 테스트를 자체 문서화하고 이해하기 쉽게 만듭니다.
- **광범위한 조건 테스트**: 유효하고 유효하지 않은 입력, 존재하지 않는 리소스, 커스텀 비즈니스 규칙을 포함한 다양한 조건에서 엔드포인트 동작을 검증합니다.
- **명확성과 유지 관리성 향상**: 테스트를 모듈식의 관리 가능한 단위로 분해하여 코드 구성을 개선하고 기술 부채를 줄입니다.
- **포괄적인 커버리지 보장**: 시나리오 기반 접근 방식 덕분에 엔드포인트를 엄격하게 테스트하여 테스트되지 않은 케이스가 남지 않습니다.

테스트에서 `ObjectDoesNotExist`와 같은 예외를 처리하고 적절한 응답을 반환하려면 다음과 같이 예외 핸들러를 정의할 수 있습니다:

```python
# examples/exception_handlers.py
from ninja import NinjaAPI
from django.core.exceptions import ObjectDoesNotExist

api = NinjaAPI()


@api.exception_handler(ObjectDoesNotExist)
def handle_object_does_not_exist(request, exc):
    return api.create_response(
        request,
        {"message": "ObjectDoesNotExist", "detail": str(exc)},
        status=404,
    )

# ... other exception handlers
```

이제 시나리오 기반 테스팅 프레임워크를 사용하여 CRUD 뷰에 대한 테스트를 작성할 수 있습니다:

```python
# examples/tests/test_department_views.py
from examples.models import Department
from examples.schemas import DepartmentOut

from ninja_crud.testing import APITestCase, APIViewTestScenario


class TestDepartmentViewSet(APITestCase):
    department: Department

    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(title="department")

    def test_read_department(self):
        self.assertScenariosSucceed(
            method="GET",
            path="/api/departments/{id}",
            scenarios=[
                APIViewTestScenario(
                    path_parameters={"id": self.department.id},
                    expected_response_status=200,
                    expected_response_body_type=DepartmentOut,
                    expected_response_body={
                        "id": self.department.id,
                        "title": self.department.title,
                    },
                ),
                APIViewTestScenario(
                    path_parameters={"id": 9999},
                    expected_response_status=404,
                ),
            ],
        )
```

Django Ninja CRUD의 선언적 뷰와 Django REST Testing의 시나리오 기반 테스팅 기능을 결합하면 견고하고 잘 테스트된 RESTful API를 쉽고 자신 있게 구축하고 유지 관리할 수 있습니다.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
