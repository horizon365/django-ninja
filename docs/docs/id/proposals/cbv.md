---
comments: true
---
# Operasi berbasis class (class-based operations)


!!! warning
    Ini hanyalah sebuah proposal dan **belum ada di kode library**, tetapi pada akhirnya hal ini mungkin menjadi bagian dari Django Ninja.

    Silakan pertimbangkan untuk menambahkan like/dislike atau komentar di [github issue](https://github.com/vitalik/django-ninja/issues/15) untuk menyatakan pendapat Anda tentang proposal ini


## Masalahnya

Sebuah operasi API adalah callable yang menerima request dan parameter, lalu mengembalikan sebuah response, tetapi di dunia nyata, sering terjadi bahwa potongan kode yang sama perlu digunakan kembali di beberapa operasi.
Mari kita lihat contoh berikut:

 - Kita memiliki aplikasi todo dengan projects dan tasks
 - Setiap project memiliki banyak task
 - Setiap project juga dapat memiliki seorang owner (seorang user)
 - User tidak boleh dapat mengakses project yang bukan miliknya

Struktur model kurang lebih seperti ini:

```python
class Project(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField()
```


Sekarang, mari kita buat beberapa operasi API untuk ini:
- daftar task dari sebuah project
- beberapa detail task
- operasi "menyelesaikan task"

Kode tersebut harus memvalidasi bahwa seorang user hanya dapat mengakses task dari project miliknya sendiri (jika tidak, kembalikan 404)

Tampilannya bisa seperti ini:


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


Seperti yang Anda lihat, baris-baris ini berulang untuk memeriksa permission:

```python hl_lines="1 2"
user_projects = request.user.project_set
project = get_object_or_404(user_projects, id=project_id))
```

Anda bisa mengekstraknya menjadi sebuah fungsi, tetapi itu hanya akan mempersingkat 3 baris dan hasilnya tetap cukup berantakan...

## Solusinya

Proposalnya adalah menghadirkan alternatif yang disebut "class-based operations", di mana Anda dapat mendekorasi sebuah class utuh dengan decorator `path`:

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

Semua inisialisasi umum dan pemeriksaan permission dimasukkan ke dalam constructor:
```python hl_lines="4 5 6"
@router.path('/project/{project_id}/tasks')
class Tasks:
    def __init__(self, request, project_id=int):
        user_projects = request.user.project_set
        self.project = get_object_or_404(user_projects, id=project_id))
        self.tasks = self.project.task_set.all()
```

Ini membuat operasi bisnis utama hanya berfokus pada task (yang diekspos sebagai atribut `self.tasks`)

Anda dapat menggunakan instance `api` dan `router` untuk mendukung class path.

## Masalahnya

Method `__init__`:

```def __init__(self, request, project_id=int):```

Python tidak mendukung keyword `async` untuk `__init__`, jadi untuk mendukung operasi async kita memerlukan method inisialisasi lain, tetapi `__init__` terdengar paling logis.


## Pikiran/proposal Anda

Silakan sampaikan pikiran/like/dislike Anda tentang proposal ini di [github issue](https://github.com/vitalik/django-ninja/issues/15).

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
