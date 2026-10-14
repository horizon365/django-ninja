---
title: Django Ninja - 高速な Django REST フレームワーク
template: home.html
comments: true
---

Django Ninja は、Django と Python 3.6+ の型ヒントを使って API を構築するための Web フレームワークです。

主な特徴：

 - **理解しやすい**: 使いやすさと直感性を重視して設計されています。
 - **高速な実行**: **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** と **<a href="guides/async-support/">非同期サポート</a>** のおかげで、非常に高いパフォーマンスを発揮します。
 - **高速なコーディング**: Django Ninja は、Django と Python 3.6+ の型ヒントを使って API を構築するための Web フレームワークです。
 - **標準準拠**: **OpenAPI**（旧 Swagger）や **JSON Schema** といった標準に基づいています。
 - **Django フレンドリー**: （言うまでもなく）Django コアや ORM とスムーズに統合できます。
 - **本番環境対応**: 複数の企業が実際のプロジェクトで利用しています（Django Ninja を利用していて、フィードバックを公開したい場合は ppr.vitaly@gmail.com までメールしてください）。

<a href="https://github.com/vitalik/django-ninja-benchmarks" target="_blank">ベンチマーク</a>：

![Django Ninja REST Framework](img/benchmark.png)

## インストール

```
pip install django-ninja
```

## クイック例

新しい Django プロジェクトを開始します（既存のプロジェクトを使っても構いません）
```
django-admin startproject apidemo
```

`urls.py` で：

```python hl_lines="3 5 8 9 10 15"
{!./src/index001.py!}
```

あとは通常どおり実行します：
```
./manage.py runserver
```

注意: 動作させるために、INSTALLED_APPS に Django Ninja を追加する必要はありません。

## 動作確認

ブラウザで <a href="http://127.0.0.1:8000/api/add?a=1&b=2" target="_blank">http://127.0.0.1:8000/api/add?a=1&b=2</a> を開いてください。

次のような JSON レスポンスが表示されます：
```JSON
{"result": 3}
```
これで、あなたは次のような API を作成したことになります：

 - `/api/add` で HTTP GET リクエストを受け取る
 - GET パラメータ `a` と `b` を受け取り、検証し、型変換する
 - 結果を JSON としてデコードする
 - 定義された操作の OpenAPI スキーマを生成する

## 対話型 API ドキュメント

次に <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a> にアクセスしてください。

自動生成された対話型の API ドキュメント（<a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a> または <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a> によるもの）が表示されます：

![Swagger UI](img/index-swagger-ui.png)


## まとめ

要するに、パラメータやリクエストボディなどの型を、関数の引数として**一度だけ**宣言すればよいのです。

これは標準的でモダンな Python の型を使って行います。

新しい構文や、特定のライブラリのメソッドやクラスなどを学ぶ必要はありません。

標準の **Python 3.6+** だけで十分です。

たとえば、`int` であれば：

```python
a: int
```

あるいは、より複雑な `Item` モデルであれば：

```python
class Item(Schema):
    foo: str
    bar: float

def operation(a: Item):
    ...
```

...この 1 つの宣言だけで、次のものが得られます：

* エディターサポート。次のものを含みます：
    * 自動補完
    * 型チェック
* データ検証：
    * データが無効な場合の自動的で明確なエラー
    * 深くネストされた JSON オブジェクトに対しても検証が可能
* <abbr title="Also known as: serialization, parsing, marshalling">シリアライゼーション</abbr> — ネットワークからの入力データを Python のデータへ変換して出力し、次のものから読み取ります：
    * JSON
    * パスパラメータ
    * クエリパラメータ
    * Cookies
    * Headers
    * フォーム
    * ファイル
* 自動生成される対話型 API ドキュメント

このプロジェクトは <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a> に大きな影響を受けています。

!!! note

    すぐに始めたい場合は **[チュートリアル](tutorial/index.md)** をチェックしてください。

    Django Ninja を取り巻くエコシステム：

    1. [django-ninja](index.md): Django の優れた部分を活かし、Pydantic の力と組み合わせたフレームワーク — セキュリティと利便性の交差点における最適な選択肢です。

    2. [django-ninja-crud](django-ninja-crud/index.md): django-ninja をベースに構築された、CRUD インターフェースの開発を簡素化するフレームワーク。宣言的なモデルビューセットとシナリオベースのテスト手法を提供します。

    3. [django-ninja-extra](django-ninja-extra/index.md): 冗長な Django ドキュメントを読み飛ばし、最小限のコードで強力な Web アプリケーションとモダンな API インターフェースを素早く構築できるツールです。

    4. [django-ninja-jwt](django-ninja-jwt/index.md): django-ninja 向けの JSON Web Token プラグイン。認証および関連機能を実装しており、人気の高い Django Rest Framework プラグインからフォークされました。
