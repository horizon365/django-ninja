---
comments: true
---
# GitHub Issues 기반의 무료 댓글 시스템 추가하기

Giscus는 GitHub의 Discussion 시스템으로 구동되는 댓글 모듈입니다. 사용자는 GitHub 계정으로 로그인할 수 있으며, Markdown 형식의 댓글을 지원합니다. 인터페이스는 깔끔하고 매력적입니다.

예시는 이 페이지 하단을 참조하세요.

Giscus를 사용하기 전에 다음 단계를 완료해야 합니다:

## Giscus 전용 리포지토리 구성하기
*    리포지토리는 반드시 public이어야 합니다. 그렇지 않으면 방문자가 discussion을 볼 수 없습니다.
*    giscus 앱이 설치되어 있어야 합니다. 그렇지 않으면 방문자가 댓글을 달거나 응답할 수 없습니다. [여기를 클릭하여 설치](https://github.com/apps/giscus).
*    리포지토리에서 Discussions 기능이 활성화되어 있어야 합니다. 활성화 경로는 프로젝트의 `Settings` - `Features` - `Discussions`입니다.

## 온라인에서 자신만의 설정 생성하기
[Giscus](https://giscus.app/)에 방문하여 설정 도구를 사용해 댓글 시스템을 로드하는 코드 스니펫을 생성합니다.
해당 코드 스니펫을 복사해 다음 단계를 위해 준비해 둡니다. 생성된 스니펫은 대략 다음과 같이 생겼습니다.

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
## comments.html 구성 후 overrides/partials 디렉터리 아래에 배치하기
comments.html (기본적으로 비어 있음)은 Giscus가 생성한 코드 스니펫을 추가하기 가장 좋은 위치입니다.
테마 확장 가이드를 따라 comments.html을 오버라이드하세요. 강조된 줄을 이전 단계에서 Giscus 설정 도구가 생성한 코드 스니펫으로 교체합니다.
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
파일 구조:
```
.
├─ overrides/
│  └─ partials
│     └─ comments.html
│  └─ base.html
└─ mkdocs.yml
```
## 완료

이제 md 파일에서 `comments`를 `true`로 설정하여 페이지에서 댓글을 활성화할 수 있습니다:

```markdown
---
comments: true
---

# Page title
...


> 공식 문서: 
> 1. https://squidfunk.github.io/mkdocs-material/setup/adding-a-comment-system/?h=comment
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">

