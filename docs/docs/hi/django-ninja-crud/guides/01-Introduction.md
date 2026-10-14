---
comments: true
---
# परिचय
Django Ninja CRUD एक शक्तिशाली, [declarative](https://en.wikipedia.org/wiki/Declarative_programming), लेकिन थोड़ा opinionated framework है जो [Django Ninja](https://github.com/vitalik/django-ninja) के साथ **CRUD** ([**C**reate, **R**ead, **U**pdate, **D**elete](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)) endpoints के development को सरल बनाता है,
और साथ ही [Django REST Testing](https://github.com/hbakri/django-rest-testing) का उपयोग करके इन API endpoints को test करने के लिए एक declarative, scenario-based approach भी प्रदान करता है।

## 🍓 Declarative CRUD Viewsets को पुनः परिभाषित करना  

हमारे model viewsets के साथ Django CRUD operations के भविष्य में कदम रखें। हमारा framework endpoint creation को एक declarative lens के माध्यम से पुनः कल्पित करता है, जटिल processes को संक्षिप्त, पठनीय कोड में बदल देता है। सर्वोत्तम practices पर built, model viewsets कुशल और मजबूत डिज़ाइन का सार समाहित करते हैं। Model और schemas को declaratively निर्दिष्ट करके, आप पूर्ण CRUD operations तेजी से generate कर सकते हैं, जिससे आप उन चुनौतियों पर ध्यान केंद्रित कर सकते हैं जो वास्तव में मायने रखती हैं। Web application development को पुनः परिभाषित करने की यात्रा यहीं से शुरू होती है।
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
## हल करने की समस्या
यह आपको common endpoints को class-based views के रूप में परिभाषित करने और उन्हें आसानी से अपनी project की conventions के अनुरूप customize करने की अनुमति देता है, और अपने स्वयं के custom views आसानी से बनाने तथा उन्हें प्रदान किए गए CRUD views के साथ declare करने की सुविधा भी देता है, जिससे modularity और extensibility को बढ़ावा मिलता है।
यह package इस पर ध्यान केंद्रित करने के लिए प्रोत्साहित करता है जो सबसे महत्वपूर्ण है: **वास्तविक दुनिया की समस्याओं को हल करना**, न कि अपने project में बार-बार पहिया (wheel) दोबारा आविष्कार करना।

मूल रूप से DRF के [ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset) से प्रेरित,
Django Ninja CRUD अपनी सीमाओं को दूर करने के लिए विकसित हुआ, true modularity प्राप्त करने के लिए [composition over inheritance](https://en.wikipedia.org/wiki/Composition_over_inheritance) approach अपनाया — जो API endpoints बनाने के लिए एक व्यापक declarative approach की ओर एक आधारभूत कदम है।

मौजूदा inheritance-based viewsets की चुनौतियाँ:

- **प्रति model CRUD endpoints की विशिष्टता**: Django Ninja CRUD आपको एक ही model के लिए कई endpoints परिभाषित करने की अनुमति देता है, जिससे versioning या alternative representations संभव होती हैं।    
- **Customization flexibility की कमी**: एक monolithic class पर methods को override करने के बजाय, अलग-अलग views को composition और configuration के माध्यम से customize किया जा सकता है।         
- **Inheritance hierarchies के भीतर अंतर्निहित संबंध**: composition views को decouple करता है, dependencies को कम करता है और reusability को बेहतर बनाता है।       
- **नए endpoints के लिए modularity की कमी**: custom endpoints जोड़ने के लिए अब पूरे viewset को subclass करने की आवश्यकता नहीं है, जिससे नई features को incrementally पेश करना आसान हो जाता है।      

## ✨ मुख्य Features
- **पूर्णतः declarative**: views और tests को यह declare करके परिभाषित करें कि आप क्या चाहते हैं, न कि यह कैसे करना है।
- **अद्वितीय modularity**: अपने viewsets को वांछित CRUD views के साथ customize करें, प्रत्येक view के व्यवहार को customize करते हुए।
- **Scenario-based testing framework**: विविध test cases को declaratively और संक्षेप में परिभाषित करने के लिए scenario-based testing framework का लाभ उठाएँ।
- **मायने रखने वाली चीज़ों पर ध्यान दें**: वास्तविक दुनिया की समस्याओं को हल करने में अधिक समय बिताएँ और common, दोहराव वाले कार्यों पर कम।

> Model viewset test cases के साथ सटीक test करें

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

**Django Ninja CRUD केवल एक tool नहीं है; यह Django web application development और testing में एक paradigm shift है।**



## 💬 आगे क्या?


!!! success

    अगले अध्याय **[इंस्टॉल कैसे करें](02-Installation.md)** पर जारी रखें।
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
