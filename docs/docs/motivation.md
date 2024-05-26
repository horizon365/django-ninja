# 开发动机

!!! 引言
    **Django Ninja** 看起来基本上和 **FastAPI** 一样， 那为什么不直接使用 FastAPI 呢？

确实, **Django Ninja** 很大程度上受到了 <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a> (由 <a href="https://github.com/tiangolo" target="_blank">Sebastián Ramírez</a>开发)

也就是说，在让 FastAPI 和 Django 正确协同工作时存在一些问题：

1) **FastAPI** 宣称与对象关系映射无关 (意味着你可以将其与 SQLAlchemy 或 Django ORM 一起使用)，但实际上 Django ORM 还没有准备好用于异步使用（可能在 4.0 或 4.1 版本中），如果你在同步模式下使用它，你可能会遇到 [连接关闭问题](https://github.com/tiangolo/fastapi/issues/716) 你需要付出 **很大** 努力来克服。 

2) 当你在操作中依赖认证和数据库会话时（对于某些项目，这大约占所有操作的 99%），带有参数的依赖注入会使你的代码过于冗长。

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

3) 由于`model`这个词在 Django 中是 "预留" 给 ORM 使用的, 当你将 Django ORM 与 Pydantic/FastAPI 模型命名约定混合时，会变得非常混乱。

### Django Ninja

Django Ninja 解决了所有这些问题，并且与 Django（ORM、网址、视图、认证等）非常好地集成。
在 [Code-on 一个Django 网页设计与开发工作室](https://code-on.be/)工作时，我遇到了各种各样的挑战，为了解决这些问题，我在 2020 年开始了 Django-Ninja 项目。

注意: **Django Ninja 是一个可用于生产环境的项目** - 我估计此时已经有 100 多家公司在生产中使用它，每月有 500 名新开发人员加入。

一些公司已经在寻找具有 Django Ninja 经验的开发人员。

#### 主要特性

1) 由于你可以有多个 Django Ninja API 实例 - 你可以在一个 Django 项目中运行 [多个 API 版本](guides/versioning.md) 。

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

2) Django Ninja 的 'Schema' 类与 ORM 集成，所以你可以 [序列化查询集](guides/response/index.md#returning-querysets) 或 ORM 对象:

```python
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()


@api.get("/tasks", response=TaskSchema)
def tasks_details(request):
    task = Task.objects.first()
    return task
```
3) [从 Django 模型创建 Schema](guides/response/django-pydantic.md).

4) **Django Ninja**不是使用依赖参数，而是使用 `request` 实例属性 (与常规 Django 视图的方式相同) - 更多细节请参阅[认证](guides/authentication.md).
