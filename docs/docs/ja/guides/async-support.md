---
comments: true
---
## はじめに

**バージョン 3.1** から、Django は**非同期ビューのサポート**を備えました。これにより、ネットワークや I/O がボトルネックになる効率的な同時実行ビューを実行できます。

```
pip install Django>=3.1 django-ninja
```

非同期ビューがより効率的に動作するケース:
- ネットワーク経由で外部 API を呼び出す場合
- データベースクエリの実行/待機
- ディスクへの読み書き

**Django Ninja** は非同期ビューを完全にサポートしており、非常に簡単に使用できます。

## クイック例

### コード

例を見てみましょう。何らかの処理（今のところは指定された秒数だけスリープするだけ）を行い、単語を返す API オペレーションがあります:
```python hl_lines="5"
import time

@api.get("/say-after")
def say_after(request, delay: int, word: str):
    time.sleep(delay)
    return {"saying": word}
```

このコードを非同期で実行するには、関数に **`async`** キーワードを追加するだけです（処理には非同期対応のライブラリを使用します - ここでは標準ライブラリの `sleep` を `asyncio.sleep` に置き換えます）:

```python hl_lines="1 4 5"
import asyncio

@api.get("/say-after")
async def say_after(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}
```

### 実行

このコードを実行するには、<a href="https://www.uvicorn.org/" target="_blank">Uvicorn</a> や <a href="https://github.com/django/daphne" target="_blank">Daphne</a> のような ASGI サーバーが必要です。ここでは Uvicorn を使い、例は以下の通りです:

Uvicorn をインストールするには:

```
pip install uvicorn
```

次にサーバーを起動します:

```
uvicorn your_project.asgi:application --reload
```

> <small>
> *注: `your_project` は自分のプロジェクトのパッケージ名に置き換えてください*<br>
> *`--reload` フラグは、コードを変更した際にサーバーを自動的に再起動するために使用します（本番環境では使用しないでください）*
> </small>

!!! note
    非同期ビューは `manage.py runserver` でも実行できますが、一部のライブラリとうまく動作しないため、現時点（2020年7月）では Uvicorn や Daphne のような ASGI サーバーの使用が推奨されます。

### テスト

ブラウザで <a href="http://127.0.0.1:8000/api/say-after?delay=3&word=hello" target="_blank">http://127.0.0.1:8000/api/say-after?delay=3&word=hello</a>（**delay=3**）を開きます。
3 秒待つと、"hello" メッセージが表示されるはずです。

次に、このオペレーションに **100 件の並列リクエスト**を送ってみましょう:

```
ab -c 100 -n 100 "http://127.0.0.1:8000/api/say-after?delay=3&word=hello"
```

結果は次のようになります:

```
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   1.1      1       4
Processing:  3008 3063  16.2   3069    3082
Waiting:     3008 3062  15.7   3068    3079
Total:       3008 3065  16.3   3070    3083

Percentage of the requests served within a certain time (ms)
  50%   3070
  66%   3072
  75%   3075
  80%   3076
  90%   3081
  95%   3082
  98%   3083
  99%   3083
 100%   3083 (longest request)
```

この数値から、私たちのサービスはわずかなオーバーヘッドだけでこれら 100 件の同時リクエストを処理できていることがわかります。

WSGI と同期処理で同じ並列性を実現するには、各スレッド 10 本のワーカーを約 10 個起動する必要があるでしょう！

## 同期処理と非同期処理の混在

プロジェクトでは**同期オペレーションと非同期オペレーションの両方を使用できる**こと、そして **Django Ninja** がそれらを自動的にルーティングすることを覚えておいてください:

```python hl_lines="2 7"

@api.get("/say-sync")
def say_after_sync(request, delay: int, word: str):
    time.sleep(delay)
    return {"saying": word}

@api.get("/say-async")
async def say_after_async(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}
```

## Elasticsearch の例

実際のユースケースを見てみましょう。この例では、非同期サポートを備えた最近のバージョンの Elasticsearch を使用します:
```
pip install elasticsearch>=7.8.0
```

`Elasticsearch` クラスの代わりに `AsyncElasticsearch` クラスを使用し、結果を `await` します:

```python hl_lines="2 7 11 12"
from ninja import NinjaAPI
from elasticsearch import AsyncElasticsearch


api = NinjaAPI()

es = AsyncElasticsearch()


@api.get("/search")
async def search(request, q: str):
    resp = await es.search(
        index="documents", 
        body={"query": {"query_string": {"query": q}}},
        size=20,
    )
    return resp["hits"]
```

## ORM の使用

現在、Django の重要な部分の一部は、コルーチンを考慮しないグローバルな状態を持つため、非同期環境では安全に動作できません。Django のこれらの部分は「非同期非対応（asynchronous-unsafe）」に分類され、非同期環境での実行から保護されています。**ORM** がその代表例ですが、このように保護されている部分は他にもあります。
非同期セーフティの詳細については、<a href="https://docs.djangoproject.com/en/stable/topics/async/#async-safety" target="_blank">Django 公式ドキュメント</a>を参照してください。

したがって、次のように書くと:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = Blog.objects.get(pk=post_id)
    ...
```

エラーが発生します。非同期 ORM の実装が利用可能になるまでの間は、`sync_to_async()` アダプタを使用できます:

```python hl_lines="1 3 9"
from asgiref.sync import sync_to_async

@sync_to_async
def get_blog(post_id):
    return Blog.objects.get(pk=post_id)

@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await get_blog(post_id)
    ...
```

もっと短く書くこともできます:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await sync_to_async(Blog.objects.get)(pk=post_id)
    ...
```

よくある**落とし穴**があります: Django のクエリセットは遅延評価されます（データベースクエリはイテレーションを開始したときに初めて実行されます）。そのため、次のコードは**動作しません**:

```python
all_blogs = await sync_to_async(Blog.objects.all)()
# 後で all_blogs をイテレートしようとしたときにエラーが発生します
...
```

代わりに、`list` で強制的に評価してください:

```python
all_blogs = await sync_to_async(list)(Blog.objects.all())
...
```

Django **バージョン 4.1** から、Django は ORM 操作の非同期バージョンを備えました。
これにより、ほとんどの場合 `sync_to_async` を使用する必要がなくなります。
非同期操作は同期版と同じ名前に接頭辞 *a* を付けたものになっています。つまり、上記の例は
次のように書き直せます:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await Blog.objects.aget(pk=post_id)
    ...
```

クエリセットを扱う場合は、`async for` とリスト内包表記を組み合わせて使用します:

```python
all_blogs = [blog async for blog in Blog.objects.all()]
...
```

非同期 ORM インターフェースの詳細については、<a href="https://docs.djangoproject.com/en/4.1/releases/4.1/#asynchronous-orm-interface" target="_blank">Django 公式ドキュメント</a>を参照してください。

!!! success

    次のセクション **[API のバージョニング](versioning.md)** に進みましょう

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
