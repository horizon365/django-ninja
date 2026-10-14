---
comments: true
---
# Klassenbasierte Operationen


!!! warning
    Dies ist nur ein Vorschlag und **befindet sich nicht im Bibliothekscode**, aber möglicherweise wird er eventually Teil von Django Ninja.

    Bitte erwägen Sie, ein Like/Dislike oder einen Kommentar im [GitHub-Issue](https://github.com/vitalik/django-ninja/issues/15) hinzuzufügen, um Ihre Meinung zu diesem Vorschlag auszudrücken


## Das Problem

Eine API-Operation ist ein Callable, das eine Anfrage und Parameter entgegennimmt und eine Response zurückgibt, aber in der Praxis kommt es häufig vor, dass derselbe Codeabschnitt über mehrere Operationen hinweg wiederverwendet werden muss.
Sehen wir uns das folgende Beispiel an:

 - Wir haben eine Todo-Anwendung mit Projekten und Aufgaben
 - Jedes Projekt hat mehrere Aufgaben
 - Jedes Projekt kann außerdem einen Eigentümer haben (einen Benutzer)
 - Benutzer sollten nicht auf Projekte zugreifen können, die ihnen nicht gehören

Die Modellstruktur sieht ungefähr so aus:

```python
class Project(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField()
```


Erstellen wir nun einige API-Operationen dafür:
- Liste der Aufgaben eines Projekts
- Details zu einer Aufgabe
- eine Operation „Aufgabe abschließen"

Der Code soll validieren, dass ein Benutzer nur auf Aufgaben aus seinen eigenen Projekten zugreifen kann (andernfalls 404 zurückgeben)

Das könnte so aussehen:


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


Wie Sie sehen, werden diese Zeilen zur Berechtigungsprüfung wiederholt:

```python hl_lines="1 2"
user_projects = request.user.project_set
project = get_object_or_404(user_projects, id=project_id))
```

Sie können dies in eine Funktion auslagern, aber das würde den Code nur um 3 Zeilen kürzen und er wäre weiterhin ziemlich unübersichtlich...

## Die Lösung

Der Vorschlag ist eine Alternative namens „klassenbasierte Operationen", bei der Sie eine ganze Klasse mit einem `path`-Decorator dekorieren können:

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

Die gesamte gemeinsame Initialisierung und die Berechtigungsprüfungen kommen in den Konstruktor:
```python hl_lines="4 5 6"
@router.path('/project/{project_id}/tasks')
class Tasks:
    def __init__(self, request, project_id=int):
        user_projects = request.user.project_set
        self.project = get_object_or_404(user_projects, id=project_id))
        self.tasks = self.project.task_set.all()
```

Dadurch können sich die eigentlichen Geschäftsoperationen nur auf die Aufgaben konzentrieren (verfügbar als Attribut `self.tasks`)

Sie können die Instanzen `api` und `router` verwenden, um Klassenpfade zu unterstützen.

## Das Problem

Die Methode `__init__`:

```def __init__(self, request, project_id=int):```

Python unterstützt das Schlüsselwort `async` für `__init__` nicht, daher brauchen wir zur Unterstützung asynchroner Operationen eine weitere Initialisierungsmethode, aber `__init__` klingt am logischsten.


## Ihre Gedanken/Vorschläge

Bitte äußern Sie Ihre Gedanken/Likes/Dislikes zu diesem Vorschlag im [GitHub-Issue](https://github.com/vitalik/django-ninja/issues/15).

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
