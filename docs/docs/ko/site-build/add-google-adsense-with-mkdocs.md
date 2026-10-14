---
comments: true
---
# mkdocs 문서에 Google Adsense 추가하기
사용 중인 mkdocs-material 버전에서 원본 `base.html`을 찾습니다:

```
✗ python3               
>>> import material
>>> material.__path__
['/opt/homebrew/lib/python3.10/site-packages/material']
```
`mkdocs.yml`에서 `overrides` 기능을 활성화하고, 사이트 디렉터리 아래에 `overrides`라는 이름의 새 폴더를 만듭니다.
```
theme:
  name: material
  custom_dir: overrides
```

파일 구조:
```
.
├─ overrides/
│  └─ base.html
└─ mkdocs.yml
```

위의 `material.__path__` 디렉터리 아래에서 `template/base.html` 파일을 편집하고, `</head>` 섹션 앞에 adsense 코드를 추가합니다,
```
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4071429194671997"
     crossorigin="anonymous"></script>
  </head>
```
그런 다음 `overides/base.html`로 저장합니다.

마지막으로, `mkdocs build` 명령을 실행한 후 생성된 페이지 소스에 `adsbygoogle` 관련 섹션이 포함되어 있는지 확인합니다.

모든 것이 순조롭게 진행되었다면, 여러분의 mkdocs 사이트에 Google Adsense가 통합된 것입니다.

축하합니다!
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
