---
comments: true
---
# Индексация сайтов mkdocs в Google/Baidu

В [предыдущей статье](add-google-adsense-with-mkdocs.md) мы рассмотрели, как добавить рекламу Google в mkdocs с помощью пользовательских шаблонов.

Позже я обнаружил, что многие рекомендуют активно отправлять сайты на индексацию в Google и Baidu.

## Индексация в Google

### Добавьте сайт

Откройте сайт Google Search Console: [Google Search Console](https://search.google.com/search-console/welcome?hl=zh-CN)

Вам предложат подтвердить право собственности на сайт. Здесь мы используем метод HTML-тега.

Таким образом, как и при добавлении рекламы в предыдущей статье, вам нужно лишь добавить одну строку перед `</head>` и затем опубликовать.

### Sitemap

После успешной проверки введите `sitemap.xml`, и через несколько минут обновите страницу, чтобы увидеть статус «Получение выполнено успешно» — это значит, что всё готово.

Следующий код разбирает файл sitemap.xml этого сайта и извлекает все ссылки на документы.

## Индексация в Baidu

### Добавьте сайт

Откройте сайт индексации Baidu: [Baidu Search Resource Platform](https://ziyuan.baidu.com/dailysubmit/index)

Аналогично проверке Google выше, используйте проверку через HTML-тег.

### Sitemap
Вероятно, потому что я не указал номер ICP-регистрации, секция sitemap для меня неактивна (выделена серым). Поэтому я выбрал ручную отправку. Обратите внимание, что максимум — 20 записей в день.

Все ссылки сайта можно получить с помощью следующего скрипта.

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

> Полезные статьи:
    1. [Building a Personal Blog Website from Scratch Series](https://www.techxiaofei.com/post/hugo/hugo_search/#%E8%B0%B7%E6%AD%8C%E6%94%B6%E5%BD%95)
  
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
