---
comments: true
---
# GitHub Issues を活用した無料コメントシステムの追加

Giscus は GitHub の Discussion システムを利用したコメントモジュールです。ユーザーは GitHub アカウントでログインでき、Markdown 形式のコメントに対応しています。インターフェースはすっきりしていて見た目も魅力的です。

例はこのページの下部をご覧ください。

Giscus を使えるようにするには、まず次の手順を完了する必要があります：

## Giscus 専用のリポジトリを設定する
*    リポジトリは公開（public）である必要があります。そうでないとビジターはディスカッションを閲覧できません。
*    giscus アプリをインストールする必要があります。そうでないとビジターはコメントや返信ができません。[ここをクリックしてインストール](https://github.com/apps/giscus)。
*    リポジトリで Discussions 機能が有効になっている必要があります。有効化のパスはプロジェクトの `Settings` - `Features` - `Discussions` です。

## オンラインで自分の設定を生成する
[Giscus](https://giscus.app/) にアクセスし、設定ツールを使ってコメントシステムを読み込むコードスニペットを生成します。
そのコードスニペットをコピーして、次のステップに備えてください。生成されるスニペットは次のようなものになります。

```javascript
<script
  src="https://giscus.app/client.js"
  data-repo="<username>/<repository>"
  data-repo-id="..."
  data-category="..."
  data-category-id="..."
  data-mapping="pathname"
  data-reactions-enabled="1"
  data-emit-metadata="1"
  data-theme="light"
  data-lang="en"
  crossorigin="anonymous"
  async
>
</script>
```
## comments.html を設定し、overrides/partials ディレクトリの下に配置する
comments.html（デフォルトでは空）は、Giscus が生成したコードスニペットを追加するのに最適な場所です。
テーマ拡張ガイドに従って comments.html をオーバーライドしてください。ハイライトされた行を、前のステップで Giscus の設定ツールが生成したコードスニペットに置き換えます。
```hl_lines="3-17"
{% if page.meta.comments %}
  <h2 id="__comments">{{ lang.t("meta.comments") }}</h2>
  <script
      src="https://giscus.app/client.js"
      data-repo="<username>/<repository>"
      data-repo-id="..."
      data-category="..."
      data-category-id="..."
      data-mapping="pathname"
      data-reactions-enabled="1"
      data-emit-metadata="1"
      data-theme="light"
      data-lang="en"
      crossorigin="anonymous"
      async
    >
    </script>

  <!-- Synchronize Giscus theme with palette -->
  <script>
    var giscus = document.querySelector("script[src*=giscus]")

    // Set palette on initial load
    var palette = __md_get("__palette")
    if (palette && typeof palette.color === "object") {
      var theme = palette.color.scheme === "slate"
        ? "transparent_dark"
        : "light"

      // Instruct Giscus to set theme
      giscus.setAttribute("data-theme", theme) 
    }

    // Register event handlers after documented loaded
    document.addEventListener("DOMContentLoaded", function() {
      var ref = document.querySelector("[data-md-component=palette]")
      ref.addEventListener("change", function() {
        var palette = __md_get("__palette")
        if (palette && typeof palette.color === "object") {
          var theme = palette.color.scheme === "slate"
            ? "transparent_dark"
            : "light"

          // Instruct Giscus to change theme
          var frame = document.querySelector(".giscus-frame")
          frame.contentWindow.postMessage(
            { giscus: { setConfig: { theme } } },
            "https://giscus.app"
          )
        }
      })
    })
  </script>
{% endif %}
```
ファイル構成：
```
.
├─ overrides/
│  └─ partials
│     └─ comments.html
│  └─ base.html
└─ mkdocs.yml
```
## 完成

これで、md ファイルで `comments` を `true` に設定することで、ページのコメントを有効にできます：

```markdown
---
comments: true
---

# Page title
...
```


> 公式ドキュメント： 
> 1. https://squidfunk.github.io/mkdocs-material/setup/adding-a-comment-system/?h=comment
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
