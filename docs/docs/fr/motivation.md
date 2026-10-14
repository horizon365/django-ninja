---
comments: true
---
# Motivation

!!! note
    **Django Ninja** se présente fondamentalement comme **FastAPI**, alors pourquoi ne pas utiliser simplement FastAPI ?

En effet, **Django Ninja** a été fortement inspiré par <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a> (développé par <a href="https://github.com/tiangolo" target="_blank">Sebastián Ramírez</a>)

Cela dit, certains problèmes se posent lorsque l'on fait fonctionner FastAPI et Django correctement ensemble :

1) **FastAPI** prétend être indépendant de l'ORM (ce qui signifie que vous pouvez l'utiliser avec SQLAlchemy ou l'ORM de Django), mais en pratique l'ORM de Django n'est pas encore prêt pour un usage asynchrone (probablement dans la version 4.0 ou 4.1). Si vous l'utilisez en mode synchrone, vous risquez de rencontrer des [problèmes de fermeture de connexions](https://github.com/tiangolo/fastapi/issues/716) et vous devrez fournir un **gros** effort pour les surmonter.

2) Lorsque vous vous appuyez sur l'authentification et les sessions de base de données dans vos opérations (pour certains projets, cela représente environ 99 % de toutes les opérations), l'injection de dépendances par paramètres rend votre code excessivement verbeux.

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

3) Comme le mot `model` est « réservé » dans Django pour l'ORM, les choses deviennent très confuses lorsque l'on mélange les conventions de nommage des modèles de l'ORM Django et celles de Pydantic/FastAPI.

### Django Ninja

Django Ninja résout tous ces problèmes et s'intègre très bien avec Django (ORM, URLs, vues, authentification, etc.).
En travaillant chez [Code-on, un studio de conception et de développement web Django](https://code-on.be/), j'ai rencontré toutes sortes de défis, et pour y répondre, j'ai lancé le projet Django-Ninja en 2020.

Remarque : **Django Ninja est un projet prêt pour la production** - j'estime qu'à l'heure actuelle plus de 100 entreprises l'utilisent en production, avec 500 nouveaux développeurs qui le rejoignent chaque mois.

Certaines entreprises recherchent déjà des développeurs ayant une expérience de Django Ninja.

#### Caractéristiques principales

1) Comme vous pouvez avoir plusieurs instances d'API Django Ninja, vous pouvez faire tourner [plusieurs versions d'API](guides/versioning.md) dans un seul projet Django.

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

2) La classe 'Schema' de Django Ninja s'intègre avec l'ORM, ce qui vous permet de [sérialiser des querysets](guides/response/index.md#returning-querysets) ou des objets ORM :

```python
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()


@api.get("/tasks", response=TaskSchema)
def tasks_details(request):
    task = Task.objects.first()
    return task
```
3) [Créer un Schema à partir d'un modèle Django](guides/response/django-pydantic.md).

4) Au lieu d'utiliser des paramètres d'injection de dépendances, **Django Ninja** utilise les propriétés de l'instance `request` (de la même manière que les vues Django habituelles) - voir [Authentification](guides/authentication.md) pour plus de détails.

!!! note

    Consultez le **[Tutoriel](tutorial/index.md)** pour démarrer rapidement.

    L'écosystème autour de Django Ninja :

    1. [django-ninja-crud](django-ninja-crud/index.md) : un framework construit sur django-ninja pour simplifier le développement d'interfaces CRUD, offrant des model viewsets déclaratifs et des méthodes de test par scénarios.

    2. [django-ninja-extra](django-ninja-extra/index.md) : un outil qui permet aux développeurs de s'affranchir de la documentation Django verbeuse et de construire rapidement des applications web puissantes et des interfaces API modernes avec un minimum de code.

    3. [django-ninja-jwt](django-ninja-jwt/index.md) : un plugin JSON Web Token pour django-ninja qui implémente l'authentification et les fonctionnalités associées, forké d'un plugin populaire de Django Rest Framework.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
