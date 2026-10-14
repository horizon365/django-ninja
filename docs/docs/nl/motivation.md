---
comments: true
---
# Motivatie

!!! note
    **Django Ninja** ziet er in grote lijnen precies hetzelfde uit als **FastAPI**, dus waarom niet gewoon FastAPI gebruiken?

Inderdaad, **Django Ninja** is sterk geïnspireerd door <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a> (ontwikkeld door <a href="https://github.com/tiangolo" target="_blank">Sebastián Ramírez</a>)

Toch zijn er enkele problemen wanneer je FastAPI en Django correct samen wilt laten werken:

1) **FastAPI** beweert ORM-agnostisch te zijn (wat betekent dat je het kunt gebruiken met SQLAlchemy of de Django ORM), maar in de praktijk is de Django ORM nog niet klaar voor async-gebruik (waarschijnlijk in versie 4.0 of 4.1). Als je het in synchrone modus gebruikt, kun je [problemen met het sluiten van verbindingen](https://github.com/tiangolo/fastapi/issues/716) tegenkomen en moet je **heel veel** moeite doen om die te overwinnen.

2) Wanneer je in je operaties afhankelijk bent van authenticatie en databasesessies (voor sommige projecten betreft dit ongeveer 99% van alle operaties), maakt dependency injection met parameters je code overdreven uitgebreid.

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

3) Omdat het woord `model` in Django "gereserveerd" is voor gebruik door de ORM, wordt het erg rommelig wanneer je de naamgevingsconventies van Django ORM en Pydantic/FastAPI-modellen door elkaar gebruikt.

### Django Ninja

Django Ninja lost al deze problemen op en integreert zeer goed met Django (ORM, URL's, views, authenticatie, enz.).
Tijdens mijn werk bij [Code-on, een Django webdesign- en ontwikkelstudio](https://code-on.be/), kwam ik allerlei uitdagingen tegen, en om die aan te pakken ben ik in 2020 het Django-Ninja-project gestart.

Let op: **Django Ninja is een productieklaar project** - ik schat dat op dit moment meer dan 100 bedrijven het in productie gebruiken, met elke maand 500 nieuwe ontwikkelaars erbij.

Sommige bedrijven zoeken al naar ontwikkelaars met Django Ninja-ervaring.

#### Belangrijkste functies

1) Omdat je meerdere Django Ninja API-instanties kunt hebben, kun je [meerdere API-versies](guides/versioning.md) binnen één Django-project draaien.

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

2) De 'Schema'-klasse van Django Ninja integreert met de ORM, zodat je [querysets kunt serialiseren](guides/response/index.md#returning-querysets) of ORM-objecten:

```python
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()


@api.get("/tasks", response=TaskSchema)
def tasks_details(request):
    task = Task.objects.first()
    return task
```
3) [Maak een Schema op basis van een Django-model](guides/response/django-pydantic.md).

4) In plaats van afhankelijkheidsparameters te gebruiken, gebruikt **Django Ninja** eigenschappen van de `request`-instantie (op dezelfde manier als gewone Django-views) - zie [Authenticatie](guides/authentication.md) voor meer details.

!!! note

    Bekijk de **[Tutorial](tutorial/index.md)** om snel aan de slag te gaan.

    Het ecosysteem rond Django Ninja:

    1. [django-ninja-crud](django-ninja-crud/index.md): Een framework gebouwd op django-ninja om de ontwikkeling van CRUD-interfaces te vereenvoudigen, met declaratieve model-viewsets en scenario-gebaseerde testmethoden.

    2. [django-ninja-extra](django-ninja-extra/index.md): Een tool waarmee ontwikkelaars de uitgebreide Django-documentatie kunnen overslaan en met minimale code snel krachtige webapplicaties en moderne API-interfaces kunnen bouwen.

    3. [django-ninja-jwt](django-ninja-jwt/index.md): Een JSON Web Token-plugin voor django-ninja die authenticatie en verwante functies implementeert, geforkt van een populaire Django Rest Framework-plugin.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
