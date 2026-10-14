---
comments: true
---
# クラスベースの操作


!!! warning
    これはあくまで提案であり、**ライブラリのコードには含まれていません**が、最終的には Django Ninja の一部になる可能性があります。

    この提案への感想を伝えるために、[github issue](https://github.com/vitalik/django-ninja/issues/15) で いいね/よくないね やコメントを追加することをご検討ください


## 問題点

API の操作（operation）は、リクエストとパラメータを受け取ってレスポンスを返す呼び出し可能なオブジェクトですが、実際の世界では、同じコードの断片を複数の操作で再利用する必要があることがよく起こります。
次の例を見てみましょう：

 - プロジェクトとタスクを持つ todo アプリケーションがあります
 - 各プロジェクトには複数のタスクがあります
 - 各プロジェクトにはオーナー（ユーザー）がいる場合もあります
 - ユーザーは自分が所有していないプロジェクトにアクセスできてはいけません

モデル構造はおおよそ次のとおりです：

```python
class Project(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField()
```


では、これに対していくつかの API 操作を作成してみましょう：
- あるプロジェクトのタスク一覧
- タスクの詳細
- 「タスクを完了する」操作

コードは、ユーザーが自分のプロジェクトに属するタスクにしかアクセスできないことを検証する必要があります（そうでなければ 404 を返します）。

コードは次のようになります：


```python
router = Router()

@router.get('/project/{project_id}/tasks/', response=List[TaskOut])
def task_list(request):
    user_projects = request.user.project_set
    project = get_object_or_404(user_projects, id=project_id))
    return project.task_set.all()

@router.get('/project/{project_id}/tasks/{task_id}/', response=TaskOut)
def details(request, task_id: int):
    user_projects = request.user.project_set
    project = get_object_or_404(user_projects, id=project_id))
    user_tasks = project.task_set.all()
    return get_object_or_404(user_tasks, id=task_id)


@router.post('/project/{project_id}/tasks/{task_id}/complete', response=TaskOut)
def complete(request, task_id: int):
    user_projects = request.user.project_set
    project = get_object_or_404(user_projects, id=project_id))
    user_tasks = project.task_set.all()
    task = get_object_or_404(user_tasks, id=task_id)
    task.completed = True
    task.save()
    return task
```


ご覧のとおり、パーミッションをチェックするために次の行が繰り返されています：

```python hl_lines="1 2"
user_projects = request.user.project_set
project = get_object_or_404(user_projects, id=project_id))
```

これを関数として切り出すこともできますが、それでも 3 行短くなるだけで、かなり散らかったままです...

## 解決策

この提案は、「クラスベースの操作」と呼ばれる代替手段を用意しようというものです。`path` デコレーターでクラス全体をデコレートできるようにします：

```python hl_lines="7 8"
from ninja import Router


router = Router()


@router.path('/project/{project_id}/tasks')
class Tasks:
    def __init__(self, request, project_id=int):
        user_projects = request.user.project_set
        self.project = get_object_or_404(user_projects, id=project_id))
        self.tasks = self.project.task_set.all()
    
    @router.get('/', response=List[TaskOut])
    def task_list(self, request):
        return self.tasks

    @router.get('/{task_id}/', response=TaskOut)
    def details(self, request, task_id: int):
        return get_object_or_404(self.tasks, id=task_id)

    @router.post('/{task_id}/complete', response=TaskOut)
    def complete(self, request, task_id: int):
        task = get_object_or_404(self.tasks, id=task_id)
        task.completed = True
        task.save()
        return task
```

共通の初期化処理とパーミッションチェックは、すべてコンストラクターに入ります：
```python hl_lines="4 5 6"
@router.path('/project/{project_id}/tasks')
class Tasks:
    def __init__(self, request, project_id=int):
        user_projects = request.user.project_set
        self.project = get_object_or_404(user_projects, id=project_id))
        self.tasks = self.project.task_set.all()
```

これにより、主要なビジネス操作はタスクだけに集中できます（`self.tasks` 属性として公開されます）

`api` と `router` のインスタンスを使って、クラスパスをサポートできます。

## 問題点

`__init__` メソッド：

```def __init__(self, request, project_id=int):```

Python は `__init__` に対する `async` キーワードをサポートしていないため、非同期操作をサポートするには別の初期化メソッドが必要になりますが、`__init__` が最も論理的に思えます。


## あなたの意見/提案

この提案についての意見や いいね/よくないね を [github issue](https://github.com/vitalik/django-ninja/issues/15) でお聞かせください。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
