---
comments: true
---
# mkdocs 사이트를 Google/Baidu에 색인시키기

[이전 글](add-google-adsense-with-mkdocs.md)에서 커스텀 템플릿을 통해 mkdocs에 Google 광고를 추가하는 방법을 소개했습니다.

이후 많은 사람들이 Google과 Baidu의 색인을 위해 사이트를 능동적으로 제출할 것을 권장한다는 것을 알게 되었습니다.

## Google 색인

### 웹사이트 추가하기

Google Search Console 웹사이트를 엽니다: [Google Search Console](https://search.google.com/search-console/welcome?hl=zh-CN)

웹사이트의 소유권을 확인하라는 안내가 표시됩니다. 여기서는 HTML 태그 방식을 사용합니다.

이 방식은 이전 글에서 광고를 추가했던 것과 마찬가지로, `</head>` 앞에 한 줄만 추가한 후 게시하면 됩니다.

### Sitemap

소유권 확인이 성공하면 `sitemap.xml`을 입력하고, 몇 분 후에 새로고침하면 상태가 "Fetch successful"로 표시되며, 이제 완료된 것입니다.

다음 코드는 이 사이트의 sitemap.xml 파일을 파싱하여 모든 doc 링크를 가져옵니다.

## Baidu 색인

### 웹사이트 추가하기

Baidu 색인 웹사이트를 엽니다: [Baidu Search Resource Platform](https://ziyuan.baidu.com/dailysubmit/index)

위의 Google 확인과 유사하게, HTML 태그 방식으로 확인을 진행합니다.

### Sitemap
ICP 등록 번호를 입력하지 않아서인지, 저의 경우 sitemap 섹션이 회색으로 비활성화되어 있었습니다. 그래서 수동 제출을 선택했습니다. 하루 최대 20개까지 제출할 수 있다는 점에 유의하세요.

사이트의 모든 링크는 다음 스크립트로 가져올 수 있습니다.

```python
import urllib.request
import xml.etree.ElementTree as ET


def parse_and_save_loc(url, output_file):
    # Fetch the XML data from the online address
    response = urllib.request.urlopen(url)
    data = response.read()

    # Parse the XML
    root = ET.fromstring(data)

    # Extract all loc attributes and save them to a TXT file
    with open(output_file, 'w') as f:
        for element in root.iter():
            if 'loc' in element.tag:
                print(element.text)
                f.write(element.text + '\n')


# Specify the online XML file address and the output TXT file path
url = 'https://django-ninja.cn/sitemap.xml'
output_file = 'urls.txt'

parse_and_save_loc(url, output_file)
```

> 참고 문서:
    1. [Building a Personal Blog Website from Scratch Series](https://www.techxiaofei.com/post/hugo/hugo_search/#%E8%B0%B7%E6%AD%8C%E6%94%B6%E5%BD%95)
  
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
