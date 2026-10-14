---
comments: true
---
# Opérations basées sur des classes


!!! warning
    Ceci n'est qu'une proposition et **ne fait pas partie du code de la bibliothèque**, mais elle pourrait à terme devenir une partie de Django Ninja.

    Pensez à ajouter un like/dislike ou un commentaire dans la [issue GitHub](https://github.com/vitalik/django-ninja/issues/15) pour exprimer votre opinion sur cette proposition


## Le problème

Une opération d'API est une fonction appelable qui accepte une requête et des paramètres et renvoie une réponse, mais dans le monde réel, il arrive souvent que le même morceau de code doive être réutilisé dans plusieurs opérations.
Regardons l'exemple suivant :

 - Nous avons une application de todo avec des projets et des tâches
 - Chaque projet comporte plusieurs tâches
 - Chaque projet peut également avoir un propriétaire (un utilisateur)
 - Les utilisateurs ne doivent pas pouvoir accéder aux projets dont ils ne sont pas propriétaires

La structure des modèles est à peu près la suivante :

```python
class Project(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField()
```


Créons maintenant quelques opérations d'API pour cela :
- la liste des tâches d'un projet
- le détail d'une tâche
- une opération « terminer une tâche »

Le code doit valider qu'un utilisateur ne peut accéder qu'aux tâches de ses propres projets (sinon, renvoyer 404)

Cela peut ressembler à ceci :


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


Comme vous pouvez le voir, ces lignes sont répétées pour vérifier les permissions :

```python hl_lines="1 2"
user_projects = request.user.project_set
project = get_object_or_404(user_projects, id=project_id))
```

Vous pouvez extraire cela dans une fonction, mais cela ne raccourcirait le code que de 3 lignes et il resterait quand même assez confus...

## La solution

La proposition consiste à avoir une alternative appelée « opérations basées sur des classes », où vous pouvez décorer une classe entière avec un décorateur `path` :

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

Toute l'initialisation commune et les vérifications de permissions vont dans le constructeur :
```python hl_lines="4 5 6"
@router.path('/project/{project_id}/tasks')
class Tasks:
    def __init__(self, request, project_id=int):
        user_projects = request.user.project_set
        self.project = get_object_or_404(user_projects, id=project_id))
        self.tasks = self.project.task_set.all()
```

Ainsi, les principales opérations métier se concentrent uniquement sur les tâches (exposées via l'attribut `self.tasks`)

Vous pouvez utiliser les instances `api` et `router` pour prendre en charge les chemins de classes.

## Le problème

La méthode `__init__` :

```def __init__(self, request, project_id=int):```

Python ne prend pas en charge le mot-clé `async` pour `__init__`, donc pour prendre en charge les opérations asynchrones, nous avons besoin d'une autre méthode d'initialisation, mais `__init__` est ce qui sonne le plus logique.


## Vos avis/propositions

Donnez votre avis/vos likes/dislikes sur cette proposition dans la [issue GitHub](https://github.com/vitalik/django-ninja/issues/15).

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
