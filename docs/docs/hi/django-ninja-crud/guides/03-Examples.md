---
comments: true
---
# Quick Examples
## 🌞 यह कैसे काम करता है

चलिए मान लेते हैं कि आप एक university के लिए एक system बना रहे हैं, और आपके पास `Department` नाम का एक model है। आपकी university के प्रत्येक department का एक unique title है।

```python
# examples/models.py
from django.db import models

class Department(models.Model):
    title = models.CharField(max_length=255, unique=True)
```

इस data के साथ interact करने के लिए, हमें इसे Python objects और एक ऐसे format के बीच आगे-पीछे बदलने का एक तरीका चाहिए जो पढ़ने और लिखने में आसान हो, जैसे JSON। Django Ninja में, हम इसके लिए "Schema" का उपयोग करते हैं:

```python
# examples/schemas.py
from ninja import Schema

class DepartmentIn(Schema):
    title: str

class DepartmentOut(Schema):
    id: int
    title: str
```

`DepartmentIn` schema वह data परिभाषित करता है जिसकी हमें एक department create या update करते समय आवश्यकता होती है। `DepartmentOut` schema वह data परिभाषित करता है जिसे हम एक department retrieve करते समय प्रदान करेंगे।

अब, इस package की शक्ति यहाँ आती है। इसके साथ, आप कोड की कुछ ही lines में `Department` model के लिए **CRUD** operations सेट अप कर सकते हैं:


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

और यदि आपका viewset ऊपर वाले जितना सरल है, तो आप डिफ़ॉल्ट request और response bodies के साथ इसे एक अधिक स्वच्छ तरीके से परिभाषित करने के लिए `APIViewSet` class का लाभ उठा सकते हैं:
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

## ☔️ Scenario-Based Testing

Django Ninja CRUD [Django REST Testing](https://github.com/hbakri/django-rest-testing) के साथ seamlessly integrate होता है, और आपके CRUD endpoints की व्यापक coverage और मजबूत validation सुनिश्चित करता है।
शुरू में, testing framework इसी package का हिस्सा था, लेकिन बाद में इसे अधिक flexibility के लिए और Django Ninja के अलावा अन्य Django REST frameworks के साथ उपयोग किए जाने के लिए एक अलग package में निकाल दिया गया।

इस package के साथ, आप कर सकते हैं:
- **Test scenarios को declaratively परिभाषित करें**: प्रत्येक scenario के लिए अपेक्षित request और response details निर्दिष्ट करें, जिससे आपके tests self-documenting और समझने में आसान हो जाते हैं।
- **शर्तों की एक विस्तृत श्रृंखला का test करें**: valid और invalid input, non-existent resources, और custom business rules सहित विभिन्न शर्तों के तहत endpoint के व्यवहार को validate करें।
- **स्पष्टता और maintainability में सुधार करें**: tests को modular, प्रबंधनीय units में तोड़ें, code organization में सुधार करें और technical debt को कम करें।
- **व्यापक coverage सुनिश्चित करें**: scenario-based approach के कारण अपने endpoints का सख्ती से test करें, कोई case बिना test छोड़ें नहीं।

अपने tests में `ObjectDoesNotExist` जैसी exceptions को handle करने और उचित responses return करने के लिए, आप इस तरह एक exception handler परिभाषित कर सकते हैं:

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

अब, आप scenario-based testing framework का उपयोग करके अपने CRUD views के लिए tests लिख सकते हैं:

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

Django Ninja CRUD के declarative views को Django REST Testing की scenario-based testing capabilities के साथ combine करके, आप मजबूत, अच्छी तरह से test किए गए RESTful APIs को आसानी और विश्वास के साथ build और maintain कर सकते हैं।
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
