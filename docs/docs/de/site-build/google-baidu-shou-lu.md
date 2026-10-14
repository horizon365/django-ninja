---
comments: true
---
# mkdocs-Sites bei Google/Baidu indexieren lassen

Im [vorherigen Artikel](add-google-adsense-with-mkdocs.md) haben wir vorgestellt, wie man Google-Anzeigen über benutzerdefinierte Templates zu mkdocs hinzufügt.

Später stellte ich fest, dass viele Menschen empfahlen, Sites aktiv zur Indexierung durch Google und Baidu einzureichen.

## Google-Indexierung

### Website hinzufügen

Öffnen Sie die Website der Google Search Console: [Google Search Console](https://search.google.com/search-console/welcome?hl=zh-CN)

Sie werden aufgefordert, das Eigentum an der Website zu verifizieren. Hier verwenden wir die HTML-Tag-Methode.

Auf diese Weise müssen Sie, genau wie beim Hinzufügen von Anzeigen im vorherigen Artikel, nur eine Zeile vor `</head>` einfügen und dann veröffentlichen.

### Sitemap

Nach erfolgreicher Verifizierung geben Sie `sitemap.xml` ein, und nach wenigen Minuten sehen Sie nach einem Refresh den Status „Abruf erfolgreich" — damit sind Sie fertig.

Der folgende Code parst die sitemap.xml-Datei dieser Site und ruft alle Dokumentenlinks ab.

## Baidu-Indexierung

### Website hinzufügen

Öffnen Sie die Baidu-Indexierungs-Website: [Baidu Search Resource Platform](https://ziyuan.baidu.com/dailysubmit/index)

Ähnlich wie bei der obigen Google-Verifizierung: Verwenden Sie die HTML-Tag-Verifizierung.

### Sitemap
Wahrscheinlich weil ich die ICP-Registrierungsnummer nicht ausgefüllt habe, ist der Sitemap-Bereich bei mir ausgegraut. Daher habe ich die manuelle Einreichung gewählt. Beachten Sie, dass maximal 20 Einträge pro Tag möglich sind.

Alle Links der Site können über das folgende Skript abgerufen werden.

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

> Referenzartikel:
    1. [Building a Personal Blog Website from Scratch Series](https://www.techxiaofei.com/post/hugo/hugo_search/#%E8%B0%B7%E6%AD%8C%E6%94%B6%E5%BD%95)
  
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
