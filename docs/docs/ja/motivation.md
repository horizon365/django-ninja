---
comments: true
---
# 動機

!!! note
    **Django Ninja** は基本的に **FastAPI** と見た目がほぼ同じです。では、なぜ FastAPI をそのまま使わないのでしょうか？

実際のところ、**Django Ninja** は <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a>（<a href="https://github.com/tiangolo" target="_blank">Sebastián Ramírez</a> 氏が開発）に大きな影響を受けています

とはいえ、FastAPI と Django を正しく連携させるにはいくつかの問題があります：

1) **FastAPI** は ORM に依存しない（つまり SQLAlchemy や Django ORM と併用できる）と謳っていますが、実際には Django ORM はまだ非同期での利用に対応していません（おそらくバージョン 4.0 か 4.1 で対応予定）。同期モードで使うと、[接続が閉じられる問題](https://github.com/tiangolo/fastapi/issues/716) に遭遇する可能性があり、それを克服するには**非常に大きな**労力が必要です。

2) 操作の中で認証やデータベースセッションに依存している場合（プロジェクトによっては全操作の約 99% に相当します）、パラメータによる依存性の注入はコードを過度に冗長にします。

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

3) Django では `model` という単語が ORM 用に「予約」されているため、Django ORM と Pydantic/FastAPI のモデル命名規則を混在させると、非常に混乱したことになります。

### Django Ninja

Django Ninja はこれらの問題をすべて解決し、Django（ORM、URL、ビュー、認証など）と非常にうまく統合されます。
[Django の Web デザイン・開発スタジオ Code-on](https://code-on.be/) で働いていたとき、私はさまざまな課題に直面し、それらに対処するために 2020 年に Django-Ninja プロジェクトを開始しました。

注意: **Django Ninja は本番環境で使用できるプロジェクトです** - 現時点で 100 社以上が本番環境で利用しており、毎月 500 人の新しい開発者が参加していると見積もっています。

すでに Django Ninja の経験を持つ開発者を募集している企業もあります。

#### 主な特徴

1) Django Ninja の API インスタンスは複数持つことができるため、1 つの Django プロジェクトで [複数の API バージョン](guides/versioning.md) を実行できます。

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

2) Django Ninja の 'Schema' クラスは ORM と統合されているため、[クエリセット](guides/response/index.md#returning-querysets) や ORM オブジェクトをシリアライズできます：

```python
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()


@api.get("/tasks", response=TaskSchema)
def tasks_details(request):
    task = Task.objects.first()
    return task
```
3) [Django モデルから Schema を作成する](guides/response/django-pydantic.md)。

4) 依存性パラメータを使う代わりに、**Django Ninja** は `request` インスタンスのプロパティを使用します（通常の Django ビューと同じ方法です）- 詳細は [認証](guides/authentication.md) を参照してください。

!!! note

    すぐに始めたい場合は **[チュートリアル](tutorial/index.md)** をチェックしてください。

    Django Ninja を取り巻くエコシステム：

    1. [django-ninja-crud](django-ninja-crud/index.md): django-ninja をベースに構築された、CRUD インターフェースの開発を簡素化するフレームワーク。宣言的なモデルビューセットとシナリオベースのテスト手法を提供します。

    2. [django-ninja-extra](django-ninja-extra/index.md): 冗長な Django ドキュメントを読み飛ばし、最小限のコードで強力な Web アプリケーションとモダンな API インターフェースを素早く構築できるツールです。

    3. [django-ninja-jwt](django-ninja-jwt/index.md): django-ninja 向けの JSON Web Token プラグイン。認証および関連機能を実装しており、人気の高い Django Rest Framework プラグインからフォークされました。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
