---
comments: true
---
# Class-based operations


!!! warning
    This is only a proposal and **is not in the library code**, but eventually it may become part of Django Ninja.

    Please consider adding a like/dislike or comment in the [github issue](https://github.com/vitalik/django-ninja/issues/15) to express your feelings about this proposal


## The problem

An API operation is a callable that accepts a request and parameters and returns a response, but in the real world, it often happens that the same piece of code needs to be reused across multiple operations.
Let's look at the following example:

 - We have a todo application with projects and tasks
 - Each project has multiple tasks
 - Each project may also have an owner (a user)
 - Users should not be able to access projects they do not own

The model structure is roughly this:

```python
class Project(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField()
```


Now, let's create some API operations for this:
- list of tasks of a project
- some task details
- a "complete task" operation

The code should validate that a user can only access tasks from their own projects (otherwise, return 404)

It can look like this:


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


As you can see, these lines are repeated to check permissions:

```python hl_lines="1 2"
user_projects = request.user.project_set
project = get_object_or_404(user_projects, id=project_id))
```

You can extract this into a function, but that would only make it 3 lines shorter and it would still be quite messy...

## The solution

The proposal is to have an alternative called "class-based operations", where you can decorate a whole class with a `path` decorator:

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

All the common initialization and permission checks go into the constructor:
```python hl_lines="4 5 6"
@router.path('/project/{project_id}/tasks')
class Tasks:
    def __init__(self, request, project_id=int):
        user_projects = request.user.project_set
        self.project = get_object_or_404(user_projects, id=project_id))
        self.tasks = self.project.task_set.all()
```

This makes the main business operations focus only on the tasks (exposed as the `self.tasks` attribute)

You can use the `api` and `router` instances to support class paths.

## The problem

The `__init__` method:

```def __init__(self, request, project_id=int):```

Python does not support the `async` keyword for `__init__`, so to support async operations we need another initialization method, but `__init__` sounds the most logical.


## Your thoughts/proposals

Please give your thoughts/likes/dislikes about this proposal in the [github issue](https://github.com/vitalik/django-ninja/issues/15).

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
