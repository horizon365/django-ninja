---
comments: true
---
# Request Body

Der Request Body wird typischerweise bei „create"- und „update"-Operationen verwendet (POST, PUT, PATCH).
Wenn Sie zum Beispiel eine Ressource mit POST oder PUT erstellen, enthält der Request Body üblicherweise eine Repräsentation der zu erstellenden Ressource.

Um einen Request Body zu deklarieren, müssen Sie **Django Ninjas `Schema`** verwenden.

!!! note
    Unter der Haube nutzt **Django Ninja** die gesamte Leistungsfähigkeit und alle Features des <a href="https://pydantic.com.cn/" class="external-link" target="_blank">Pydantic</a> Model.
    Der Alias `Schema` wurde gewählt, um Verwirrung im Code bei der Arbeit mit Django-Modellen zu vermeiden, da die Model-Klasse von Pydantic standardmäßig `Model` heißt, was mit Djangos `Model`-Klasse kollidieren würde.
    

## Schema importieren

Zuerst müssen Sie `Schema` aus `ninja` importieren:

```python hl_lines="2"
{!./src/tutorial/body/code01.py!}
```

## Ihr Datenmodell erstellen

Dann deklarieren Sie Ihr Datenmodell als Klasse, die von `Schema` erbt.

Verwenden Sie für alle Attribute die Standard-Python-Typen:

```python hl_lines="5 6 7 8 9"
{!./src/tutorial/body/code01.py!}
```

Hinweis: Wenn Sie den Standardwert eines Attributs auf **`None`** setzen, wird es im Request Body optional. Das obige Modell deklariert zum Beispiel ein JSON-„`object`" (oder Python-`dict`) wie folgt:

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

... da `description` optional ist (sein Standardwert ist `None`), ist auch dieses JSON-„`object`" gültig:

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```

## Als Parameter deklarieren

Um es zu Ihrer *Path-Operation* hinzuzufügen, deklarieren Sie es auf dieselbe Weise wie Path- und Query-Parameter:


```python hl_lines="13"
{!./src/tutorial/body/code01.py!}
```

... und deklarieren Sie seinen Typ als das von Ihnen erstellte `Item`-Modell.

## Ergebnis

Allein mit dieser Python-Typdeklaration wird **Django Ninja**:

* den Request Body als JSON einlesen.
* in die passenden Typen konvertieren (falls erforderlich).
* die Daten validieren.
    * Sind die Daten ungültig, wird ein verständlicher und aussagekräftiger Fehler zurückgegeben, der genau den Ort und Inhalt der fehlerhaften Daten angibt.
* Ihnen die empfangenen Daten im Parameter `item` bereitstellen.
    * Da Sie seinen Typ in der Funktion als `Item` deklariert haben, erhalten Sie außerdem Editor-Unterstützung (Autovervollständigung usw.) für alle Attribute und ihre Typen.
* <a href="https://json-schema.org" class="external-link" target="_blank">JSON-Schema</a>-Definitionen für Ihr Modell generieren, die Sie überall dort in Ihrem Projekt verwenden können, wo Sie sie benötigen.
* Diese Schemata werden Teil des generierten OpenAPI-Schemas und werden von der automatischen Dokumentation <abbr title="User Interfaces">UI</abbr> verwendet.

## Automatische Dokumentation

Die JSON-Schemata Ihrer Modelle werden Teil Ihres generierten OpenAPI-Schemas und werden in der interaktiven API-Dokumentation angezeigt:

![Openapi schema](../../img/body-schema-doc.png)

... und sie werden auch in der API-Dokumentation für jede *Path-Operation* verwendet, die sie benötigt:

![Openapi schema](../../img/body-schema-doc2.png)

## Editor-Unterstützung

In Ihrem Editor erhalten Sie innerhalb Ihrer Funktion überall Type Hints und Vervollständigung (das passiert nicht, wenn Sie statt eines Schema-Objekts ein `dict` verwenden):

![Type hints](../../img/body-editor.gif)


Die vorherigen Screenshots wurden mit <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a> erstellt.

Dieselbe Editor-Unterstützung erhalten Sie in <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> und den meisten anderen Python-Editoren.

## Request Body + Path-Parameter

Sie können Path-Parameter **und** Request Body gleichzeitig deklarieren.


**Django Ninja** erkennt, dass Funktionsparameter, die Path-Parametern entsprechen, **aus dem Pfad** genommen werden sollen, während Funktionsparameter, die mit `Schema` deklariert wurden, **aus dem Request Body** genommen werden sollen.

```python hl_lines="11 12"
{!./src/tutorial/body/code02.py!}
```

## Request Body + Path- + Query-Parameter

Sie können auch **Request Body**, **Path**- und **Query**-Parameter gleichzeitig deklarieren.

**Django Ninja** erkennt jeden Parameter und nimmt die Daten aus der richtigen Stelle.

```python hl_lines="11 12"
{!./src/tutorial/body/code03.py!}
```

Funktionsparameter werden wie folgt erkannt:

* Wenn der Parameter ebenfalls im **Path** deklariert ist, wird er als Path-Parameter verwendet.

 
* Ist der Parameter ein **einfacher Typ** (wie `int`, `float`, `str`, `bool` usw.), wird er als **Query**-Parameter interpretiert.
* Ist der Parameter als **Schema** (oder Pydantic `BaseModel`) deklariert, wird er als **Request Body** interpretiert.

!!! done

    Weiter zum nächsten Kapitel! **[Formulardaten](form-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
