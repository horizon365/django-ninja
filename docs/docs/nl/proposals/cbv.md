---
comments: true
---
# Class-based operations


!!! warning
    Dit is slechts een voorstel en **zit niet in de code van de bibliotheek**, maar uiteindelijk kan het onderdeel worden van Django Ninja.

    Overweeg om een like/dislike of opmerking toe te voegen in de [github issue](https://github.com/vitalik/django-ninja/issues/15) om je mening over dit voorstel te geven


## Het probleem

Een API-operatie is een aanroepbare functie die een request en parameters accepteert en een response teruggeeft, maar in de praktijk komt het vaak voor dat dezelfde code hergebruikt moet worden voor meerdere operaties.
Laten we het volgende voorbeeld bekijken:

 - We hebben een todo-applicatie met projecten en taken
 - Elk project heeft meerdere taken
 - Elk project kan ook een eigenaar hebben (een gebruiker)
 - Gebruikers mogen geen toegang hebben tot projecten die niet van hen zijn

De modelstructuur is grofweg als volgt:

```python
class Project(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField()
```


Laten we nu enkele API-operaties hiervoor maken:
- lijst met taken van een project
- details van een taak
- een "taak voltooien"-operatie

De code moet valideren dat een gebruiker alleen toegang heeft tot taken uit eigen projecten (anders, retourneer 404)

Het kan er zo uitzien:


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


Zoals je ziet worden deze regels herhaald om rechten te controleren:

```python hl_lines="1 2"
user_projects = request.user.project_set
project = get_object_or_404(user_projects, id=project_id))
```

Je kunt dit in een functie onderbrengen, maar dat maakt het slechts 3 regels korter en het blijft behoorlijk rommelig...

## De oplossing

Het voorstel is om een alternatief te hebben genaamd "class-based operations", waarbij je een hele klasse kunt decoreren met een `path`-decorator:

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

Alle gezamenlijke initialisatie en rechtencontroles gaan naar de constructor:
```python hl_lines="4 5 6"
@router.path('/project/{project_id}/tasks')
class Tasks:
    def __init__(self, request, project_id=int):
        user_projects = request.user.project_set
        self.project = get_object_or_404(user_projects, id=project_id))
        self.tasks = self.project.task_set.all()
```

Zo hoeven de belangrijkste bedrijfsoperaties zich alleen met de taken bezig te houden (beschikbaar gesteld als het attribuut `self.tasks`)

Je kunt de instanties `api` en `router` gebruiken om klasse-paden te ondersteunen.

## Het probleem

De `__init__`-methode:

```def __init__(self, request, project_id=int):```

Python ondersteunt het `async`-sleutelwoord niet voor `__init__`, dus om async-operaties te ondersteunen hebben we een andere initialisatiemethode nodig, maar `__init__` klinkt het meest logisch.


## Jouw gedachten/voorstellen

Geef je gedachten/likes/dislikes over dit voorstel in de [github issue](https://github.com/vitalik/django-ninja/issues/15).

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
