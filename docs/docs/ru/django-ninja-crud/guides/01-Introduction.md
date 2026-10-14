---
comments: true
---
# Введение
Django Ninja CRUD — это мощный, [декларативный](https://en.wikipedia.org/wiki/Declarative_programming), но слегка opinionated фреймворк, который упрощает разработку **CRUD**-эндпоинтов ([**C**reate, **R**ead, **U**pdate, **D**elete](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)) с [Django Ninja](https://github.com/vitalik/django-ninja),
а также предоставляет декларативный, сценарный подход к тестированию этих API-эндпоинтов с помощью [Django REST Testing](https://github.com/hbakri/django-rest-testing).

## 🍓 Переосмысление декларативных CRUD Viewsets  

Шагните в будущее CRUD-операций Django с нашими модельными viewsets. Наш фреймворк переосмысливает создание эндпоинтов через декларативную призму, превращая сложные процессы в лаконичный, читаемый код. Построенный на лучших практиках, модельный viewset воплощает суть эффективного и надёжного дизайна. Декларативно указывая модель и схемы, вы можете быстро генерировать полноценные CRUD-операции, освобождая себя для решения действительно важных задач. Именно здесь начинается путь переосмысления разработки веб-приложений.
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
## Решаемая проблема
Он позволяет определять общие эндпоинты как class-based views и легко настраивать их в соответствии с соглашениями вашего проекта, а также легко создавать собственные кастомные views и объявлять их вместе с предоставленными CRUD-views, способствуя модульности и расширяемости.
Этот пакет поощряет фокусировку на самом важном: **решении реальных задач**, а не изобретении велосипеда по всему проекту.

Изначально вдохновлённый [ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset) из DRF,
Django Ninja CRUD развился, чтобы устранить его ограничения, приняв подход [композиции вместо наследования](https://en.wikipedia.org/wiki/Composition_over_inheritance)
для достижения истинной модульности — основополагающего шага к более широкому декларативному подходу к созданию API-эндпоинтов.

Проблемы, с которыми сталкиваются существующие viewsets, основанные на наследовании:

- **Уникальность CRUD-эндпоинтов для каждой модели**: Django Ninja CRUD позволяет определять несколько эндпоинтов для одной и той же модели, обеспечивая версионирование или альтернативные представления.    
- **Недостаток гибкости кастомизации**: вместо переопределения методов в монолитном классе отдельные views можно настраивать через композицию и конфигурацию.         
- **Неявные связи внутри иерархий наследования**: композиция развязывает views, уменьшая зависимости и улучшая повторное использование.       
- **Недостаток модульности для новых эндпоинтов**: добавление кастомных эндпоинтов больше не требует наследования всего viewset, что упрощает постепенное внедрение новых функций.      

## ✨ Ключевые особенности
- **Полностью декларативный**: определяйте views и тесты, объявляя, что вы хотите получить, а не как это сделать.
- **Непревзойдённая модульность**: настраивайте свои viewsets нужными CRUD-views, изменяя поведение каждого view.
- **Сценарный фреймворк тестирования**: используйте сценарный фреймворк тестирования, чтобы декларативно и лаконично определять разнообразные тест-кейсы.
- **Фокус на главном**: тратьте больше времени на решение реальных задач и меньше — на общие, повторяющиеся задачи.

> Тестируйте точно с помощью тест-кейсов модельных viewsets

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

**Django Ninja CRUD — это больше, чем инструмент; это смена парадигмы в разработке и тестировании веб-приложений на Django.**



## 💬 Что дальше?


!!! success

    Переходите к следующей главе **[Как установить](02-Installation.md)**.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
