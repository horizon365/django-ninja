---
comments: true
---
# Corps de la requête

Le corps de la requête est généralement utilisé avec les opérations de « création » et de « mise à jour » (POST, PUT, PATCH).
Par exemple, lors de la création d'une ressource avec POST ou PUT, le corps de la requête contient généralement une représentation de la ressource à créer.

Pour déclarer un corps de requête, vous devez utiliser **le `Schema` de Django Ninja**.

!!! note
    Sous le capot, **Django Ninja** exploite toute la puissance et les fonctionnalités du Model <a href="https://pydantic.com.cn/" class="external-link" target="_blank">Pydantic</a>.
    L'alias `Schema` a été choisi pour éviter toute confusion dans le code lors de la manipulation des models Django, puisque la classe de model de Pydantic est nommée `Model` par défaut, ce qui entre en conflit avec la classe `Model` de Django.


## Importation du Schema

Tout d'abord, vous devez importer `Schema` depuis `ninja` :

```python hl_lines="2"
{!./src/tutorial/body/code01.py!}
```

## Création de votre modèle de données

Déclarez ensuite votre modèle de données comme une classe qui hérite de `Schema`.

Utilisez les types Python standard pour tous les attributs :

```python hl_lines="5 6 7 8 9"
{!./src/tutorial/body/code01.py!}
```

Remarque : si vous définissez la valeur par défaut d'un attribut sur **`None`**, il devient optionnel dans le corps de la requête. Par exemple, le modèle ci-dessus déclare un « `object` » JSON (ou un `dict` Python) comme ceci :

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...puisque `description` est optionnel (sa valeur par défaut est `None`), ce « `object` » JSON sera également valide :

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```

## Déclaration en tant que paramètre

Pour l'ajouter à votre *opération de chemin* (path operation), déclarez-le de la même manière que vous déclarez les paramètres de chemin et de requête :


```python hl_lines="13"
{!./src/tutorial/body/code01.py!}
```

... et déclarez son type comme le modèle `Item` que vous avez créé.

## Résultat

Avec cette simple déclaration de type Python, **Django Ninja** va :

* Lire le corps de la requête en tant que JSON.
* Convertir vers les types appropriés (si nécessaire).
* Valider les données.
    * Si les données sont invalides, il renverra une erreur conviviale et explicite qui indique précisément l'emplacement et le contenu des données erronées.
* Vous fournir les données reçues dans le paramètre `item`.
    * Comme vous avez déclaré son type comme `Item` dans la fonction, vous bénéficierez également de la prise en charge par l'éditeur (autocomplétion, etc.) pour tous les attributs et leurs types.
* Générer les définitions <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> pour votre modèle, que vous pourrez également utiliser partout où vous en aurez besoin dans votre projet.
* Ces schémas feront partie du schéma OpenAPI généré et seront utilisés par la documentation automatique <abbr title="User Interfaces">UI</abbr>.

## Documentation automatique

Les JSON Schemas de vos modèles feront partie de votre schéma OpenAPI généré et seront affichés dans la documentation interactive de l'API :

![Openapi schema](../../img/body-schema-doc.png)

...et ils seront également utilisés dans la documentation de l'API pour chaque *opération de chemin* qui les requiert :

![Openapi schema](../../img/body-schema-doc2.png)

## Prise en charge par l'éditeur

Dans votre éditeur, à l'intérieur de votre fonction, vous obtiendrez des indications de type et une complétion omniprésentes (cela n'arrivera pas si vous utilisez un `dict` au lieu d'un objet Schema) :

![Type hints](../../img/body-editor.gif)


Les captures d'écran précédentes utilisent <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>.

Vous obtiendrez la même prise en charge par l'éditeur dans <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> et la plupart des autres éditeurs Python.

## Corps de la requête + Paramètres de chemin

Vous pouvez déclarer des paramètres de chemin **et** un corps de requête en même temps.


**Django Ninja** reconnaîtra que les paramètres de fonction correspondant aux paramètres de chemin doivent être pris **du chemin**, tandis que les paramètres de fonction déclarés avec `Schema` doivent être pris **du corps de la requête**.

```python hl_lines="11 12"
{!./src/tutorial/body/code02.py!}
```

## Corps de la requête + Chemin + Paramètres de requête

Vous pouvez également déclarer en même temps des paramètres de **corps de requête**, de **chemin** et de **requête**.

**Django Ninja** reconnaîtra chaque paramètre et prendra les données à l'emplacement correct.

```python hl_lines="11 12"
{!./src/tutorial/body/code03.py!}
```

Les paramètres de fonction seront reconnus comme suit :

* Si le paramètre est également déclaré dans le **chemin**, il sera utilisé comme paramètre de chemin.


* Si le paramètre est un **type simple** (tel que `int`, `float`, `str`, `bool`, etc.), il sera interprété comme un paramètre de **requête** (query).
* Si le paramètre est déclaré comme un type **Schema** (ou `BaseModel` Pydantic), il sera interprété comme un **corps de requête**.

!!! done

    Poursuivez avec le chapitre suivant ! **[Données de formulaire](form-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
