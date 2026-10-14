---
comments: true
---
# クイック例
## 🌞 仕組み

大学向けのシステムを構築していて、`Department` というモデルがあると想像してください。大学の各学部（department）には一意のタイトルが付いています。

```python
# examples/models.py
from django.db import models

class Department(models.Model):
    title = models.CharField(max_length=255, unique=True)
```

このデータを扱うには、Python オブジェクトと、JSON のような読み書きしやすい形式との間で双方向に変換する方法が必要です。Django Ninja では、これを実現するために「Schema」を使用します：

```python
# examples/schemas.py
from ninja import Schema

class DepartmentIn(Schema):
    title: str

class DepartmentOut(Schema):
    id: int
    title: str
```

`DepartmentIn` schema は、学部（department）を作成または更新する際に必要なデータを定義します。`DepartmentOut` schema は、学部を取得する際に提供するデータを定義します。

さて、ここからがこのパッケージの威力です。これを使えば、`Department` モデルに対する **CRUD** 操作をわずか数行のコードでセットアップできます：


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

そして、ビューセットが上記のようにシンプルであれば、`APIViewSet` クラスを活用して、デフォルトのリクエストボディとレスポンスボディを備えたより簡潔な形で定義できます：
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

## ☔️ シナリオベースのテスト

Django Ninja CRUD は [Django REST Testing](https://github.com/hbakri/django-rest-testing) とシームレスに統合されており、CRUD エンドポイントの包括的なカバレッジと堅牢なバリデーションを保証します。
当初、このテストフレームワークはこのパッケージの一部でしたが、後により柔軟性を持たせ、Django Ninja 以外の他の Django REST フレームワークでも使えるようにするため、独立したパッケージとして切り出されました。

このパッケージを使うと、次のことができます：
- **テストシナリオを宣言的に定義する**： 各シナリオに対して期待されるリクエストとレスポンスの詳細を指定し、テストを自己文書化され理解しやすいものにします。
- **幅広い条件をテストする**： 有効・無効な入力、存在しないリソース、カスタムビジネスルールを含む様々な条件下でのエンドポイントの挙動を検証します。
- **明瞭性と保守性を向上させる**： テストをモジュール化された管理しやすい単位に分割し、コードの整理を改善し技術的負債を削減します。
- **包括的なカバレッジを保証する**： シナリオベースのアプローチにより、エンドポイントを厳密にテストし、テストされていないケースを残しません。

テスト内で `ObjectDoesNotExist` のような例外を処理し適切なレスポンスを返すには、次のように例外ハンドラを定義できます：

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

これで、シナリオベースのテストフレームワークを使って CRUD ビューのテストを書くことができます：

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

Django Ninja CRUD の宣言的なビューと Django REST Testing のシナリオベースのテスト機能を組み合わせることで、堅牢でよくテストされた RESTful API を簡単に、自信を持って構築・保守できます。
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
