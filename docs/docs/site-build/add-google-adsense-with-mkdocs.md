---
comments: true
---
# 添加 Google Adsense 到 mkdocs 文档中
在您的 mkdocs-material 版本中找到原始的 `base.html`：

```
✗ python3               
>>> import material
>>> material.__path__
['/opt/homebrew/lib/python3.10/site-packages/material']
```
在 `mkdocs.yml` 中，开启`overrides`功能，并在站点目录下，新建文件夹 `overrides`。
```
theme:
  name: material
  custom_dir: overrides
```

文件结构：
```
.
├─ overrides/
│  └─ base.html
└─ mkdocs.yml
```

编辑上面的 `material.__path__` 目录下的 `template/base.html`文件， 在 `</head>` 部分的前面添加您的adsense代码，
```
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4071429194671997"
     crossorigin="anonymous"></script>
  </head>
```
然后将其保存到 `overides/base.html`。

最后使用 `mkdocs build` 命令后，检查生成的网页源码中是否包含 `adsbygoogle` 相关部分。

不出意料的话，现在你的 mkdocs 站点已经集成了 Google Adsense。

恭喜！