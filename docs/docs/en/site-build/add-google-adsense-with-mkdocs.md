---
comments: true
---
# Adding Google Adsense to mkdocs Documentation
Find the original `base.html` in your mkdocs-material version:

```
✗ python3               
>>> import material
>>> material.__path__
['/opt/homebrew/lib/python3.10/site-packages/material']
```
In `mkdocs.yml`, enable the `overrides` feature, and create a new folder named `overrides` under the site directory.
```
theme:
  name: material
  custom_dir: overrides
```

File structure:
```
.
├─ overrides/
│  └─ base.html
└─ mkdocs.yml
```

Edit the `template/base.html` file under the `material.__path__` directory above, and add your adsense code before the `</head>` section,
```
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4071429194671997"
     crossorigin="anonymous"></script>
  </head>
```
Then save it to `overides/base.html`.

Finally, after running the `mkdocs build` command, check whether the generated page source contains the `adsbygoogle` related section.

If all goes well, your mkdocs site has now integrated Google Adsense.

Congratulations!
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
