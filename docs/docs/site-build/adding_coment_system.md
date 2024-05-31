---
comments: true
---
# 增加依托于 github issue 的免费评论系统

Giscus 是一个依托于 GitHub Discussion 系统的评论模块，用户可以通过 GitHub 账号登陆，还支持 markdown 格式的评论，界面既简洁又好看。

例子可以参见本页面的最底部。

在你可以使用 Giscus 之前，你需要完成以下步骤：

## 配置 giscus 专用仓库
*    该仓库是公开的，否则访客将无法查看 discussion。
*    giscus app 已安装，否则访客将无法评论和回应。 [点此安装](https://github.com/apps/giscus)。
*    Discussions 功能已在你的仓库中启用。启用路径为项目的 `Settings` - `Features` - `Discussions`。

## 在线生成自己的专用配置
访问 [Giscus](https://giscus.app/) 并通过他们的配置工具生成代码片段以加载评论系统。
复制该代码片段用于下一步。生成的代码片段应该看起来与此类似。

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
## 配置 comments.html，并放到 overrides/partials 目录下
comments.html（默认情况下为空）是添加 Giscus 生成的代码片段的最佳位置。
遵循主题扩展指南并用 覆盖 comments.html。用你在上一步中使用 Giscus 配置工具生成的代码片段替换突出显示的行。
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
文件结构：
```
.
├─ overrides/
│  └─ partials
│     └─ comments.html
│  └─ base.html
└─ mkdocs.yml
```
## 大功告成

现在你可以通过在 md 文件中将 comments 设置为 true 来在页面上启用评论：

```markdown
---
comments: true
---

# Page title
...
```


> 官方文档： 
> 1. https://squidfunk.github.io/mkdocs-material/setup/adding-a-comment-system/?h=comment