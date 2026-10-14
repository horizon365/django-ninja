---
comments: true
---
# レスポンススキーマ

**Django Ninja** では、バリデーションとドキュメント化の目的でレスポンススキーマを定義できます。

ユーザーを作成する API オペレーションを作成する必要があるとします。**入力**パラメータは **username+password** ですが、このオペレーションの**出力**は **id+username** であるべきです（パスワードは**含めない**）。

入力スキーマを作成しましょう:

```python hl_lines="3 5"
from ninja import Schema

class UserIn(Schema):
    username: str
    password: str


@api.post("/users/")
def create_user(request, data: UserIn):
    user = User(username=data.username) # User class comes from django auth.User
    user.set_password(data.password)
    user.save()
    # ... return ?
```

次に、出力スキーマを定義し、`response` 引数として `@api.post` デコレータに渡します:

```python hl_lines="8 9 10 13 18"
from ninja import Schema

class UserIn(Schema):
    username: str
    password: str


class UserOut(Schema):
    id: int
    username: str


@api.post("/users/", response=UserOut)
def create_user(request, data: UserIn):
    user = User(username=data.username)
    user.set_password(data.password)
    user.save()
    return user
```

**Django Ninja** は `response` スキーマを次の目的で使用します:

- 出力データを宣言されたスキーマに変換する
- データをバリデーションする
- OpenAPI スキーマ定義を追加する
- 自動ドキュメントシステムで使用される
- そして最も重要なこととして、出力データをスキーマで定義されたフィールドのみに**制限する**。

## ネストされたオブジェクト

ネストされた/サブオブジェクトを含むレスポンスを返す必要があることもよくあります。

`User` への外部キーを持つ `Task` Django モデルがあるとします:

```python hl_lines="6"
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey("auth.User", null=True, blank=True)
```

次に、すべてのタスクを出力し、各タスクについてユーザーに関するいくつかのフィールドを出力してみましょう。

```python hl_lines="13 16"
from typing import List
from ninja import Schema

class UserSchema(Schema):
    id: int
    first_name: str
    last_name: str

class TaskSchema(Schema):
    id: int
    title: str
    is_completed: bool
    owner: UserSchema = None  # ! None - the marker makes it non-required


@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    queryset = Task.objects.select_related("owner")
    return list(queryset)
```

このオペレーションを実行すると、次のようなレスポンスが得られるはずです:

```JSON hl_lines="6 7 8 9 16"
[
    {
        "id": 1,
        "title": "Task 1",
        "is_completed": false,
        "owner": {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
        }
    },
    {
        "id": 2,
        "title": "Task 2",
        "is_completed": false,
        "owner": null
    },
]
```

## エイリアス

ネストされたレスポンスを使う代わりに、レスポンスの出力を単にフラット化したい場合もあるでしょう。
Ninja の `Schema` オブジェクトは、ドット表記のレスポンスを扱えるよう、Pydantic の `Field(..., alias="")` 形式を拡張しています。

上記のモデルを使って、タスクオーナーの名だけをインラインで含み、`is_completed` の代わりに `completed` を使用するスキーマを作成してみましょう:

```python hl_lines="1 7-9"
from ninja import Field, Schema


class TaskSchema(Schema):
    id: int
    title: str
    # The first Field argument is the default value; use ... for required fields.
    completed: bool = Field(..., alias="is_completed")
    owner_first_name: str = Field(None, alias="owner.first_name")
```

エイリアスは Django テンプレート構文の変数アクセスもサポートしています:

```python hl_lines="2"
class TaskSchema(Schema):
    last_message: str = Field(None, alias="message_set.0.text")
```

```python hl_lines="3"
class TaskSchema(Schema):
    type: str = Field(None)
    type_display: str = Field(None, alias="get_type_display") # callable will be executed
```

## リゾルバ

フィールド名に基づいたリゾルバメソッドで、計算されたフィールドを作成することもできます。

メソッドは 1 つの引数を受け取る必要があり、その引数はスキーマが解決しようとしているオブジェクトです。

