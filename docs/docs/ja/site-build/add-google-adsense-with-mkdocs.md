---
comments: true
---
# mkdocs ドキュメントに Google Adsense を追加する
お使いの mkdocs-material バージョンにある元の `base.html` を探します：

```
✗ python3               
>>> import material
>>> material.__path__
['/opt/homebrew/lib/python3.10/site-packages/material']
```
`mkdocs.yml` で `overrides` 機能を有効にし、サイトディレクトリの下に `overrides` という名前の新しいフォルダーを作成します。
```
theme:
  name: material
  custom_dir: overrides
```

ファイル構成：
```
.
├─ overrides/
│  └─ base.html
└─ mkdocs.yml
```

上記の `material.__path__` ディレクトリにある `template/base.html` ファイルを編集し、`</head>` セクションの前に adsense コードを追加します。
```
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4071429194671997"
     crossorigin="anonymous"></script>
  </head>
```
それを `overides/base.html` として保存します。

最後に、`mkdocs build` コマンドを実行した後、生成されたページのソースに `adsbygoogle` 関連のセクションが含まれているか確認します。

すべてうまくいけば、あなたの mkdocs サイトに Google Adsense が統合されました。

おめでとうございます！
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
