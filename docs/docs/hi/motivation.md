---
comments: true
---
# प्रेरणा (Motivation)

!!! note
    **Django Ninja** देखने में मूल रूप से **FastAPI** जैसा ही है, तो FastAPI का ही इस्तेमाल क्यों न करें?

सच कहूँ तो, **Django Ninja** <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a> से बहुत अधिक प्रेरित है (जिसे <a href="https://github.com/tiangolo" target="_blank">Sebastián Ramírez</a> ने विकसित किया है)

फिर भी, FastAPI और Django को सही तरीके से साथ काम कराने में कुछ समस्याएँ होती हैं:

1) **FastAPI** खुद को ORM-agnostic बताता है (इसका मतलब है कि आप इसे SQLAlchemy या Django ORM के साथ इस्तेमाल कर सकते हैं), लेकिन व्यवहार में Django ORM अभी async इस्तेमाल के लिए तैयार नहीं है (शायद version 4.0 या 4.1 में)। अगर आप इसे synchronous mode में इस्तेमाल करते हैं, तो आपको [connection closing issues](https://github.com/tiangolo/fastapi/issues/716) का सामना करना पड़ सकता है और उन पर काबू पाने के लिए **बहुत सारी** मेहनत करनी पड़ती है।

2) जब आप अपने operations में authentication और database sessions पर निर्भर होते हैं (कुछ projects के लिए यह सभी operations का लगभग 99% हिस्सा होता है), तो parameters के साथ dependency injection आपके code को बहुत लंबा-चौड़ा (verbose) बना देता है।

```python hl_lines="25 26"
...

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode(token)
    if not user:
        raise HTTPException(...)
    return user


@app.get("/task/{task_id}", response_model=Task)
def read_user(
        task_id: int,
        db: Session = Depends(get_db), 
        current_user: User = Depends(get_current_user),
    ):
        ... use db with current_user ....
```

3) चूँकि Django में `model` शब्द ORM के लिए "आरक्षित" (reserved) है, इसलिए जब आप Django ORM और Pydantic/FastAPI model naming conventions को मिलाते हैं तो चीज़ें बहुत उलझने लगती हैं।

### Django Ninja

Django Ninja इन सभी समस्याओं को हल करता है और Django (ORM, URLs, views, authentication, आदि) के साथ बहुत अच्छी तरह integrate होता है।
[Code-on, एक Django web design और development studio](https://code-on.be/) में काम करते हुए, मैं विभिन्न चुनौतियों का सामना करता रहा, और उन्हें हल करने के लिए मैंने 2020 में Django-Ninja project शुरू किया।

ध्यान दें: **Django Ninja एक production-ready project है** - मेरा अनुमान है कि इस समय 100 से अधिक कंपनियाँ इसे production में इस्तेमाल कर रही हैं, और हर महीने 500 नए developers इसमें जुड़ रहे हैं।

कुछ कंपनियाँ पहले से ही Django Ninja का अनुभव रखने वाले developers की तलाश में हैं।

#### मुख्य विशेषताएँ

1) चूँकि आपके पास कई Django Ninja API instances हो सकते हैं, इसलिए आप एक ही Django project में [कई API versions](guides/versioning.md) चला सकते हैं।

```python
api_v1 = NinjaAPI(version='1.0', auth=token_auth)
...
api_v2 = NinjaAPI(version='2.0', auth=token_auth)
...
api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')
...


urlpatterns = [
    ...
    path('api/v1/', api_v1.urls),
    path('api/v2/', api_v2.urls),
    path('internal-api/', api_private.urls),
]
```

2) Django Ninja की 'Schema' class ORM के साथ integrate होती है, इसलिए आप [querysets को serialize](guides/response/index.md#returning-querysets) कर सकते हैं या ORM objects:

```python
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()


@api.get("/tasks", response=TaskSchema)
def tasks_details(request):
    task = Task.objects.first()
    return task
```
3) [Django model से एक Schema बनाएँ](guides/response/django-pydantic.md)।

4) dependency parameters का इस्तेमाल करने की बजाय, **Django Ninja** `request` instance की properties का इस्तेमाल करता है (वही तरीका जो साधारण Django views करते हैं) - अधिक जानकारी के लिए [Authentication](guides/authentication.md) देखें।

!!! note

    जल्दी शुरुआत करने के लिए **[Tutorial](tutorial/index.md)** देखें।

    Django Ninja के आस-पास का ecosystem:

    1. [django-ninja-crud](django-ninja-crud/index.md): django-ninja पर बना एक framework जो CRUD interface development को आसान बनाता है, जो declarative model viewsets और scenario-आधारित testing methods प्रदान करता है।

    2. [django-ninja-extra](django-ninja-extra/index.md): एक tool जो developers को लंबे-चौड़े Django documentation से बचाता है और न्यूनतम code के साथ तेज़ी से शक्तिशाली web applications और आधुनिक API interfaces बनाने देता है।

    3. [django-ninja-jwt](django-ninja-jwt/index.md): django-ninja के लिए एक JSON Web Token plugin जो authentication और संबंधित features implement करता है, जो एक लोकप्रिय Django Rest Framework plugin से fork किया गया है।

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
