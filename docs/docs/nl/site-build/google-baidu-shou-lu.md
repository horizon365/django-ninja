---
comments: true
---
# mkdocs-sites laten indexeren door Google/Baidu

In het [vorige artikel](add-google-adsense-with-mkdocs.md) hebben we uitgelegd hoe je via aangepaste templates Google Ads toevoegt aan mkdocs.

Later ontdekte ik dat veel mensen aanbevelden om sites actief aan te melden voor indexering door Google en Baidu.

## Google-indexering

### Website toevoegen

Open de website van Google Search Console: [Google Search Console](https://search.google.com/search-console/welcome?hl=zh-CN)

Je wordt gevraagd om het eigendom van de website te verifiëren. Hier gebruiken we de HTML-tag-methode.

Op deze manier hoef je, net als bij het toevoegen van advertenties in het vorige artikel, slechts één regel toe te voegen vóór `</head>` en vervolgens te publiceren.

### Sitemap

Na een geslaagde verificatie voer je `sitemap.xml` in, en na enkele minuten kun je verversen om de status "Ophalen geslaagd" te zien, wat betekent dat je klaar bent.

De volgende code parseert het sitemap.xml-bestand van deze site en haalt alle documentlinks op.

## Baidu-indexering

### Website toevoegen

Open de website voor Baidu-indexering: [Baidu Search Resource Platform](https://ziyuan.baidu.com/dailysubmit/index)

Vergelijkbaar met de Google-verificatie hierboven, gebruik je HTML-tag-verificatie.

### Sitemap
Waarschijnlijk omdat ik het ICP-registratienummer niet heb ingevuld, is de sitemap-sectie bij mij grijs weergegeven. Daarom heb ik gekozen voor handmatige invoer. Let op: het maximum is 20 invoeren per dag.

Alle links van de site kun je verkrijgen via het volgende script.

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

> Referentieartikelen:
    1. [Building a Personal Blog Website from Scratch Series](https://www.techxiaofei.com/post/hugo/hugo_search/#%E8%B0%B7%E6%AD%8C%E6%94%B6%E5%BD%95)
  
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
