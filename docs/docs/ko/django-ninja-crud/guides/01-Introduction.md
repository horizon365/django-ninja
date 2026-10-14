---
comments: true
---
# 소개
Django Ninja CRUD는 강력하고 [선언적](https://en.wikipedia.org/wiki/Declarative_programming)이면서도 다소 독선적인 프레임워크로, [Django Ninja](https://github.com/vitalik/django-ninja)를 사용한 **CRUD** ([**C**reate, **R**ead, **U**pdate, **D**elete](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)) 엔드포인트 개발을 단순화하며,
또한 [Django REST Testing](https://github.com/hbakri/django-rest-testing)을 사용하여 이러한 API 엔드포인트를 테스트하기 위한 선언적이고 시나리오 기반 접근 방식을 제공합니다.

## 🍓 선언적 CRUD 뷰셋의 재정의  

모델 뷰셋으로 Django CRUD 작업의 미래로 들어가 보세요. 우리 프레임워크는 선언적 렌즈를 통해 엔드포인트 생성을 재구상하여 복잡한 프로세스를 간결하고 읽기 쉬운 코드로 변환합니다. 모범 사례를 기반으로 구축된 모델 뷰셋은 효율적이고 견고한 설계의 본질을 캡슐화합니다. 모델과 스키마를 선언적으로 지정함으로써 완전한 CRUD 작업을 빠르게 생성할 수 있어, 정말 중요한 과제에 집중할 수 있습니다. 이곳이 웹 애플리케이션 개발을 재정의하는 여정이 시작되는 곳입니다.
```python
from ninja import Router
from ninja_crud import views, viewsets

from examples.models import Department
from examples.schemas import DepartmentIn, DepartmentOut

router = Router()


class DepartmentViewSet(viewsets.ModelViewSet):
    model = Department
    default_input_schema = DepartmentIn
    default_output_schema = DepartmentOut

    list_view = views.ListModelView()
    create_view = views.CreateModelView()
    retrieve_view = views.RetrieveModelView()
    update_view = views.UpdateModelView()
    delete_view = views.DeleteModelView()


DepartmentViewSet.register_routes(router)
```
## 해결하려는 문제
일반적인 엔드포인트를 클래스 기반 뷰로 정의하고 프로젝트의 관례에 맞게 쉽게 커스터마이즈할 수 있으며, 자체 커스텀 뷰를 쉽게 만들어 제공된 CRUD 뷰와 함께 선언함으로써 모듈성과 확장성을 촉진할 수 있습니다.
이 패키지는 가장 중요한 것, 즉 프로젝트 전반에 걸쳐 바퀴를 재발명하는 대신 **실제 문제를 해결하는 데** 집중하도록 권장합니다.

원래 DRF의 [ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset)에서 영감을 받은
Django Ninja CRUD는 그 한계를 해결하기 위해 발전하여, [상속보다는 합성](https://en.wikipedia.org/wiki/Composition_over_inheritance)
접근 방식을 채택하여 진정한 모듈성을 달성했습니다 — 이는 API 엔드포인트 생성을 위한 더 넓은 선언적 접근 방식을 향한 기초적인 단계입니다.

기존 상속 기반 뷰셋이 직면한 과제:

- **모델당 CRUD 엔드포인트의 고유성**: Django Ninja CRUD를 사용하면 동일한 모델에 대해 여러 엔드포인트를 정의하여 버전 관리 또는 대체 표현을 가능하게 합니다.    
- **커스터마이징 유연성 부족**: 모놀리식 클래스의 메서드를 오버라이드하는 대신 개별 뷰가 합성과 구성을 통해 커스터마이즈될 수 있습니다.         
- **상속 계층 내의 암시적 관계**: 합성은 뷰를 분리하여 종속성을 줄이고 재사용성을 향상시킵니다.       
- **새 엔드포인트에 대한 모듈성 부족**: 커스텀 엔드포인트를 추가하는 데 더 이상 전체 뷰셋을 서브클래싱할 필요가 없어 새로운 기능을 점진적으로 도입하기 쉬워집니다.      

## ✨ 주요 기능
- **순수하게 선언적**: 수행 방법이 아닌 원하는 것을 선언하여 뷰와 테스트를 정의합니다.
- **비교할 수 없는 모듈성**: 원하는 CRUD 뷰로 뷰셋을 커스터마이즈하고 각 뷰의 동작을 커스터마이즈합니다.
- **시나리오 기반 테스트 프레임워크**: 시나리오 기반 테스트 프레임워크를 활용하여 다양한 테스트 케이스를 선언적이고 간결하게 정의합니다.
- **중요한 것에 집중**: 일반적이고 반복적인 작업에 더 적은 시간을, 실제 문제 해결에 더 많은 시간을 사용합니다.

> 모델 뷰셋 테스트 케이스로 정밀하게 테스트하세요

```python
from ninja_crud import testing

from examples.models import Department
from examples.views import DepartmentViewSet


class TestDepartmentViewSet(testing.viewsets.ModelViewSetTestCase):
    model_viewset_class = DepartmentViewSet
    base_path = "api/departments"

    @classmethod
    def setUpTestData(cls):
        cls.department_1 = Department.objects.create(title="department-1")
        cls.department_2 = Department.objects.create(title="department-2")

    @property
    def path_parameters(self):
        return testing.components.PathParameters(
            ok={"id": self.department_1.id},
            not_found={"id": 999}
        )

    @property
    def payloads(self):
        return testing.components.Payloads(
            ok={"title": "department-3"},
            bad_request={"title": ""},
            conflict={"title": self.department_2.title}
        )

    test_list_view = testing.views.ListModelViewTest()
    test_create_view = testing.views.CreateModelViewTest(payloads)
    test_retrieve_view = testing.views.RetrieveModelViewTest(path_parameters)
    test_update_view = testing.views.UpdateModelViewTest(path_parameters, payloads)
    test_delete_view = testing.views.DeleteModelViewTest(path_parameters)

```

**Django Ninja CRUD는 단순한 도구 그 이상입니다; 이는 Django 웹 애플리케이션 개발 및 테스트의 패러다임 전환입니다.**



## 💬 다음은 무엇인가요?


!!! success

    다음 장 **[설치 방법](02-Installation.md)**으로 계속 진행하세요.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
