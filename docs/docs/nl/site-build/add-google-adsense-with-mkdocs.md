---
comments: true
---
# Google Adsense toevoegen aan mkdocs-documentatie
Zoek de originele `base.html` in jouw mkdocs-material-versie:

```
✗ python3               
>>> import material
>>> material.__path__
['/opt/homebrew/lib/python3.10/site-packages/material']
```
Schakel in `mkdocs.yml` de functie `overrides` in en maak een nieuwe map aan met de naam `overrides` onder de site-map.
```
theme:
  name: material
  custom_dir: overrides
```

Bestandsstructuur:
```
.
├─ overrides/
│  └─ base.html
└─ mkdocs.yml
```

Bewerk het bestand `template/base.html` onder de hierboven genoemde map `material.__path__` en voeg je adsense-code toe vóór de sectie `</head>`,
```
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4071429194671997"
     crossorigin="anonymous"></script>
  </head>
```
Sla het daarna op als `overides/base.html`.

Controleer ten slotte, na het uitvoeren van het commando `mkdocs build`, of de gegenereerde paginabron de sectie met `adsbygoogle` bevat.

Als alles goed gaat, heeft je mkdocs-site nu Google Adsense geïntegreerd.

Gefeliciteerd!
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
