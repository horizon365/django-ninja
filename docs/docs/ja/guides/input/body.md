---
comments: true
---
# リクエストボディ

リクエストボディは通常、"create" や "update" のオペレーション（POST、PUT、PATCH）で使用されます。
たとえば、POST や PUT でリソースを作成する場合、リクエストボディには作成されるリソースの表現が含まれるのが一般的です。

リクエストボディを宣言するには、**Django Ninja の `Schema`** を使用する必要があります。

!!! note
    内部的には、**Django Ninja** は <a href="https://pydantic.com.cn/" class="external-link" target="_blank">Pydantic</a> Model のすべてのパワーと機能を活用しています。
    Django モデルと一緒に作業するときのコードの混乱を避けるため、`Schema` というエイリアスが選ばれました。Pydantic のモデルクラスはデフォルトで `Model` という名前であり、Django の `Model` クラスと衝突するためです。


## Schema のインポート

まず、`ninja` から `Schema` をインポートする必要があります:

```python hl_lines="2"
{!./src/tutorial/body/code01.py!}
```

## データモデルの作成

次に、`Schema` を継承したクラスとしてデータモデルを宣言します。

すべての属性には標準的な Python 型を使用します:

```python hl_lines="5 6 7 8 9"
{!./src/tutorial/body/code01.py!}
```

注: 属性のデフォルト値を **`None`** に設定すると、その属性はリクエストボディ内でオプションになります。たとえば、上記のモデルは次のような JSON "`object`"（Python の `dict`）を宣言しています:

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...`description` はオプション（デフォルト値が `None`）なので、次の JSON "`object`" も有効です:

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```

## パラメータとして宣言する

*パスオペレーション*に追加するには、パスパラメータやクエリパラメータを宣言するのと同じ方法で宣言します:


```python hl_lines="13"
{!./src/tutorial/body/code01.py!}
```

...そして、その型を作成した `Item` モデルとして宣言します。

## 結果

たったこれだけの Python 型宣言で、**Django Ninja** は次のことを行います:

* リクエストボディを JSON として読み取ります。
* （必要に応じて）適切な型に変換します。
* データをバリデーションします。
    * データが無効な場合、誤りのあるデータの場所と内容を正確に示す、親切で意味のあるエラーを返します。
* 受信したデータをパラメータ `item` で提供します。
    * 関数内でその型を `Item` として宣言したので、すべての属性とその型についてエディタサポート（オートコンプリートなど）も得られます。
* モデルの <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> 定義を生成します。これはプロジェクト内の必要などこでも使用できます。
* これらのスキーマは生成された OpenAPI スキーマの一部となり、自動ドキュメントの <abbr title="User Interfaces">UI</abbr> で使用されます。

## 自動ドキュメント

モデルの JSON Schema は生成された OpenAPI スキーマの一部となり、インタラクティブな API ドキュメントに表示されます:

![Openapi schema](../../img/body-schema-doc.png)

...また、それらを必要とするすべての*パスオペレーション*の API ドキュメントでも使用されます:

![Openapi schema](../../img/body-schema-doc2.png)

## エディタサポート

エディタ内の関数では、あらゆる場所で型ヒントと補完が得られます（`Schema` オブジェクトの代わりに `dict` を使用した場合はこれが起こりません）:

![Type hints](../../img/body-editor.gif)


上記のスクリーンショットは <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a> を使用したものです。

<a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> やその他のほとんどの Python エディタでも同じエディタサポートが得られます。

## リクエストボディ + パスパラメータ

パスパラメータ**と**リクエストボディを同時に宣言できます。


**Django Ninja** は、パスパラメータに一致する関数パラメータは**パスから**取得し、`Schema` で宣言された関数パラメータは**リクエストボディから**取得すべきであると認識します。

```python hl_lines="11 12"
{!./src/tutorial/body/code02.py!}
```

## リクエストボディ + パス + クエリパラメータ

**リクエストボディ**、**パス**、**クエリ**のパラメータを同時に宣言することもできます。

**Django Ninja** はそれぞれのパラメータを認識し、正しい場所からデータを取得します。

```python hl_lines="11 12"
{!./src/tutorial/body/code03.py!}
```

関数パラメータは次のように認識されます:

* パラメータが**パス**でも宣言されている場合、パスパラメータとして使用されます。


* パラメータが**単一の型**（`int`、`float`、`str`、`bool` など）である場合、**クエリ**パラメータとして解釈されます。
* パラメータが **Schema**（または Pydantic の `BaseModel`）型として宣言されている場合、**リクエストボディ**として解釈されます。

!!! done

    次の章に進みましょう！ **[フォームデータ](form-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
