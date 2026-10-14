---
comments: true
---
# Class-based operations


!!! warning
    यह केवल एक proposal है और **library code में नहीं है**, लेकिन आखिरकार यह Django Ninja का हिस्सा बन सकता है।

    कृपया इस proposal के बारे में अपनी राय व्यक्त करने के लिए [github issue](https://github.com/vitalik/django-ninja/issues/15) में like/dislike या comment जोड़ने पर विचार करें


## समस्या

एक API operation एक ऐसा callable होता है जो request और parameters accept करता है और एक response return करता है, लेकिन वास्तविक दुनिया में अक्सर ऐसा होता है कि एक ही code को कई operations में दोबारा इस्तेमाल (reuse) करने की ज़रूरत पड़ती है।
आइए निम्नलिखित उदाहरण देखें:

 - हमारे पास projects और tasks वाला एक todo application है
 - हर project में कई tasks होते हैं
 - हर project का एक owner (एक user) भी हो सकता है
 - Users उन projects को access नहीं कर पाएँ जिनके वे owner नहीं हैं

Model की structure लगभग ऐसी है:

```python
class Project(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField()
```


अब, इसके लिए कुछ API operations बनाते हैं:
- किसी project के tasks की list
- किसी task की details
- एक "complete task" operation

Code को यह validate करना चाहिए कि user केवल अपने ही projects के tasks को access कर सके (अन्यथा, 404 return करें)

यह ऐसा दिख सकता है:


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


जैसा कि आप देख सकते हैं, permissions की जाँच के लिए ये lines दोहराई जाती हैं:

```python hl_lines="1 2"
user_projects = request.user.project_set
project = get_object_or_404(user_projects, id=project_id))
```

आप इसे एक function में निकाल सकते हैं, लेकिन इससे बस 3 lines छोटा होगा और फिर भी यह काफ़ी गड़बड़ लगेगा...

## समाधान

Proposal यह है कि एक वैकल्पिक तरीका "class-based operations" नाम से उपलब्ध हो, जिसमें आप पूरी class को एक `path` decorator से decorate कर सकें:

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

सभी common initialization और permission checks constructor में चले जाते हैं:
```python hl_lines="4 5 6"
@router.path('/project/{project_id}/tasks')
class Tasks:
    def __init__(self, request, project_id=int):
        user_projects = request.user.project_set
        self.project = get_object_or_404(user_projects, id=project_id))
        self.tasks = self.project.task_set.all()
```

इससे मुख्य business operations केवल tasks पर ध्यान केंद्रित करते हैं (जिन्हें `self.tasks` attribute के रूप में expose किया जाता है)

आप class paths को support करने के लिए `api` और `router` instances का इस्तेमाल कर सकते हैं।

## समस्या

`__init__` method:

```def __init__(self, request, project_id=int):```

Python, `__init__` के लिए `async` keyword को support नहीं करता, इसलिए async operations को support देने के लिए हमें एक और initialization method चाहिए, लेकिन `__init__` सबसे तर्कसंगत (logical) लगता है।


## आपके विचार/proposals

कृपया इस proposal के बारे में अपने विचार/likes/dislikes [github issue](https://github.com/vitalik/django-ninja/issues/15) में दें।

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
