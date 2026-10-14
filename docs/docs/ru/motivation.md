---
comments: true
---
# Мотивация

!!! note
    **Django Ninja** выглядит практически так же, как **FastAPI**, так почему бы просто не использовать FastAPI?

Действительно, **Django Ninja** был в значительной степени вдохновлён <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a> (разработанным <a href="https://github.com/tiangolo" target="_blank">Себастьяном Рамиресом</a>)

Тем не менее, при совместном использовании FastAPI и Django возникает ряд проблем:

1) **FastAPI** заявляет, что он ORM-агностичен (то есть его можно использовать с SQLAlchemy или Django ORM), но на практике Django ORM пока не готов к асинхронному использованию (вероятно, в версии 4.0 или 4.1). Если использовать его в синхронном режиме, вы можете столкнуться с [проблемами закрытия соединений](https://github.com/tiangolo/fastapi/issues/716), и потребуется **очень много** усилий, чтобы их преодолеть.

2) Когда вы полагаетесь на аутентификацию и сессии базы данных в своих операциях (для некоторых проектов это около 99% всех операций), внедрение зависимостей через параметры делает код чрезмерно многословным.

```python hl_lines="25 26"
...

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode(token)
    if not user:
        raise HTTPException(...)
    return user


@app.get("/task/{task_id}", response_model=Task)
def read_user(
        task_id: int,
        db: Session = Depends(get_db), 
        current_user: User = Depends(get_current_user),
    ):
        ... use db with current_user ....
```

3) Поскольку слово `model` «зарезервировано» в Django для нужд ORM, всё становится очень запутанным, когда вы смешиваете соглашения об именовании моделей Django ORM и Pydantic/FastAPI.

### Django Ninja

Django Ninja решает все эти проблемы и очень хорошо интегрируется с Django (ORM, URL-ы, view-функции, аутентификация и т.д.).
Работая в [Code-on, студии веб-дизайна и разработки на Django](https://code-on.be/), я столкнулся с самыми разными трудностями, и для их решения в 2020 году начал проект Django-Ninja.

Примечание: **Django Ninja — это проект, готовый к продакшену** — я оцениваю, что на данный момент более 100 компаний используют его в продакшене, и каждую месяц к ним присоединяются 500 новых разработчиков.

Некоторые компании уже ищут разработчиков с опытом работы в Django Ninja.

#### Основные возможности

1) Поскольку у вас может быть несколько экземпляров Django Ninja API, вы можете запускать [несколько версий API](guides/versioning.md) в одном Django-проекте.

```python
api_v1 = NinjaAPI(version='1.0', auth=token_auth)
...
api_v2 = NinjaAPI(version='2.0', auth=token_auth)
...
api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')
...


urlpatterns = [
    ...
    path('api/v1/', api_v1.urls),
    path('api/v2/', api_v2.urls),
    path('internal-api/', api_private.urls),
]
```

2) Класс 'Schema' в Django Ninja интегрируется с ORM, поэтому вы можете [сериализовать querysets](guides/response/index.md#returning-querysets) или ORM-объекты:

```python
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()


@api.get("/tasks", response=TaskSchema)
def tasks_details(request):
    task = Task.objects.first()
    return task
```
3) [Создание Schema из Django-модели](guides/response/django-pydantic.md).

4) Вместо параметров зависимостей **Django Ninja** использует свойства экземпляра `request` (так же, как обычные Django view-функции) — подробнее см. [Аутентификацию](guides/authentication.md).

!!! note

    Ознакомьтесь с **[Учебником](tutorial/index.md)**, чтобы быстро начать.

    Экосистема вокруг Django Ninja:

    1. [django-ninja-crud](django-ninja-crud/index.md): Фреймворк, построенный на django-ninja для упрощения разработки CRUD-интерфейсов, предоставляющий декларативные viewsets для моделей и сценарные методы тестирования.

    2. [django-ninja-extra](django-ninja-extra/index.md): Инструмент, позволяющий разработчикам пропустить громоздкую документацию Django и быстро создавать мощные веб-приложения и современные API-интерфейсы с минимальным кодом.

    3. [django-ninja-jwt](django-ninja-jwt/index.md): Плагин JSON Web Token для django-ninja, реализующий аутентификацию и связанный функционал, форк популярного плагина Django Rest Framework.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
