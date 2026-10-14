---
comments: true
---
# Een gratis reactiesysteem toevoegen op basis van GitHub Issues

Giscus is een reactiemodule die draait op het Discussion-systeem van GitHub. Gebruikers kunnen inloggen via hun GitHub-account, en het ondersteunt opgemaakte opmerkingen in Markdown. De interface is zowel overzichtelijk als aantrekkelijk.

Zie onderaan deze pagina voor een voorbeeld.

Voordat je Giscus kunt gebruiken, moet je de volgende stappen uitvoeren:

## Stel een speciale repository in voor Giscus
*    De repository moet openbaar zijn, anders kunnen bezoekers de discussies niet bekijken.
*    De giscus-app moet geïnstalleerd zijn, anders kunnen bezoekers niet reageren of antwoorden. [Klik hier om te installeren](https://github.com/apps/giscus).
*    De functie Discussions moet in je repository zijn ingeschakeld. Het pad om dit in te schakelen is `Settings` - `Features` - `Discussions` van het project.

## Genereer je eigen configuratie online
Bezoek [Giscus](https://giscus.app/) en gebruik hun configuratietool om het codefragment te genereren waarmee het reactiesysteem wordt geladen.
Kopieer dat codefragment voor de volgende stap. Het gegenereerde fragment zou er ongeveer zo uit moeten zien.

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
## Configureer comments.html en plaats het onder de map overrides/partials
comments.html (standaard leeg) is de beste plek om het codefragment toe te voegen dat door Giscus is gegenereerd.
Volg de handleiding voor thema-extensies en overschrijf comments.html. Vervang de gemarkeerde regels door het codefragment dat in de vorige stap door de Giscus-configuratietool is gegenereerd.
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
Bestandsstructuur:
```
.
├─ overrides/
│  └─ partials
│     └─ comments.html
│  └─ base.html
└─ mkdocs.yml
```
## Klaar

Nu kun je opmerkingen op een pagina inschakelen door in het md-bestand `comments` op `true` te zetten:

```markdown
---
comments: true
---

# Page title
...
```


> Officiële documentatie: 
> 1. https://squidfunk.github.io/mkdocs-material/setup/adding-a-comment-system/?h=comment
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
