---
comments: true
---
# フォームデータ

**Django Ninja** は、`request.POST` データ（つまり `application/x-www-form-urlencoded` や `multipart/form-data`）のパースとバリデーションも行えます。

## パラメータとしてのフォームデータ

```python hl_lines="1 4"
from ninja import NinjaAPI, Form

@api.post("/login")
def login(request, username: Form[str], password: Form[str]):
    return {'username': username, 'password': '*****'}
```

以下の点に注意してください:

1) `ninja` から `Form` クラスをインポートする必要があります
```python
from ninja import Form
```

2) パラメータのデフォルト値として `Form` を使用します:
```python
username: Form[str]
```

## Schema の使用

[リクエストボディ](body.md#declare-it-as-a-parameter)と同様に、スキーマを使用してパラメータを整理できます。

```python hl_lines="12"
{!./src/tutorial/form/code01.py!}
```

## リクエストフォーム + パス + クエリパラメータ

[リクエストボディ](body.md#request-body-path-query-parameters)と同様に、フォームデータを他のパラメータソースと組み合わせることができます。

クエリパラメータ**と**パスパラメータ**と**フォームフィールド**などを**同時に宣言できます。

**Django Ninja** は、パスパラメータに一致する関数パラメータは**パスから**取得し、`Form(...)` で宣言された関数パラメータは**リクエストのフォームフィールドから**取得する、といった認識を行います。

```python hl_lines="12"
{!./src/tutorial/form/code02.py!}
```
## 空のフォームフィールドのデフォルト値へのマッピング

オプションのフォームフィールドは、空の値と共に送信されることがよくあります。この値は空文字列として解釈されるため、`int` や `bool` などのフィールドではバリデーションに失敗する可能性があります。

Pydantic のドキュメントで説明されているように、これは[ジェネリッククラスを型として使用する](https://pydantic.com.cn/usage/types/#generic-classes-as-types)ことで解決できます。

```python hl_lines="15 16 23-25"
{!./src/tutorial/form/code03.py!}
```

!!! done

    次の章に進みましょう！ **[ファイルアップロード](file-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
