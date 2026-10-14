---
comments: true
---
# Faire indexer les sites mkdocs par Google/Baidu

Dans [l'article précédent](add-google-adsense-with-mkdocs.md), nous avons vu comment ajouter des annonces Google à mkdocs via des modèles personnalisés.

Plus tard, j'ai constaté que beaucoup de gens recommandaient de soumettre activement les sites à l'indexation de Google et Baidu.

## Indexation Google

### Ajouter un site

Ouvrez le site Google Search Console : [Google Search Console](https://search.google.com/search-console/welcome?hl=zh-CN)

Il vous demandera de vérifier la propriété du site. Ici, nous utilisons la méthode de la balise HTML.

De cette façon, comme pour l'ajout d'annonces dans l'article précédent, il vous suffit d'ajouter une ligne avant `</head>` puis de publier.

### Sitemap

Une fois la vérification réussie, saisissez `sitemap.xml`, et après quelques minutes, actualisez pour voir le statut « récupération réussie », ce qui signifie que c'est terminé.

Le code suivant analyse le fichier sitemap.xml de ce site et récupère tous les liens de documentation.

## Indexation Baidu

### Ajouter un site

Ouvrez le site d'indexation Baidu : [Baidu Search Resource Platform](https://ziyuan.baidu.com/dailysubmit/index)

Semblable à la vérification Google ci-dessus, utilisez la vérification par balise HTML.

### Sitemap
Probablement parce que je n'ai pas renseigné le numéro d'enregistrement ICP, la section sitemap est grisée pour moi. J'ai donc choisi la soumission manuelle. Notez que le maximum est de 20 entrées par jour.

Tous les liens du site peuvent être obtenus via le script suivant.

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

> Articles de référence :
    1. [Building a Personal Blog Website from Scratch Series](https://www.techxiaofei.com/post/hugo/hugo_search/#%E8%B0%B7%E6%AD%8C%E6%94%B6%E5%BD%95)
  
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
