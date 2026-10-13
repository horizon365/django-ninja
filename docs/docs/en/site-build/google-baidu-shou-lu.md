---
comments: true
---
# Getting mkdocs Sites Indexed by Google/Baidu

In the [previous article](add-google-adsense-with-mkdocs.md), we introduced how to add Google Ads to mkdocs via custom templates.

Later, I found that many people recommended actively submitting sites for indexing by Google and Baidu.

## Google Indexing

### Add a Website

Open the Google Search Console website: [Google Search Console](https://search.google.com/search-console/welcome?hl=zh-CN)

It will prompt you to verify ownership of the website. Here, we use the HTML tag method.

This way, just like adding ads in the previous article, you only need to add a line before `</head>` and then publish.

### Sitemap

After successful verification, enter `sitemap.xml`, and after a few minutes, refresh to see the status as "Fetch successful", which means you are done.

The following code parses this site's sitemap.xml file and retrieves all doc links.

## Baidu Indexing

### Add a Website

Open the Baidu indexing website: [Baidu Search Resource Platform](https://ziyuan.baidu.com/dailysubmit/index)

Similar to the Google verification above, use HTML tag verification.

### Sitemap
Probably because I did not fill in the ICP filing number, the sitemap section is grayed out for me. So I chose manual submission. Note that the maximum is 20 entries per day.

All the site's links can be obtained via the following script.

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
