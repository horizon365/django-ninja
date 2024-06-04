---
comments: true
---
# 介绍
Django Ninja CRUD 是一个强大的, [声明式的](https://en.wikipedia.org/wiki/Declarative_programming), 但也有点执着的框架，它使用[Django Ninja](https://github.com/vitalik/django-ninja)
简化了CRUD **CRUD** ([**C**创建, **R**读取, **U**更新, **D**删除](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete))
接口的开发，并且还使用[Django REST Testing](https://github.com/hbakri/django-rest-testing) 为测试这些API接口提供了一种声明式的基于场景的方法。

## 🍓重新定义声明式 CRUD 视图集  

通过我们的模型视图集踏入 Django CRUD 操作的未来。我们的框架通过声明式视角重新构想端点创建，将复杂过程简化为简洁、可读的代码。基于最佳实践，模型视图集封装了高效和稳健设计的精髓。通过声明式地指定模型和模式，您可以快速生成成熟的 CRUD 操作，让您有自由去应对真正重要的挑战。这就是重新定义网络应用程序开发之旅开始的地方。
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
## 要解决的问题
它允许你将常见端点定义为基于类的视图，并轻松地对其进行定制以符合你的项目约定，还可以轻松创建你自己的自定义视图并与提供的 CRUD 视图一起声明，促进了模块性和可扩展性。
这个包鼓励关注最重要的事情：**解决实际问题**，而不是在你的整个项目中重复造轮子。

最初受到 DRF 的 [ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset)启发，
Django Ninja CRUD 演变为解决其局限性, 采用[组合优于继承](https://en.wikipedia.org/wiki/Composition_over_inheritance)
的方法来实现真正的模块性——这是朝着更广泛的声明式创建 API 接口迈出的基础一步。

已有的基于继承的视图集的面临的问题：

- **每个模型的 CRUD 端点的唯一性**: Django Ninja CRUD 允许你为同一模型定义多个端点，实现版本控制或替代表示。    
- **定制灵活性不足**: 不是在一个整体类上重写方法，而是可以通过组合和配置来定制单个视图。         
- **继承层次结构内的隐含关系**: 组合解耦视图，减少依赖并提高可重用性。       
- **新端点缺乏模块性**: 添加自定义端点不再需要子类化整个视图集，使得逐步引入新功能更容易。      

## ✨ 主要特性
- **纯粹声明式**: 通过声明你想要什么而不是如何去做来定义视图和测试。
- **无与伦比的模块性**：用所需的 CRUD 视图定制你的视图集，定制每个视图的行为。
- **基于场景的测试框架**：利用基于场景的测试框架简洁地声明性地定义各种测试用例。
- **关注重要事项**：花更多时间解决现实世界的问题，而减少在常见和重复任务上的时间。

> 使用模型视图集测试用例进行精确测试

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

**Django Ninja CRUD 不仅仅是一个工具; 它是 Django 网络应用开发和测试中的一种范式转变。**



## 💬 下一步?


!!! 大功告成

    继续下一章节 **[如何安装](02-Installation.md)**.