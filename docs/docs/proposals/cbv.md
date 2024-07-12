---
comments: true
---
# 基于类的操作


!!! 警告
    这只是一个提议，且 **不在库代码中**， 但最终它可能会成为 Django Ninja 的一部分。

    请考虑在 [github issue](https://github.com/vitalik/django-ninja/issues/15) 中添加喜欢/不喜欢或评论来表达你对这个提议的感受


## 问题

一个 API 操作是一个可调用对象，它接受请求和参数并返回响应，但在现实世界中，经常会出现需要在多个操作中重用相同代码片段的情况。
让我们看下面这个例子：

 - 我们有一个待办事项应用程序，包含项目和任务
 - 每个项目有多个任务
 - 每个项目可能也有一个所有者（用户）
 - 用户不应能访问他们不拥有的项目

模型结构大概是这样的：

```python
class Project(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField()
```


现在，让我们为此创建一些 API 操作：
- 项目的任务列表
- 一些任务详情
- 一个“完成任务”操作

代码应该验证用户只能访问他/她自己项目的任务（否则，返回 404）

它可以是这样的：


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


如你所见，这些行经常重复出现以检查权限：

```python hl_lines="1 2"
user_projects = request.user.project_set
project = get_object_or_404(user_projects, id=project_id))
```

你可以将其提取到一个函数中，但这只会使其减少 3 行，并且仍然会相当混乱...

## 解决方案

提议是有一个替代方案称为“基于类的操作”，你可以用一个 `path` 装饰器来装饰整个类：

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

所有常见的初始化和权限检查都放在构造函数中：
```python hl_lines="4 5 6"
@router.path('/project/{project_id}/tasks')
class Tasks:
    def __init__(self, request, project_id=int):
        user_projects = request.user.project_set
        self.project = get_object_or_404(user_projects, id=project_id))
        self.tasks = self.project.task_set.all()
```

这使得主要业务操作仅关注任务 (作为 `self.tasks` 属性暴露)

你可以使用 `api` and `router` 实例来支持类路径。

## 问题

`__init__` 方法:

```def __init__(self, request, project_id=int):```

Python 不支持把 `async` 关键字用于 `__init__`, 所以为了支持异步操作，我们需要其他初始化方法，但 `__init__` 听起来最符合逻辑。


## 你的想法/提议

请在 [github 问题](https://github.com/vitalik/django-ninja/issues/15) 中给出你对这个提议的想法/喜欢/不喜欢。

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
