---
comments: true
---
# Introduction
Django Ninja CRUD is a powerful, [declarative](https://en.wikipedia.org/wiki/Declarative_programming), yet slightly opinionated framework that simplifies the development of **CRUD** ([**C**reate, **R**ead, **U**pdate, **D**elete](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)) endpoints with [Django Ninja](https://github.com/vitalik/django-ninja),
and also provides a declarative, scenario-based approach for testing these API endpoints using [Django REST Testing](https://github.com/hbakri/django-rest-testing).

## 🍓 Redefining Declarative CRUD Viewsets  

Step into the future of Django CRUD operations with our model viewsets. Our framework reimagines endpoint creation through a declarative lens, transforming complex processes into concise, readable code. Built on best practices, the model viewsets encapsulate the essence of efficient and robust design. By declaratively specifying the model and schemas, you can quickly generate full-fledged CRUD operations, freeing you to tackle the challenges that truly matter. This is where the journey of redefining web application development begins.
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
## The Problem to Solve
It allows you to define common endpoints as class-based views and easily customize them to fit your project's conventions, and to easily create your own custom views and declare them alongside the provided CRUD views, promoting modularity and extensibility.
This package encourages focusing on what matters most: **solving real-world problems**, rather than reinventing the wheel throughout your project.

Originally inspired by DRF's [ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset),
Django Ninja CRUD evolved to address its limitations, adopting a [composition over inheritance](https://en.wikipedia.org/wiki/Composition_over_inheritance)
approach to achieve true modularity — a foundational step toward a broader declarative approach to creating API endpoints.

Challenges faced by existing inheritance-based viewsets:

- **Uniqueness of CRUD endpoints per model**: Django Ninja CRUD allows you to define multiple endpoints for the same model, enabling versioning or alternative representations.    
- **Lack of customization flexibility**: instead of overriding methods on a monolithic class, individual views can be customized through composition and configuration.         
- **Implicit relationships within inheritance hierarchies**: composition decouples views, reducing dependencies and improving reusability.       
- **Lack of modularity for new endpoints**: adding custom endpoints no longer requires subclassing the entire viewset, making it easier to introduce new features incrementally.      

## ✨ Key Features
- **Purely declarative**: define views and tests by declaring what you want, rather than how to do it.
- **Unmatched modularity**: customize your viewsets with the desired CRUD views, customizing the behavior of each view.
- **Scenario-based testing framework**: leverage the scenario-based testing framework to declaratively and concisely define diverse test cases.
- **Focus on what matters**: spend more time solving real-world problems and less on common, repetitive tasks.

> Test precisely with model viewset test cases

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

**Django Ninja CRUD is more than a tool; it is a paradigm shift in Django web application development and testing.**



## 💬 What's Next?


!!! success

    Continue to the next chapter **[How to Install](02-Installation.md)**.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
