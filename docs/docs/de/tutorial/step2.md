---
comments: true
---
# Tutorial - Eingabeparameter verarbeiten

## Parameter aus dem Query-String übergeben

Ändern wir die Operation so, dass sie einen Namen aus dem URL-Query-String entgegennimmt. Dazu fügen Sie unserer Funktion einfach ein Argument `name` hinzu.

```python
@api.get("/hello")
def hello(request, name):
    return f"Hello {name}"
```

Wenn wir das benannte Argument angeben, erhalten wir die erwartete (HTTP 200) Antwort.

<a href="http://localhost:8000/api/hello?name=you"
target="_blank">localhost:8000/api/hello?name=you</a>:

```json
"Hello you"
```

### Standardwerte

Wenn Sie den Parameter nicht angeben, wird eine HTTP-422-Fehlerantwort zurückgegeben.

*[HTTP 422]: Unprocessable Entity

<a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a>:

```json
{
  "detail": [
    {
      "loc": ["query", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

Wir können einen Standardwert für das Argument `name` festlegen, falls er nicht angegeben wird:

```python hl_lines="2"
@api.get("/hello")
def hello(request, name="world"):
    return f"Hello {name}"
```

## Eingabetypen

**Django Ninja** verwendet standardmäßige [Python Type Hints](https://docs.python.org/3/library/typing.html), um Eingabetypen zu formatieren. Wenn kein Typ angegeben wird, wird ein String angenommen (aber Type Hints für alle Argumente anzugeben ist Best Practice).

Fügen wir eine zweite Operation hinzu, die eine einfache Berechnung mit Ganzzahlen durchführt.

```python hl_lines="5-7"
@api.get("/hello")
def hello(request, name: str = "world"):
    return f"Hello {name}"

@api.get("/math")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

<a href="http://localhost:8000/api/math?a=2&b=3"
target="_blank">localhost:8000/api/math?a=2&b=3</a>:

```json
{
  "add": 5,
  "multiply": 6
}
```

## Parameter über Pfad-Strings übergeben

Sie können Pfad-„Parameter" mit derselben Syntax wie Python-Format-Strings deklarieren.

Jeder Parameter, der im Pfad-String gefunden wird, wird als Argument an Ihre Funktion übergeben, statt aus dem Query-String genommen zu werden.

```python hl_lines="1"
@api.get("/math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

Jetzt greifen wir über <a href="http://localhost:8000/api/math/2and3"
target="_blank">localhost:8000/api/math/2and3</a> auf die Math-Operation zu.


## Parameter über den Request Body übergeben

Wir ändern die Operation `hello` so, dass sie eine HTTP-`POST`-Anfrage verwendet und die Parameter aus dem Request Body bezieht.

Um anzugeben, dass Parameter aus dem Request Body stammen, müssen wir ein Schema deklarieren.

*[Schema]: Eine Erweiterung eines Pydantic-„Model"

```python hl_lines="1 5-6 8-10"
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class HelloSchema(Schema):
    name: str = "world"

@api.post("/hello")
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"
```

### Selbst dokumentierende API

Wenn Sie nun <a href="http://localhost:8000/api/hello" target="_blank">localhost:8000/api/hello</a> aufrufen, erhalten Sie eine HTTP-405-Fehlerantwort, weil wir die an diese URL gerichtete Anfrage auf den POST-Typ ändern müssen.

*[HTTP 405]: Method Not Allowed

Eine einfache Möglichkeit, dies zu tun, ist die Swagger-Dokumentation, die automatisch für uns erstellt wird, unter der Standard-URL „/docs" (an unsere API-Basis-URL angehängt).

1. Besuchen Sie <a href="http://localhost:8000/api/docs" target="_blank">localhost:8000/api/docs</a>, um die von uns erstellten Operationen zu sehen
1. Öffnen Sie die Operation `/api/hello`
2. Klicken Sie auf „Try it out"
3. Ändern Sie den Request Body
4. Klicken Sie auf „Execute"

!!! success

    Fahren Sie mit dem nächsten Kapitel fort: **[Responses verarbeiten](step3.md)**
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
