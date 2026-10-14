
Ninja JWT の開発作業を行うには、Github 上で自分のフォークを作成し、ローカルにクローンし、そのための仮想環境を作成して有効化したうえで、プロジェクトディレクトリ内で作業します：

その後、flit をインストールします

```shell
$(venv) pip install flit
```

コードのリントとスタイルに使われる開発用ライブラリと pre-commit フックをインストールします

```shell
$(venv) make install
```

テストを実行するには：

```shell
$(venv) make test
```

カバレッジ付きでテストを実行するには：

```shell
$(venv) make test-cov
```

!!! success

    これでチュートリアルは終わりです！

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
