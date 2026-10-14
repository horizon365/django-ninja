---
comments: true
---
# mkdocs Documentation में Google Adsense जोड़ना
अपने mkdocs-material version में मूल `base.html` ढूँढें:

```
✗ python3               
>>> import material
>>> material.__path__
['/opt/homebrew/lib/python3.10/site-packages/material']
```
`mkdocs.yml` में, `overrides` feature को enable करें, और site directory के अंतर्गत `overrides` नाम का एक नया folder बनाएँ।
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

ऊपर वाली `material.__path__` directory के अंतर्गत `template/base.html` file को edit करें, और `</head>` section से पहले अपना adsense code जोड़ें,
```
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4071429194671997"
     crossorigin="anonymous"></script>
  </head>
```
फिर इसे `overides/base.html` में save करें।

अंत में, `mkdocs build` command चलाने के बाद, check करें कि generated page source में `adsbygoogle` से संबंधित section है या नहीं।

अगर सब ठीक रहा, तो अब आपकी mkdocs site में Google Adsense integrate हो गया है।

बधाई हो!
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