リゾルバを標準メソッドとして作成すると、`self` を通じてスキーマ内の他のバリデーション済み・フォーマット済みの属性にアクセスできます。

```python hl_lines="5 7-11"
class TaskSchema(Schema):
    id: int
    title: str
    is_completed: bool
    owner: Optional[str] = None
    lower_title: str

    @staticmethod
    def resolve_owner(obj):
        if not obj.owner:
            return
        return f"{obj.owner.first_name} {obj.owner.last_name}"

    def resolve_lower_title(self, obj):
        return self.title.lower()
```

### 追加コンテキストへのアクセス

Pydantic v2 では、シリアライザに渡された追加のコンテキストを扱うことができます。次の例では、渡された `context` 引数からリクエストオブジェクトを取得するリゾルバを持つことができます:
```python hl_lines="6"
class Data(Schema):
    a: int
    path: str = ""

    @staticmethod
    def resolve_path(obj, context):
        request = context["request"]
        return request.path
```

このスキーマを受信リクエストに使用すると — リクエストオブジェクトが自動的にコンテキストに渡されます。

独自のコンテキストを渡すこともできます:

```python
data = Data.model_validate({'some': 1}, context={'request': MyRequest()})
```

## クエリセットの返却

前の例では、意図的にクエリセットをリストに変換しました（評価時に SQL クエリが実行されます）。

これを避けて、クエリセットをそのまま結果として返すこともできます。自動的にリストとして評価されます:

```python hl_lines="3"
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()
```

