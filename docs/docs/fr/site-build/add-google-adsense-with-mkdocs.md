---
comments: true
---
# Ajouter Google Adsense à une documentation mkdocs
Repérez le fichier `base.html` d'origine dans votre version de mkdocs-material :

```
✗ python3               
>>> import material
>>> material.__path__
['/opt/homebrew/lib/python3.10/site-packages/material']
```
Dans `mkdocs.yml`, activez la fonctionnalité `overrides` et créez un nouveau dossier nommé `overrides` sous le répertoire du site.
```
theme:
  name: material
  custom_dir: overrides
```

Structure des fichiers :
```
.
├─ overrides/
│  └─ base.html
└─ mkdocs.yml
```

Éditez le fichier `template/base.html` sous le répertoire `material.__path__` indiqué ci-dessus, et ajoutez votre code adsense avant la section `</head>`,
```
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4071429194671997"
     crossorigin="anonymous"></script>
  </head>
```
Puis enregistrez-le dans `overides/base.html`.

Enfin, après avoir exécuté la commande `mkdocs build`, vérifiez si le code source de la page générée contient la section liée à `adsbygoogle`.

Si tout se passe bien, votre site mkdocs intègre désormais Google Adsense.

Félicitations !
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
