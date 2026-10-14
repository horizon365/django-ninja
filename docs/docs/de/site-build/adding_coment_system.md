---
comments: true
---
# Ein kostenloses Kommentarsystem auf Basis von GitHub Issues hinzufügen

Giscus ist ein Kommentarmodul, das auf dem Discussion-System von GitHub basiert. Benutzer können sich über ihr GitHub-Konto einloggen, und es unterstützt Kommentare im Markdown-Format. Die Oberfläche ist sowohl aufgeräumt als auch ansprechend.

Ein Beispiel finden Sie am Ende dieser Seite.

Bevor Sie Giscus verwenden können, müssen Sie die folgenden Schritte ausführen:

## Ein eigenes Repository für Giscus konfigurieren
*    Das Repository muss öffentlich sein, sonst können Besucher die Diskussionen nicht sehen.
*    Die Giscus-App muss installiert sein, sonst können Besucher nicht kommentieren oder antworten. [Klicken Sie hier zur Installation](https://github.com/apps/giscus).
*    Die Discussions-Funktion muss in Ihrem Repository aktiviert sein. Der Pfad zur Aktivierung lautet `Settings` - `Features` - `Discussions` des Projekts.

## Ihre Konfiguration online generieren
Besuchen Sie [Giscus](https://giscus.app/) und verwenden Sie deren Konfigurationstool, um den Codeausschnitt zum Laden des Kommentarsystems zu generieren.
Kopieren Sie diesen Codeausschnitt für den nächsten Schritt. Der generierte Ausschnitt sollte etwa so aussehen.

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
## comments.html konfigurieren und unter dem Verzeichnis overrides/partials ablegen
comments.html (standardmäßig leer) ist der beste Ort, um den von Giscus generierten Codeausschnitt einzufügen.
Folgen Sie der Anleitung zur Theme-Erweiterung und überschreiben Sie comments.html. Ersetzen Sie die hervorgehobenen Zeilen durch den Codeausschnitt, der im vorherigen Schritt vom Giscus-Konfigurationstool generiert wurde.
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
Dateistruktur:
```
.
├─ overrides/
│  └─ partials
│     └─ comments.html
│  └─ base.html
└─ mkdocs.yml
```
## Fertig

Jetzt können Sie Kommentare auf einer Seite aktivieren, indem Sie in der md-Datei `comments` auf `true` setzen:

```markdown
---
comments: true
---

# Page title
...
```


> Offizielle Dokumentation: 
> 1. https://squidfunk.github.io/mkdocs-material/setup/adding-a-comment-system/?h=comment
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
