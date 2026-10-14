---
comments: true
---
# Einführung
Django Ninja CRUD ist ein leistungsfähiges, [deklaratives](https://en.wikipedia.org/wiki/Declarative_programming), dabei leicht meinungsstarkes Framework, das die Entwicklung von **CRUD**-Endpunkten ([**C**reate, **R**ead, **U**pdate, **D**elete](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)) mit [Django Ninja](https://github.com/vitalik/django-ninja) vereinfacht
und zusätzlich einen deklarativen, szenariobasierten Ansatz zum Testen dieser API-Endpunkte mit [Django REST Testing](https://github.com/hbakri/django-rest-testing) bereitstellt.

## 🍓 Die deklarativen CRUD-ViewSets neu definieren  

Treten Sie mit unseren Model-ViewSets in die Zukunft der Django-CRUD-Operationen ein. Unser Framework denkt die Erstellung von Endpunkten durch eine deklarative Brille neu, verwandelt komplexe Prozesse in prägnanten, lesbaren Code. Es baut auf Best Practices auf, und die Model-ViewSets kapseln die Essenz eines effizienten und robusten Designs ein. Indem Sie Modell und Schemas deklarativ angeben, können Sie schnell vollwertige CRUD-Operationen erzeugen, die Sie freisetzen, um sich den Herausforderungen zu widmen, die wirklich zählen. Hier beginnt die Reise, die Entwicklung von Webanwendungen neu zu definieren.
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
## Das zu lösende Problem
Es erlaubt Ihnen, häufige Endpunkte als klassenbasierte Views zu definieren und sie leicht an die Konventionen Ihres Projekts anzupassen, sowie einfach eigene benutzerdefinierte Views zu erstellen und sie neben den bereitgestellten CRUD-Views zu deklarieren, was Modularität und Erweiterbarkeit fördert.
Dieses Paket ermutigt dazu, sich auf das Wesentlichste zu konzentrieren: **echte Probleme zu lösen**, statt im gesamten Projekt das Rad neu zu erfinden.

Ursprünglich inspiriert von DRFs [ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset),
wurde Django Ninja CRUD weiterentwickelt, um dessen Limitierungen zu beheben, und verfolgt einen [Composition over Inheritance](https://en.wikipedia.org/wiki/Composition_over_inheritance)-Ansatz,
um echte Modularität zu erreichen — ein grundlegender Schritt hin zu einem breiteren deklarativen Ansatz zur Erstellung von API-Endpunkten.

Herausforderungen bestehender auf Vererbung basierender ViewSets:

- **Eindeutigkeit der CRUD-Endpunkte pro Modell**: Django Ninja CRUD erlaubt es, mehrere Endpunkte für dasselbe Modell zu definieren, was Versionierung oder alternative Darstellungen ermöglicht.    
- **Mangelnde Anpassungsflexibilität**: statt Methoden auf einer monolithischen Klasse zu überschreiben, können einzelne Views durch Komposition und Konfiguration angepasst werden.         
- **Implizite Beziehungen innerhalb von Vererbungshierarchien**: Komposition entkoppelt Views, reduziert Abhängigkeiten und verbessert die Wiederverwendbarkeit.       
- **Mangelnde Modularität für neue Endpunkte**: das Hinzufügen benutzerdefinierter Endpunkte erfordert keine Unterklasse des gesamten ViewSets mehr, was es erleichtert, neue Funktionen schrittweise einzuführen.      

## ✨ Hauptmerkmale
- **Rein deklarativ**: definieren Sie Views und Tests, indem Sie deklarieren, was Sie wollen, nicht wie es zu tun ist.
- **Unschlagbare Modularität**: passen Sie Ihre ViewSets mit den gewünschten CRUD-Views an und konfigurieren Sie das Verhalten jedes einzelnen Views.
- **Szenariobasiertes Testframework**: nutzen Sie das szenariobasierte Testframework, um vielfältige Testfälle deklarativ und prägnant zu definieren.
- **Fokus auf das Wesentliche**: verbringen Sie mehr Zeit mit der Lösung echter Probleme und weniger mit häufigen, sich wiederholenden Aufgaben.

> Testen Sie präzise mit Testfällen für Model-ViewSets

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

**Django Ninja CRUD ist mehr als ein Werkzeug; es ist ein Paradigmenwechsel in der Entwicklung und dem Testen von Django-Webanwendungen.**



## 💬 Wie geht es weiter?


!!! success

    Fahren Sie mit dem nächsten Kapitel fort: **[Installation](02-Installation.md)**.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
