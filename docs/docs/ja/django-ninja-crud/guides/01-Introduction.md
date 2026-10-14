---
comments: true
---
# はじめに
Django Ninja CRUD は、[Django Ninja](https://github.com/vitalik/django-ninja) を使った **CRUD**（[**C**reate、**R**ead、**U**pdate、**D**elete](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)）エンドポイントの開発を簡素化する、強力で [宣言的](https://en.wikipedia.org/wiki/Declarative_programming) ながらやや独断的なフレームワークであり、
さらに [Django REST Testing](https://github.com/hbakri/django-rest-testing) を使ってこれらの API エンドポイントをテストするための宣言的でシナリオベースのアプローチも提供します。

## 🍓 宣言的な CRUD ビューセットの再定義  

私たちのモデルビューセットとともに、Django CRUD 操作の未来へ踏み出しましょう。このフレームワークは、エンドポイントの作成を宣言的な視点で再構想し、複雑なプロセスを簡潔で読みやすいコードへと変換します。ベストプラクティスに基づいて構築されたモデルビューセットは、効率的で堅牢な設計の本質をカプセル化しています。モデルと schema を宣言的に指定するだけで、本格的な CRUD 操作を素早く生成でき、本当に重要な課題に取り組む自由が得られます。ここからが、web アプリケーション開発を再定義する旅の始まりです。
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
## 解決すべき課題
このフレームワークを使うと、よく使われるエンドポイントをクラスベースのビューとして定義し、プロジェクトの規約に合わせて簡単にカスタマイズできるほか、独自のカスタムビューを作成して提供された CRUD ビューと並べて宣言することも容易になり、モジュール性と拡張性が促進されます。
このパッケージは、プロジェクト全体で車輪の再発明を行うのではなく、**現実世界の問題を解決する**という最も重要なことに集中することを推奨しています。

もともと DRF の [ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset) に触発された
Django Ninja CRUD は、その限界を克服するために進化を遂げ、[合成は継承に勝る](https://en.wikipedia.org/wiki/Composition_over_inheritance)
（composition over inheritance）アプローチを採用して真のモジュール性を実現しました — これは、API エンドポイントを作成するためのより広範な宣言的アプローチに向けた基礎的な一歩です。

既存の継承ベースのビューセットが直面している課題：

- **モデルごとの CRUD エンドポイントの一意性**： Django Ninja CRUD では、同じモデルに対して複数のエンドポイントを定義でき、バージョニングや代替表現が可能です。    
- **カスタマイズの柔軟性の欠如**： モノリシックなクラスのメソッドをオーバーライドする代わりに、個々のビューを合成と設定を通じてカスタマイズできます。         
- **継承階層内の暗黙的な関係**： 合成によってビューが分離され、依存関係が減り、再利用性が向上します。       
- **新しいエンドポイントのモジュール性の欠如**： カスタムエンドポイントの追加に、ビューセット全体をサブクラス化する必要がなくなり、新機能を段階的に導入しやすくなります。      

## ✨ 主な特徴
- **純粋に宣言的**： どうやるかではなく、何が欲しいかを宣言することでビューとテストを定義します。
- **比類のないモジュール性**： 望む CRUD ビューでビューセットをカスタマイズし、各ビューの挙動をカスタマイズできます。
- **シナリオベースのテストフレームワーク**： シナリオベースのテストフレームワークを活用し、多様なテストケースを宣言的かつ簡潔に定義できます。
- **重要なことに集中**： 現実世界の問題を解決する時間を増やし、よくある繰り返し作業に費やす時間を減らせます。

> モデルビューセットのテストケースで正確にテストする

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

**Django Ninja CRUD は単なるツールではなく、Django web アプリケーションの開発とテストにおけるパラダイムシフトです。**



## 💬 次は何をしますか？


!!! success

    次の章の **[インストール方法](02-Installation.md)** に進みましょう。
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
