---
comments: true
---
# Добавление бесплатной системы комментариев на основе GitHub Issues

Giscus — это модуль комментариев, работающий на основе системы Discussion в GitHub. Пользователи могут входить через свою учётную запись GitHub, поддерживаются комментарии в формате Markdown. Интерфейс одновременно лаконичный и привлекательный.

Пример можно увидеть внизу этой страницы.

Прежде чем использовать Giscus, необходимо выполнить следующие шаги:

## Настройте выделенный репозиторий для Giscus
*    Репозиторий должен быть публичным, иначе посетители не смогут просматривать обсуждения.
*    Должно быть установлено приложение giscus, иначе посетители не смогут комментировать и отвечать. [Нажмите здесь, чтобы установить](https://github.com/apps/giscus).
*    В вашем репозитории должна быть включена функция Discussions. Путь для включения: `Settings` - `Features` - `Discussions` проекта.

## Сгенерируйте свою конфигурацию онлайн
Посетите [Giscus](https://giscus.app/) и используйте их инструмент конфигурации, чтобы сгенерировать фрагмент кода для загрузки системы комментариев.
Скопируйте этот фрагмент кода для следующего шага. Сгенерированный фрагмент должен выглядеть примерно так.

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
## Настройте comments.html и поместите его в каталог overrides/partials
comments.html (по умолчанию пустой) — лучшее место для добавления фрагмента кода, сгенерированного Giscus.
Следуя руководству по расширению темы, переопределите comments.html. Замените выделенные строки фрагментом кода, сгенерированным инструментом конфигурации Giscus на предыдущем шаге.
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
Структура файлов:
```
.
├─ overrides/
│  └─ partials
│     └─ comments.html
│  └─ base.html
└─ mkdocs.yml
```
## Готово

Теперь вы можете включить комментарии на странице, установив `comments` в `true` в md-файле:

```markdown
---
comments: true
---

# Page title
...
```


> Официальная документация: 
> 1. https://squidfunk.github.io/mkdocs-material/setup/adding-a-comment-system/?h=comment
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
