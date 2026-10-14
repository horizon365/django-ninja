---
comments: true
---
# Introductie
Django Ninja CRUD is een krachtig, [declaratief](https://en.wikipedia.org/wiki/Declarative_programming) en lichtelijk opiniegedreven framework dat de ontwikkeling van **CRUD**-endpoints ([**C**reate, **R**ead, **U**pdate, **D**elete](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)) met [Django Ninja](https://github.com/vitalik/django-ninja) vereenvoudigt,
en ook een declaratieve, op scenario's gebaseerde aanpak biedt voor het testen van deze API-endpoints met [Django REST Testing](https://github.com/hbakri/django-rest-testing).

## 🍓 Declaratieve CRUD-viewsets herdefiniëren  

Betreed de toekomst van Django CRUD-bewerkingen met onze model-viewsets. Ons framework herinterpretert het creëren van endpoints door een declaratieve bril, en transformeert complexe processen in beknopte, leesbare code. Gebouwd op best practices, vatten de model-viewsets de essentie van efficiënt en robuust ontwerp samen. Door declaratief het model en de schema's op te geven, kun je snel volwaardige CRUD-bewerkingen genereren, zodat je je kunt richten op de uitdagingen die er echt toe doen. Hier begint de reis van het herdefiniëren van webapplicatieontwikkeling.
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
## Het op te lossen probleem
Het stelt je in staat om veelvoorkomende endpoints te definiëren als class-based views en ze eenvoudig aan te passen aan de conventies van je project, en om eenvoudig je eigen aangepaste views te maken en deze naast de meegeleverde CRUD-views te declareren, wat modulariteit en uitbreidbaarheid bevordert.
Dit pakket moedigt aan om je te richten op wat het belangrijkst is: **echte problemen oplossen**, in plaats van het wiel opnieuw uit te vinden in je project.

Oorspronkelijk geïnspireerd door DRF's [ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset),
evolueerde Django Ninja CRUD om de beperkingen ervan aan te pakken, met een aanpak van [compositie boven overerving](https://en.wikipedia.org/wiki/Composition_over_inheritance)
om echte modulariteit te bereiken — een fundamentele stap richting een bredere declaratieve aanpak voor het creëren van API-endpoints.

Uitdagingen van bestaande op overerving gebaseerde viewsets:

- **Uniekheid van CRUD-endpoints per model**: Django Ninja CRUD stelt je in staat om meerdere endpoints voor hetzelfde model te definiëren, wat versionering of alternatieve representaties mogelijk maakt.    
- **Gebrek aan aanpassingsflexibiliteit**: in plaats van methoden te overschrijven op een monolithische klasse, kunnen individuele views worden aangepast via compositie en configuratie.         
- **Impliciete relaties binnen overervingshiërarchieën**: compositie ontkoppelt views, vermindert afhankelijkheden en verbetert hergebruik.       
- **Gebrek aan modulariteit voor nieuwe endpoints**: het toevoegen van aangepaste endpoints vereist niet langer het subclassen van de gehele viewset, waardoor het gemakkelijker wordt om stap voor stap nieuwe functies te introduceren.      

## ✨ Belangrijkste functies
- **Puur declaratief**: definieer views en tests door te declareren wat je wilt, in plaats van hoe het moet.
- **Ongeëvenaarde modulariteit**: stel je viewsets samen met de gewenste CRUD-views en pas het gedrag van elke view aan.
- **Op scenario's gebaseerd testframework**: gebruik het op scenario's gebaseerde testframework om op declaratieve en beknopte wijze uiteenlopende testcases te definiëren.
- **Focus op wat er toe doet**: besteed meer tijd aan het oplossen van echte problemen en minder aan veelvoorkomende, repetitieve taken.

> Test nauwkeurig met testcases voor model-viewsets

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

**Django Ninja CRUD is meer dan een tool; het is een paradigmaverschuiving in de ontwikkeling en het testen van Django-webapplicaties.**



## 💬 Wat nu?


!!! success

    Ga verder naar het volgende hoofdstuk **[Hoe te installeren](02-Installation.md)**.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
