---
comments: true
---
# Request Body

De request body wordt doorgaans gebruikt bij "create"- en "update"-operaties (POST, PUT, PATCH).
Bij het aanmaken van een resource met POST of PUT bevat de request body bijvoorbeeld meestal een representatie van de aan te maken resource.

Om een request body te declareren, moet je **de `Schema` van Django Ninja** gebruiken.

!!! note
    Onder de motorkap benut **Django Ninja** alle kracht en mogelijkheden van het <a href="https://pydantic.com.cn/" class="external-link" target="_blank">Pydantic</a> Model.
    De alias `Schema` is gekozen om codeverwarring te voorkomen bij het werken met Django models, aangezien de model class van Pydantic standaard `Model` heet, wat botst met de `Model` class van Django.
    

## Schema importeren

Allereerst moet je `Schema` importeren uit `ninja`:

```python hl_lines="2"
{!./src/tutorial/body/code01.py!}
```

## Je datamodel maken

Declareer vervolgens je datamodel als een class die overerft van `Schema`.

Gebruik standaard Python types voor alle attributen:

```python hl_lines="5 6 7 8 9"
{!./src/tutorial/body/code01.py!}
```

Let op: als je de standaardwaarde van een attribuut instelt op **`None`**, wordt het optioneel in de request body. Het model hierboven declareert bijvoorbeeld een JSON "`object`" (of Python `dict`) zoals hieronder:

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...aangezien `description` optioneel is (de standaardwaarde is `None`), is ook deze JSON "`object`" geldig:

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```

## Declareren als parameter

Om het toe te voegen aan je *path operation*, declareer je het op dezelfde manier als je path- en queryparameters declareert:


```python hl_lines="13"
{!./src/tutorial/body/code01.py!}
```

... en declareer het type als het `Item` model dat je hebt gemaakt.

## Resultaat

Met alleen die Python typedefinitie zal **Django Ninja**:

* De request body als JSON inlezen.
* Converteren naar de juiste types (indien nodig).
* De data valideren.
    * Als de data ongeldig is, wordt er een vriendelijke en zinvolle foutmelding teruggegeven die precies aangeeft waar de foutieve data zich bevindt en wat de inhoud ervan is.
* De ontvangen data aan je geven in de parameter `item`.
    * Aangezien je het type als `Item` in de functie hebt gedeclareerd, krijg je ook editorondersteuning (autocomplete, enz.) voor alle attributen en hun types.
* <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> definities voor je model genereren, die je overal in je project kunt gebruiken waar je ze nodig hebt.
* Deze schemas worden onderdeel van het gegenereerde OpenAPI schema en worden gebruikt door de automatische documentatie <abbr title="User Interfaces">UI</abbr>.

## Automatische documentatie

De JSON Schemas van je modellen worden onderdeel van je gegenereerde OpenAPI schema en worden weergegeven in de interactieve API-documentatie:

![Openapi schema](../../img/body-schema-doc.png)

...en ze worden ook gebruikt in de API-documentatie voor elke *path operation* die ze nodig heeft:

![Openapi schema](../../img/body-schema-doc2.png)

## Editorondersteuning

In je editor, binnen je functie, krijg je overal type hints en completion (dit gebeurt niet als je een `dict` gebruikt in plaats van een Schema object):

![Type hints](../../img/body-editor.gif)


De bovenstaande schermafbeeldingen zijn gemaakt met <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>.

Je krijgt dezelfde editorondersteuning in <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> en de meeste andere Python editors.

## Request Body + Path Parameters

Je kunt path parameters **en** request body tegelijk declareren.


**Django Ninja** herkent dat functieparameters die overeenkomen met path parameters **uit het path** moeten worden genomen, terwijl functieparameters die met `Schema` zijn gedeclareerd **uit de request body** moeten worden genomen.

```python hl_lines="11 12"
{!./src/tutorial/body/code02.py!}
```

## Request Body + Path + Query Parameters

Je kunt ook **request body**, **path**- en **query** parameters tegelijk declareren.

**Django Ninja** herkent elke parameter en haalt de data uit de juiste locatie.

```python hl_lines="11 12"
{!./src/tutorial/body/code03.py!}
```

Functieparameters worden als volgt herkend:

* Als de parameter ook in het **path** is gedeclareerd, wordt deze gebruikt als path parameter.

 
* Als de parameter een **enkel type** is (zoals `int`, `float`, `str`, `bool`, enz.), wordt deze geïnterpreteerd als een **query** parameter.
* Als de parameter is gedeclareerd als **Schema** type (of Pydantic `BaseModel`), wordt deze geïnterpreteerd als een **request body**.

!!! done

    Ga verder naar het volgende hoofdstuk! **[Formulierdata](form-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
