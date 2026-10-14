---
comments: true
---
# mkdocs Sites को Google/Baidu में Index करवाना

[पिछले article](add-google-adsense-with-mkdocs.md) में, हमने बताया था कि custom templates के ज़रिए mkdocs में Google Ads कैसे जोड़ें।

बाद में, मैंने पाया कि कई लोगों ने सलाह दी कि sites को Google और Baidu में index करवाने के लिए सक्रिय रूप से submit करें।

## Google Indexing

### Website जोड़ें

Google Search Console की website खोलें: [Google Search Console](https://search.google.com/search-console/welcome?hl=zh-CN)

यह आपसे website की ownership verify करने को कहेगा। यहाँ, हम HTML tag method का इस्तेमाल करते हैं।

इस तरह, पिछले article की तरह ads जोड़ने की ही तरह, आपको बस `</head>` से पहले एक line जोड़नी है और फिर publish करना है।

### Sitemap

Verification सफल होने के बाद, `sitemap.xml` enter करें, और कुछ मिनटों के बाद refresh करें — status "Fetch successful" दिखेगा, जिसका मतलब है कि आपका काम पूरा हो गया।

निम्नलिखित code इस site की sitemap.xml file को parse करता है और सभी doc links निकालता है।

## Baidu Indexing

### Website जोड़ें

Baidu indexing की website खोलें: [Baidu Search Resource Platform](https://ziyuan.baidu.com/dailysubmit/index)

ऊपर वाले Google verification की तरह ही, HTML tag verification का इस्तेमाल करें।

### Sitemap
शायद इसलिए कि मैंने ICP filing number नहीं भरा था, मेरे लिए sitemap section grayed out है। इसलिए मैंने manual submission चुनी। ध्यान दें कि अधिकतम 20 entries प्रति दिन हो सकती हैं।

Site के सभी links निम्नलिखित script के ज़रिए प्राप्त किए जा सकते हैं।

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

> Reference articles:
    1. [Building a Personal Blog Website from Scratch Series](https://www.techxiaofei.com/post/hugo/hugo_search/#%E8%B0%B7%E6%AD%8C%E6%94%B6%E5%BD%95)
  
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
