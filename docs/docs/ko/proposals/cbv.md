---
comments: true
---
# 클래스 기반 operations


!!! warning
    이것은 어디까지나 제안이며 **라이브러리 코드에는 포함되어 있지 않습니다**. 하지만 언젠가 Django Ninja의 일부가 될 수도 있습니다.

    이 제안에 대한 의견을 표현하기 위해 [github issue](https://github.com/vitalik/django-ninja/issues/15)에서 좋아요/싫어요 또는 댓글을 추가해 주시기 바랍니다.


## 문제점

API operation은 request와 파라미터를 받아 응답을 반환하는 호출 가능한 객체입니다. 하지만 실제 세계에서는 동일한 코드 조각을 여러 operation에서 재사용해야 하는 경우가 자주 발생합니다.
다음 예제를 살펴보겠습니다:

 - 프로젝트와 task가 있는 todo 애플리케이션이 있습니다
 - 각 프로젝트에는 여러 개의 task가 있습니다
 - 각 프로젝트에는 소유자(사용자)가 있을 수도 있습니다
 - 사용자는 자신이 소유하지 않은 프로젝트에 접근할 수 없어야 합니다

모델 구조는 대략 다음과 같습니다:

```python
class Project(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField()
```


이제 이를 위한 몇 가지 API operation을 만들어 보겠습니다:
- 프로젝트의 task 목록
- task 상세 정보
- "task 완료" operation

코드는 사용자가 자신의 프로젝트에 속한 task에만 접근할 수 있는지 검증해야 합니다 (그렇지 않으면 404 반환)

다음과 같이 작성할 수 있습니다:


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


보시다시피, 권한을 확인하기 위해 다음 줄들이 반복됩니다:

```python hl_lines="1 2"
user_projects = request.user.project_set
project = get_object_or_404(user_projects, id=project_id))
```

이를 함수로 추출할 수도 있지만, 그렇게 해도 겨우 3줄 줄어들 뿐 여전히 상당히 지저분할 것입니다...

## 해결책

이 제안은 `path` 데코레이터로 클래스 전체를 장식할 수 있는 "클래스 기반 operations"라는 대안을 도입하는 것입니다:

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

모든 공통 초기화와 권한 검사는 생성자에 들어갑니다:
```python hl_lines="4 5 6"
@router.path('/project/{project_id}/tasks')
class Tasks:
    def __init__(self, request, project_id=int):
        user_projects = request.user.project_set
        self.project = get_object_or_404(user_projects, id=project_id))
        self.tasks = self.project.task_set.all()
```

이렇게 하면 주요 비즈니스 operation은 task(`self.tasks` 속성으로 노출됨)에만 집중할 수 있습니다.

`api`와 `router` 인스턴스를 사용하여 클래스 경로를 지원할 수 있습니다.

## 문제점

`__init__` 메서드:

```def __init__(self, request, project_id=int):```

Python은 `__init__`에 대해 `async` 키워드를 지원하지 않으므로, async operation을 지원하려면 다른 초기화 방법이 필요합니다. 하지만 `__init__`이 가장 논리적으로 들립니다.


## 여러분의 생각/제안

이 제안에 대한 생각/좋아요/싫어요를 [github issue](https://github.com/vitalik/django-ninja/issues/15)에서 남겨 주세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
