---
comments: true
---
# Добавление Google Adsense в документацию mkdocs
Найдите оригинальный `base.html` в вашей версии mkdocs-material:

```
✗ python3               
>>> import material
>>> material.__path__
['/opt/homebrew/lib/python3.10/site-packages/material']
```
В `mkdocs.yml` включите возможность `overrides` и создайте новую папку с именем `overrides` в каталоге сайта.
```
theme:
  name: material
  custom_dir: overrides
```

Структура файлов:
```
.
├─ overrides/
│  └─ base.html
└─ mkdocs.yml
```

Отредактируйте файл `template/base.html` в каталоге `material.__path__`, указанном выше, и добавьте ваш код adsense перед секцией `</head>`,
```
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4071429194671997"
     crossorigin="anonymous"></script>
  </head>
```
Затем сохраните его в `overides/base.html`.

Наконец, после выполнения команды `mkdocs build` проверьте, содержит ли исходный код сгенерированной страницы секцию, относящуюся к `adsbygoogle`.

Если всё прошло успешно, ваш сайт mkdocs теперь интегрирован с Google Adsense.

Поздравляю!
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
