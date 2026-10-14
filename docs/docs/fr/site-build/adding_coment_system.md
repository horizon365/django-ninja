---
comments: true
---
# Ajouter un système de commentaires gratuit propulsé par les Issues GitHub

Giscus est un module de commentaires propulsé par le système de Discussions de GitHub. Les utilisateurs peuvent se connecter via leur compte GitHub, et il prend en charge les commentaires au format Markdown. L'interface est à la fois épurée et attrayante.

Voyez un exemple en bas de cette page.

Avant de pouvoir utiliser Giscus, vous devez effectuer les étapes suivantes :

## Configurer un dépôt dédié pour Giscus
*    Le dépôt doit être public, sinon les visiteurs ne pourront pas consulter les discussions.
*    L'application giscus doit être installée, sinon les visiteurs ne pourront pas commenter ni répondre. [Cliquez ici pour l'installer](https://github.com/apps/giscus).
*    La fonctionnalité Discussions doit être activée dans votre dépôt. Le chemin pour l'activer est `Settings` - `Features` - `Discussions` du projet.

## Générer votre configuration en ligne
Rendez-vous sur [Giscus](https://giscus.app/) et utilisez leur outil de configuration pour générer l'extrait de code permettant de charger le système de commentaires.
Copiez cet extrait de code pour l'étape suivante. L'extrait généré doit ressembler à ceci.

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
## Configurer comments.html et le placer sous le répertoire overrides/partials
comments.html (vide par défaut) est l'endroit idéal pour ajouter l'extrait de code généré par Giscus.
Suivez le guide d'extension du thème et surchargez comments.html. Remplacez les lignes surlignées par l'extrait de code généré par l'outil de configuration Giscus à l'étape précédente.
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
Structure des fichiers :
```
.
├─ overrides/
│  └─ partials
│     └─ comments.html
│  └─ base.html
└─ mkdocs.yml
```
## Terminé

Vous pouvez désormais activer les commentaires sur une page en définissant `comments` à `true` dans le fichier md :

```markdown
---
comments: true
---

# Page title
...
```


> Documentation officielle : 
> 1. https://squidfunk.github.io/mkdocs-material/setup/adding-a-comment-system/?h=comment
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
