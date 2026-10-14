---
comments: true
---
# Introduction
Django Ninja CRUD est un framework puissant, [déclaratif](https://en.wikipedia.org/wiki/Declarative_programming), mais légèrement opinionné, qui simplifie le développement d'endpoints **CRUD** ([**C**reate, **R**ead, **U**pdate, **D**elete](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)) avec [Django Ninja](https://github.com/vitalik/django-ninja),
et fournit également une approche déclarative et basée sur des scénarios pour tester ces endpoints d'API à l'aide de [Django REST Testing](https://github.com/hbakri/django-rest-testing).

## 🍓 Redéfinir les Viewsets CRUD déclaratifs  

Entrez dans le futur des opérations CRUD Django avec nos model viewsets. Notre framework réinvente la création d'endpoints sous un angle déclaratif, transformant des processus complexes en code concis et lisible. Construits sur les meilleures pratiques, les model viewsets encapsulent l'essence d'une conception efficace et robuste. En spécifiant déclarativement le modèle et les schémas, vous pouvez rapidement générer des opérations CRUD complètes, vous libérant pour relever les défis qui comptent vraiment. C'est ici que commence le voyage de la redéfinition du développement d'applications web.
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
## Le problème à résoudre
Il vous permet de définir des endpoints courants sous forme de vues basées sur des classes et de les personnaliser facilement pour les adapter aux conventions de votre projet, ainsi que de créer facilement vos propres vues personnalisées et de les déclarer aux côtés des vues CRUD fournies, favorisant ainsi la modularité et l'extensibilité.
Ce paquet encourage à se concentrer sur ce qui compte le plus : **résoudre des problèmes concrets**, plutôt que de réinventer la roue tout au long de votre projet.

Initialement inspiré du [ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset) de DRF,
Django Ninja CRUD a évolué pour remédier à ses limites, adoptant une approche de [composition plutôt qu'héritage](https://en.wikipedia.org/wiki/Composition_over_inheritance)
pour atteindre une véritable modularité — une étape fondamentale vers une approche déclarative plus large de la création d'endpoints d'API.

Défis rencontrés par les viewsets existants basés sur l'héritage :

- **Unicité des endpoints CRUD par modèle** : Django Ninja CRUD vous permet de définir plusieurs endpoints pour le même modèle, permettant le versionnage ou des représentations alternatives.    
- **Manque de flexibilité de personnalisation** : au lieu de surcharger des méthodes sur une classe monolithique, des vues individuelles peuvent être personnalisées par composition et configuration.         
- **Relations implicites dans les hiérarchies d'héritage** : la composition découple les vues, réduisant les dépendances et améliorant la réutilisabilité.       
- **Manque de modularité pour les nouveaux endpoints** : l'ajout d'endpoints personnalisés ne nécessite plus de créer une sous-classe de l'ensemble du viewset, ce qui facilite l'introduction incrémentale de nouvelles fonctionnalités.      

## ✨ Fonctionnalités clés
- **Purement déclaratif** : définissez des vues et des tests en déclarant ce que vous voulez, plutôt que comment le faire.
- **Modularité inégalée** : personnalisez vos viewsets avec les vues CRUD souhaitées, en personnalisant le comportement de chaque vue.
- **Framework de test basé sur des scénarios** : exploitez le framework de test basé sur des scénarios pour définir de manière déclarative et concise divers cas de test.
- **Concentrez-vous sur l'essentiel** : passez plus de temps à résoudre des problèmes concrets et moins sur les tâches courantes et répétitives.

> Testez avec précision grâce aux cas de test de model viewset

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

**Django Ninja CRUD est plus qu'un outil ; c'est un changement de paradigme dans le développement et le test d'applications web Django.**



## 💬 Et ensuite ?


!!! success

    Poursuivez avec le chapitre suivant **[Comment installer](02-Installation.md)**.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