!!! warning

    オペレーションが非同期の場合、この例は動作しません。ORM クエリは安全な方法で呼び出す必要があるためです。
    ```python hl_lines="2"
    @api.get("/tasks", response=List[TaskSchema])
    async def tasks(request):
        return Task.objects.all()
    ```

    詳細については、[非同期サポート](../async-support.md#using-orm) を参照してください。

## ファイルフィールドとイメージフィールド

**Django Ninja** は、（`FileField` または `ImageField` で宣言された）ファイルや画像を、デフォルトで `string` の URL に変換します。

例:

```python hl_lines="3"
class Picture(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
```

画像フィールドをレスポンスに出力する必要がある場合は、次のようにスキーマを宣言します:

```python hl_lines="3"
class PictureSchema(Schema):
    title: str
    image: str
```

これをレスポンスに出力すると、各オブジェクトに対して URL が自動的に生成されます:

```JSON
{
    "title": "Zebra",
    "image": "/static/images/zebra.jpg"
}
```

## 複数のレスポンススキーマ

複数のレスポンススキーマを定義する必要がある場合があります。

たとえば、認証の場合は次のようなレスポンスを返すかもしれません:

- **200** 成功 -> token
- **401** -> Unauthorized
- **402** -> Payment required
- など

実際、[OpenAPI 仕様](https://swagger.io/docs/specification/describing-responses/)では複数のレスポンススキーマを渡すことが許されています。

`response` 引数に辞書を渡すことができます。ここで:

- キーはレスポンスコード
- 値は各コードに対応するスキーマ

また、結果を返すときには — どのスキーマをバリデーションとシリアライズに使用すべきかを **Django Ninja** に伝えるために、ステータスコードも一緒に渡す必要があります。

例:

```python hl_lines="9 12 14 16"
class Token(Schema):
    token: str
    expires: date

class Message(Schema):
    message: str


@api.post('/login', response={200: Token, 401: Message, 402: Message})
def login(request, payload: Auth):
    if auth_not_valid:
        return 401, {'message': 'Unauthorized'}
    if negative_balance:
        return 402, {'message': 'Insufficient balance amount. Please proceed to a payment page.'}
    return 200, {'token': xxx, ...}
```

## 複数のレスポンスコード

前の例では、基本的に `Message` スキーマを 2 回繰り返していました:

```
...401: Message, 402: Message}
```

この重複を避けるために、1 つのスキーマに複数のレスポンスコードを指定できます:

```python hl_lines="2 5 8 10"
...
from ninja.responses import codes_4xx


@api.post('/login', response={200: Token, codes_4xx: Message})
def login(request, payload: Auth):
    if auth_not_valid:
        return 401, {'message': 'Unauthorized'}
    if negative_balance:
        return 402, {'message': 'Insufficient balance amount. Please proceed to a payment page.'}
    return 200, {'token': xxx, ...}
```

**Django Ninja** には次の HTTP コードが付属しています:

```python
from ninja.responses import codes_1xx
from ninja.responses import codes_2xx
from ninja.responses import codes_3xx
from ninja.responses import codes_4xx
from ninja.responses import codes_5xx
```

`frozenset` を使用して独自の範囲を作成することもできます:

```python
my_codes = frozenset({416, 418, 425, 429, 451})

@api.post('/login', response={200: Token, my_codes: Message})
def login(request, payload: Auth):
    ...
```

## 空のレスポンス

[204 No Content](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204) のような一部のレスポンスにはボディがありません。
レスポンスボディが空であることを示すには、`response` 引数にスキーマの代わりに `None` を指定します:

```python hl_lines="1 3"
@api.post("/no_content", response={204: None})
def no_content(request):
    return 204, None
```

## エラーレスポンス

詳細については、[エラーハンドリング](../errors.md) を参照してください。

## 自己参照スキーマ

- スキーマが自分自身やツリー状の構造オブジェクトを参照する必要がある場合があります。

- そのためには、次のようにします:

- スキーマの型を引用符で囲む

- `update_forward_refs` メソッドを使って自己参照型を適用する

```python hl_lines="3 6"
class Organization(Schema):
    title: str
    part_of: 'Organization' = None     #!! Note that the type here needs to be in quotes!! !!


Organization.update_forward_refs()  # !!! this line is important


@api.get('/organizations', response=List[Organization])
def list_organizations(request):
    ...
```

## `create_schema()` で生成された自己参照スキーマ

`create_schema()` で生成したスキーマの `update_forward_refs()` メソッドを使用できるようにするには、クラスの "name" が名前空間に存在している必要があります。この場合、`create_schema()` に `name` 引数を渡すことが重要です。

```python hl_lines="3"
UserSchema = create_schema(
    User,
    name='UserSchema',  # !!! this is important for update_forward_refs()
    fields=['id', 'username']
    custom_fields=[
        ('manager', 'UserSchema', None),
    ]
)
UserSchema.update_forward_refs()
```

## ビューの外でのシリアライズ

スキーマオブジェクトの `.from_orm()` メソッドを使えば、コード内でオブジェクトを直接シリアライズできます。

次のモデルを考えてみましょう:

```python
class Person(models.Model):
    name = models.CharField(max_length=50)
```

これは次のスキーマでアクセスできます:
```python
class PersonSchema(Schema):
    name: str
```

シリアライズは、スキーマの `.from_orm()` メソッドを使って直接行えます。スキーマオブジェクトのインスタンスを取得したら、`.dict()` メソッドと `.json()` メソッドで辞書出力と文字列の JSON 版を取得できます。

```python
>>> person = Person.objects.get(id=1)
>>> data = PersonSchema.from_orm(person)
>>> data
PersonSchema(id=1, name='Mr. Smith')
>>> data.dict()
{'id':1, 'name':'Mr. Smith'}
>>> data.json()
'{"id":1, "name":"Mr. Smith"}'
```

複数のエントリ: またはクエリセット（またはリスト）

```python
>>> persons = Person.objects.all()
>>> data = [PersonSchema.from_orm(i).dict() for i in persons]
[{'id':1, 'name':'Mr. Smith'},{'id': 2, 'name': 'Mrs. Smith'}...]
```

## Django の HTTP レスポンス

通常の Django HTTP レスポンスを返すことも可能です:

```python
from django.http import HttpResponse
from django.shortcuts import redirect


@api.get("/http")
def result_django(request):
    return HttpResponse('some data')   # !!!!


@api.get("/something")
def some_redirect(request):
    return redirect("/some-path")  # !!!!
```

!!! done

    次の章に進みましょう！ **[レスポンスの調整](temporal_response.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
