---
comments: true
---
# 快速示例
## 🌞 工作原理

让我们想象一下，你正在为一所大学构建一个系统，并且有一个名为 `Department`（部门）的模型。你大学里的每个部门都有一个独特的标题。

```python
# examples/models.py
from django.db import models

class Department(models.Model):
    title = models.CharField(max_length=255, unique=True)
```

为了与这些数据交互，我们需要一种方法将其在 Python 对象和一种易于读写的格式（如 JSON）之间进行转换。在 Django Ninja 中，我们使用“Schema”（模式）来实现这一点：

```python
# examples/schemas.py
from ninja import Schema

class DepartmentIn(Schema):
    title: str

class DepartmentOut(Schema):
    id: int
    title: str
```

`DepartmentIn` 模式定义了我们在创建或更新一个部门时所需的数据。 `DepartmentOut` 模式定义了我们在检索一个部门时将提供的数据。

现在，这个包的强大之处来了。有了它，你可以用仅仅几行代码为 `Department` 模型设置 **CRUD** 操作：


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


# 除了视图集管理的 CRUD 操作外，
# api 或路由器可以按照标准的 Django Ninja 方式使用
@api.get("/statistics/", response=dict)
def get_department_statistics(request: HttpRequest):
    return {"total": Department.objects.count()}
```

并且如果你的视图集像上面那个一样简单，你可以利用 `APIViewSet` 类以一种更简洁的方式来定义它，具有默认的请求和响应主体：
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

## ☔️ 基于场景的测试

Django Ninja CRUD 与 [Django REST Testing](https://github.com/hbakri/django-rest-testing), 无缝集成，并确保对你的 CRUD 端点进行全面覆盖和强大的验证。
起初，测试框架是这个包的一部分，但后来被提取到它自己的包中，以允许有更多的灵活性，并能与 Django Ninja 以外的其他 Django REST 框架一起使用。

有了这个包，你可以：
- **声明式定义测试场景**：为每个场景指定预期的请求和响应细节，使你的测试具有自文档化且易于理解。
- **测试各种条件**：在各种条件下验证端点行为，包括有效和无效输入、不存在的资源和自定义业务规则。
- **提高清晰度和可维护性**：将测试分解为模块化、可管理的单元，改善代码组织并减少技术债务。
- **确保全面覆盖**：由于基于场景的方法，严格测试你的端点，不遗漏任何情况。

为了在你的测试中处理像 `ObjectDoesNotExist` 这样的异常并返回适当的响应，你可以像这样定义一个异常处理程序：

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

# ... 其他异常处理程序
```

现在，你可以使用基于场景的测试框架为你的 CRUD 视图编写测试：

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

通过将 Django Ninja CRUD 的声明式视图与 Django REST 测试的基于场景的测试能力相结合，你可以轻松自信地构建和维护强大、经过良好测试的 RESTful API。
<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
