---
comments: true
---
# Google Adsense zur mkdocs-Dokumentation hinzufügen
Finden Sie die originale `base.html` in Ihrer mkdocs-material-Version:

```
✗ python3               
>>> import material
>>> material.__path__
['/opt/homebrew/lib/python3.10/site-packages/material']
```
Aktivieren Sie in `mkdocs.yml` die Funktion `overrides` und erstellen Sie einen neuen Ordner namens `overrides` unter dem Site-Verzeichnis.
```
theme:
  name: material
  custom_dir: overrides
```

Dateistruktur:
```
.
├─ overrides/
│  └─ base.html
└─ mkdocs.yml
```

Bearbeiten Sie die Datei `template/base.html` unter dem oben genannten Verzeichnis `material.__path__` und fügen Sie Ihren Adsense-Code vor dem Abschnitt `</head>` ein,
```
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4071429194671997"
     crossorigin="anonymous"></script>
  </head>
```
Dann speichern Sie sie unter `overides/base.html`.

Führen Sie abschließend den Befehl `mkdocs build` aus und prüfen Sie, ob der generierte Seitenquelltext den Abschnitt mit `adsbygoogle` enthält.

Wenn alles gut geht, hat Ihre mkdocs-Site nun Google Adsense integriert.

Herzlichen Glückwunsch!
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
