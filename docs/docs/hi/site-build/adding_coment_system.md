---
comments: true
---
# GitHub Issues पर आधारित एक Free Comment System जोड़ना

Giscus, GitHub के Discussion system द्वारा संचालित एक comment module है। Users अपने GitHub account से log in कर सकते हैं, और यह Markdown format में comments को support करता है। इसका interface साफ-सुथरा और आकर्षक दोनों है।

उदाहरण के लिए इस page का निचला हिस्सा देखें।

Giscus का इस्तेमाल करने से पहले, आपको निम्नलिखित steps पूरे करने होंगे:

## Giscus के लिए एक Dedicated Repository configure करें
*    Repository public होना चाहिए, अन्यथा visitors discussions नहीं देख पाएँगे।
*    Giscus app install होना चाहिए, अन्यथा visitors comment या respond नहीं कर पाएँगे। [Install करने के लिए यहाँ click करें](https://github.com/apps/giscus)।
*    आपके repository में Discussions feature enable होना चाहिए। इसे enable करने का path project के `Settings` - `Features` - `Discussions` में है।

## Online अपना Configuration generate करें
[Giscus](https://giscus.app/) पर जाएँ और उनके configuration tool का इस्तेमाल करके comment system load करने के लिए code snippet generate करें।
अगले step के लिए उस code snippet को copy कर लें। Generated snippet कुछ ऐसा दिखना चाहिए।

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
## comments.html configure करें और उसे overrides/partials directory के अंतर्गत रखें
comments.html (डिफ़ॉल्ट रूप से खाली) Giscus द्वारा generate किए गए code snippet को जोड़ने की सबसे अच्छी जगह है।
Theme extension guide का पालन करें और comments.html को override करें। Highlighted lines को पिछले step में Giscus configuration tool द्वारा generate किए गए code snippet से बदलें।
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
File structure:
```
.
├─ overrides/
│  └─ partials
│     └─ comments.html
│  └─ base.html
└─ mkdocs.yml
```
## पूरा हुआ

अब आप md file में `comments` को `true` set करके किसी page पर comments enable कर सकते हैं:

```markdown
---
comments: true
---

# Page title
...


> आधिकारिक documentation: 
> 1. https://squidfunk.github.io/mkdocs-material/setup/adding-a-comment-system/?h=comment
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
