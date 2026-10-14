---
comments: true
---
# Motivation

!!! note
    **Django Ninja** sieht im Grunde genauso aus wie **FastAPI** — warum also nicht einfach FastAPI verwenden?

Tatsächlich wurde **Django Ninja** stark von <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a> inspiriert (entwickelt von <a href="https://github.com/tiangolo" target="_blank">Sebastián Ramírez</a>)

Trotzdem gibt es einige Probleme, wenn man FastAPI und Django korrekt zusammenbringen möchte:

1) **FastAPI** gibt an, ORM-agnostisch zu sein (d. h. Sie können es mit SQLAlchemy oder dem Django ORM verwenden), aber in der Praxis ist das Django ORM noch nicht für die asynchrone Verwendung bereit (vermutlich in Version 4.0 oder 4.1). Wenn Sie es im synchronen Modus verwenden, können Sie auf [Probleme beim Schließen von Verbindungen](https://github.com/tiangolo/fastapi/issues/716) stoßen, und es braucht **viel** Aufwand, um sie zu überwinden.

2) Wenn Sie in Ihren Operationen auf Authentifizierung und Datenbank-Sessions angewiesen sind (bei manchen Projekten sind das etwa 99 % aller Operationen), macht Dependency Injection mit Parametern Ihren Code übermäßig ausführlich.

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

3) Da das Wort `model` in Django für das ORM „reserviert" ist, wird es sehr unübersichtlich, wenn man die Namenskonventionen von Django ORM und Pydantic/FastAPI-Modellen vermischt.

### Django Ninja

Django Ninja löst all diese Probleme und integriert sich sehr gut mit Django (ORM, URLs, Views, Authentifizierung usw.).
Während meiner Arbeit bei [Code-on, einem Django-Webdesign- und Entwicklungsstudio](https://code-on.be/), bin ich auf vielfältige Herausforderungen gestoßen, und um sie anzugehen, habe ich 2020 das Django-Ninja-Projekt gestartet.

Hinweis: **Django Ninja ist ein produktionsreifes Projekt** — ich schätze, dass es inzwischen von mehr als 100 Unternehmen im Produktivbetrieb eingesetzt wird, mit 500 neuen Entwicklern pro Monat.

Einige Unternehmen suchen bereits nach Entwicklern mit Django-Ninja-Erfahrung.

#### Hauptmerkmale

1) Da Sie mehrere Django-Ninja-API-Instanzen haben können, können Sie [mehrere API-Versionen](guides/versioning.md) in einem einzigen Django-Projekt betreiben.

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

2) Die Klasse `Schema` von Django Ninja integriert sich mit dem ORM, sodass Sie [Querysets serialisieren](guides/response/index.md#returning-querysets) oder ORM-Objekte serialisieren können:

```python
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()


@api.get("/tasks", response=TaskSchema)
def tasks_details(request):
    task = Task.objects.first()
    return task
```
3) [Ein Schema aus einem Django-Modell erstellen](guides/response/django-pydantic.md).

4) Statt Dependency-Parameter zu verwenden, nutzt **Django Ninja** Eigenschaften der `request`-Instanz (auf die gleiche Weise wie reguläre Django-Views) — siehe [Authentifizierung](guides/authentication.md) für weitere Details.

!!! note

    Sehen Sie sich das **[Tutorial](tutorial/index.md)** an, um schnell loszulegen.

    Das Ökosystem rund um Django Ninja:

    1. [django-ninja-crud](django-ninja-crud/index.md): Ein auf django-ninja aufbauendes Framework zur Vereinfachung der Entwicklung von CRUD-Schnittstellen, mit deklarativen Model-Viewsets und szenariobasierten Testmethoden.

    2. [django-ninja-extra](django-ninja-extra/index.md): Ein Werkzeug, mit dem Entwickler umfangreiche Django-Dokumentation überspringen und mit minimalem Code schnell leistungsfähige Webanwendungen und moderne API-Schnittstellen erstellen können.

    3. [django-ninja-jwt](django-ninja-jwt/index.md): Ein JSON-Web-Token-Plugin für django-ninja, das Authentifizierung und verwandte Funktionen implementiert, geforkt von einem beliebten Django Rest Framework Plugin.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
