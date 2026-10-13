---
comments: true
---
# Motivation

!!! note
    **Django Ninja** looks basically the same as **FastAPI**, so why not just use FastAPI?

Indeed, **Django Ninja** was heavily inspired by <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a> (developed by <a href="https://github.com/tiangolo" target="_blank">Sebastián Ramírez</a>)

That said, there are some issues when making FastAPI and Django work together correctly:

1) **FastAPI** claims to be ORM-agnostic (meaning you can use it with SQLAlchemy or the Django ORM), but in practice the Django ORM is not yet ready for async usage (probably in version 4.0 or 4.1). If you use it in synchronous mode, you may run into [connection closing issues](https://github.com/tiangolo/fastapi/issues/716) and you need to put in a **lot** of effort to overcome them.

2) When you rely on authentication and database sessions in your operations (for some projects this is about 99% of all operations), dependency injection with parameters makes your code overly verbose.

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

3) Since the word `model` is "reserved" in Django for use by the ORM, things get very messy when you mix Django ORM and Pydantic/FastAPI model naming conventions.

### Django Ninja

Django Ninja solves all of these issues and integrates very well with Django (ORM, URLs, views, authentication, etc.).
While working at [Code-on, a Django web design and development studio](https://code-on.be/), I encountered a variety of challenges, and to address them I started the Django-Ninja project in 2020.

Note: **Django Ninja is a production-ready project** - I estimate that at this point more than 100 companies use it in production, with 500 new developers joining every month.

Some companies are already looking for developers with Django Ninja experience.

#### Main features

1) Since you can have multiple Django Ninja API instances, you can run [multiple API versions](guides/versioning.md) in a single Django project.

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

2) Django Ninja's 'Schema' class integrates with the ORM, so you can [serialize querysets](guides/response/index.md#returning-querysets) or ORM objects:

```python
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()


@api.get("/tasks", response=TaskSchema)
def tasks_details(request):
    task = Task.objects.first()
    return task
```
3) [Create a Schema from a Django model](guides/response/django-pydantic.md).

4) Instead of using dependency parameters, **Django Ninja** uses `request` instance properties (the same way regular Django views do) - see [Authentication](guides/authentication.md) for more details.

!!! note

    Check out the **[Tutorial](tutorial/index.md)** to get started quickly.

    Ecosystem around Django Ninja:

    1. [django-ninja-crud](django-ninja-crud/index.md): A framework built on django-ninja to simplify CRUD interface development, providing declarative model viewsets and scenario-based testing methods.

    2. [django-ninja-extra](django-ninja-extra/index.md): A tool that lets developers skip verbose Django documentation and quickly build powerful web applications and modern API interfaces with minimal code.

    3. [django-ninja-jwt](django-ninja-jwt/index.md): A JSON Web Token plugin for django-ninja that implements authentication and related features, forked from a popular Django Rest Framework plugin.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
