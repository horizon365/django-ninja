---
comments: true
---
# Операции на основе классов


!!! warning
    Это только предложение, **его нет в коде библиотеки**, но со временем оно может стать частью Django Ninja.

    Пожалуйста, поставьте лайк/дизлайк или оставьте комментарий в [github issue](https://github.com/vitalik/django-ninja/issues/15), чтобы выразить своё отношение к этому предложению


## Проблема

Операция API — это вызываемый объект, который принимает запрос и параметры и возвращает ответ, но на практике часто бывает, что один и тот же фрагмент кода нужно переиспользовать в нескольких операциях.
Рассмотрим следующий пример:

 - У нас есть todo-приложение с проектами и задачами
 - У каждого проекта несколько задач
 - У каждого проекта также может быть владелец (пользователь)
 - Пользователи не должны иметь доступ к чужим проектам

Структура моделей выглядит примерно так:

```python
class Project(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField()
```


Теперь создадим для этого несколько API-операций:
- список задач проекта
- детали некоторой задачи
- операцию «завершить задачу»

Код должен проверять, что пользователь может обращаться только к задачам из своих собственных проектов (иначе — вернуть 404)

Это может выглядеть так:


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


Как видите, эти строки повторяются для проверки прав доступа:

```python hl_lines="1 2"
user_projects = request.user.project_set
project = get_object_or_404(user_projects, id=project_id))
```

Можно вынести это в функцию, но это лишь сделает код на 3 строки короче, и он всё равно останется довольно громоздким...

## Решение

Предлагается альтернатива под названием «операции на основе классов» (class-based operations), где вы можете декорировать целый класс декоратором `path`:

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

Вся общая инициализация и проверки прав доступа выносятся в конструктор:
```python hl_lines="4 5 6"
@router.path('/project/{project_id}/tasks')
class Tasks:
    def __init__(self, request, project_id=int):
        user_projects = request.user.project_set
        self.project = get_object_or_404(user_projects, id=project_id))
        self.tasks = self.project.task_set.all()
```

Благодаря этому основные бизнес-операции сосредоточены только на задачах (доступных через атрибут `self.tasks`)

Вы можете использовать экземпляры `api` и `router` для поддержки классовых путей.

## Проблема

Метод `__init__`:

```def __init__(self, request, project_id=int):```

Python не поддерживает ключевое слово `async` для `__init__`, поэтому для поддержки асинхронных операций нам нужен другой метод инициализации, хотя `__init__` звучит наиболее логично.


## Ваши мысли/предложения

Пожалуйста, поделитесь своими мыслями, поставьте лайк или дизлайк этому предложению в [github issue](https://github.com/vitalik/django-ninja/issues/15).

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
