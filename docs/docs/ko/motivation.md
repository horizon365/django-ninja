---
comments: true
---
# 동기

!!! note
    **Django Ninja**는 기본적으로 **FastAPI**와 거의 동일해 보입니다. 그렇다면 FastAPI를 그냥 쓰면 안 되는 걸까요?

실제로 **Django Ninja**는 <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a> (<a href="https://github.com/tiangolo" target="_blank">Sebastián Ramírez</a>가 개발)로부터 큰 영감을 받았습니다

그렇긴 하지만, FastAPI와 Django를 올바르게 함께 사용할 때 몇 가지 문제가 있습니다:

1) **FastAPI**는 ORM에 구애받지 않는다고 주장합니다 (즉, SQLAlchemy나 Django ORM과 함께 사용할 수 있음). 하지만 실제로 Django ORM은 아직 async 사용이 준비되지 않았습니다 (아마도 버전 4.0 또는 4.1에서). 동기 모드로 사용하면 [연결 종료 문제](https://github.com/tiangolo/fastapi/issues/716)에 부딪힐 수 있으며, 이를 극복하려면 **많은** 노력이 필요합니다.

2) operation에서 인증과 데이터베이스 세션에 의존할 때 (일부 프로젝트에서는 전체 operation의 약 99%에 해당), 파라미터를 통한 의존성 주입은 코드를 지나치게 장황하게 만듭니다.

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

3) Django에서는 `model`이라는 단어가 ORM을 위해 "예약되어" 있기 때문에, Django ORM과 Pydantic/FastAPI의 모델 명명 규칙을 섞어 쓰면 매우 혼란스러워집니다.

### Django Ninja

Django Ninja는 이러한 모든 문제를 해결하고 Django (ORM, URLs, views, 인증 등)와 매우 잘 통합됩니다.
[Django 웹 디자인 및 개발 스튜디오인 Code-on](https://code-on.be/)에서 일하면서 다양한 어려움을 겪었고, 이를 해결하기 위해 2020년에 Django-Ninja 프로젝트를 시작했습니다.

참고: **Django Ninja는 프로덕션 준비가 완료된 프로젝트입니다** - 현재 기준으로 100개 이상의 회사가 프로덕션에서 사용하고 있으며, 매월 500명의 새로운 개발자가 합류하고 있다고 추정합니다.

일부 회사는 이미 Django Ninja 경험이 있는 개발자를 찾고 있습니다.

#### 주요 특징

1) 여러 Django Ninja API 인스턴스를 가질 수 있으므로, 하나의 Django 프로젝트에서 [여러 API 버전](guides/versioning.md)을 운영할 수 있습니다.

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

2) Django Ninja의 'Schema' 클래스는 ORM과 통합되므로, queryset이나 ORM 객체를 [직렬화](guides/response/index.md#returning-querysets)할 수 있습니다:

```python
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()


@api.get("/tasks", response=TaskSchema)
def tasks_details(request):
    task = Task.objects.first()
    return task
```
3) [Django 모델로부터 Schema 생성하기](guides/response/django-pydantic.md).

4) 의존성 파라미터를 사용하는 대신, **Django Ninja**는 `request` 인스턴스의 속성을 사용합니다 (일반 Django view와 동일한 방식) - 자세한 내용은 [인증](guides/authentication.md)을 참조하세요.

!!! note

    빠르게 시작하려면 **[튜토리얼](tutorial/index.md)**을 확인해 보세요.

    Django Ninja를 둘러싼 생태계:

    1. [django-ninja-crud](django-ninja-crud/index.md): django-ninja 위에 구축되어 CRUD 인터페이스 개발을 단순화하고, 선언적 model viewset과 시나리오 기반 테스트 방법을 제공하는 프레임워크입니다.

    2. [django-ninja-extra](django-ninja-extra/index.md): 개발자가 방대한 Django 문서를 건너뛰고 최소한의 코드로 강력한 웹 애플리케이션과 현대적인 API 인터페이스를 빠르게 구축할 수 있게 해주는 도구입니다.

    3. [django-ninja-jwt](django-ninja-jwt/index.md): django-ninja를 위한 JSON Web Token 플러그인으로, 인증 및 관련 기능을 구현하며 인기 있는 Django Rest Framework 플러그인에서 포크되었습니다.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
