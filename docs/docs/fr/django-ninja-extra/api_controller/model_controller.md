**Contrôleur de modèle**
=======================

  
Le contrôleur de modèle génère dynamiquement des opérations CRUD (Create, Read, Update, Delete) pour un modèle ORM Django au sein d'un contrôleur, en fonction de la configuration spécifiée.

  
Le contrôleur de modèle étend la classe `ControllerBase` et introduit deux variables de configuration, à savoir `model_config` et `model_service`.

*     
    `model_config` est responsable de la définition de la configuration liée à la génération des routes et des schémas.
*     
    `model_service` désigne la classe utilisée pour gérer les opérations CRUD (Create, Read, Update, Delete) pour le modèle spécifié.

  
Par exemple, considérons un modèle `Event` défini dans Django :

    from django.db import models
    
    class Category(models.Model):
        title = models.CharField(max_length=100)
    
    class Event(models.Model):
        title = models.CharField(max_length=100)
        category = models.OneToOneField(
            Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='events'
        )
        start_date = models.DateField()
        end_date = models.DateField()
    
        def __str__(self):
            return self.title
    

  
Maintenant, créons un `ModelController` pour le modèle `Event`. Dans le fichier `api.py`, nous définissons un `EventModelController` :

    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
        NinjaExtraAPI
    )
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
        
    api = NinjaExtraAPI()
    api.register_controllers(EventModelController)
    

  
Notez que le contrôleur de modèle repose sur le paquet `ninja-schema` pour la génération automatique des schémas. Pour installer le paquet, utilisez la commande suivante :

    pip install ninja-schema
    

  
Après l'installation, vous pouvez accéder à la documentation API générée automatiquement en visitant http://localhost:8000/api/docs.

  
Ce document fournit une vue d'ensemble détaillée des routes, des schémas et des fonctionnalités exposés par le `EventModelController` pour le modèle `Event`.

**Configuration du modèle**
-----------------------

  
`ModelConfig` est un schéma Pydantic utilisé pour valider et configurer le comportement du contrôleur de modèle. Les principales options de configuration incluent :

*     
    Model : Un champ requis représentant le type de modèle Django associé au Model Controller.
*     
    async_routes : Indique si les routes du contrôleur doivent être créées comme des fonctions de route `asynchrones`.
*     
    allowed_routes : Une liste spécifiant les opérations API autorisées à être générées dans le Model Controller. La valeur par défaut est `["create", "find_one", "update", "patch", "delete", "list"]`.
*     
    create_schema : Un schéma Pydantic optionnel décrivant le type de données d'entrée pour l'opération `create` ou `POST` dans le contrôleur de modèle. La valeur par défaut est `None`. S'il n'est pas fourni, le `ModelController` générera un nouveau schéma basé sur l'option `schema_config`.
*     
    update_schema : Un schéma Pydantic optionnel détaillant le type de données d'entrée pour l'opération `update` ou `PUT` dans le contrôleur de modèle. La valeur par défaut est `None`. S'il n'est pas fourni, le `create_schema` sera utilisé s'il est disponible, sinon un nouveau schéma sera généré basé sur l'option `schema_config`.
*     
    retrieve_schema : Un schéma Pydantic optionnel de sortie définissant le type de données de sortie pour diverses opérations. La valeur par défaut est `None`. S'il n'est pas fourni, le `ModelController` générera un schéma basé sur l'option `schema_config`.
*     
    patch_schema : Un schéma Pydantic optionnel de sortie spécifiant le type de données d'entrée pour l'opération `patch/PATCH`. La valeur par défaut est `None`. S'il n'est pas fourni, le `ModelController` générera un schéma avec tous les champs optionnels.
*     
    schema_config : Un autre champ requis décrivant la méthode de génération de schéma requise pour les opérations du Model Controller. Les options de configuration incluent :
    *     
        `include` : Une liste de champs à inclure. La valeur par défaut est `__all__`.
        
    *     
        `exclude` : Une liste de champs à exclure. La valeur par défaut est `[]`.
        
    *     
        `optional` : Une liste de champs à forcer comme optionnels. La valeur par défaut est `[pk]`.
        
    *     
        `depth` : La profondeur pour la génération de schémas imbriqués.
        
    *     
        `read_only_fields` : Une liste de champs à exclure lors de la génération des schémas d'entrée pour les opérations create, update et patch.
        
    *     
        `write_only_fields` : Une liste de champs à exclure lors de la génération des schémas de sortie pour les opérations find_one et list.
        
    *     
        pagination : Une exigence pour l'opération `list/GET` du modèle afin d'éviter d'envoyer `100_000` éléments à la fois dans une requête. La configuration de la pagination nécessite de définir un objet schéma Pydantic `ModelPagination`. Les options incluent :
        
        *     
            `klass` : Une classe de pagination de type `PaginationBase`. La valeur par défaut est `PageNumberPaginationExtra`.
        *     
            `paginator_kwargs` : Valeurs du dictionnaire pour l'initialisation de `PaginationBase`. La valeur par défaut est None.
        *     
            `pagination_schema` : Un schéma générique Pydantic combiné avec `retrieve_schema` pour générer le schéma de réponse pour l'opération `list/GET`.
        
          
        Par exemple, si vous choisissez une pagination `ninja` comme `LimitOffsetPagination` :
        
            from ninja.pagination import LimitOffsetPagination
            from ninja_extra.schemas import NinjaPaginationResponseSchema
            from ninja_extra import (
                ModelConfig,
                ModelControllerBase,
                api_controller,
                ModelPagination
            )
            
            @api_controller("/events")
            class EventModelController(ModelControllerBase):
                model_config = ModelConfig(
                    model=Event,
                    pagination=ModelPagination(
                        klass=LimitOffsetPagination, 
                        pagination_schema=NinjaPaginationResponseSchema
                    ),
                )
            
        


**  
En savoir plus sur les opérations du contrôleur de modèle**
------------------

  
Dans les contrôleurs de modèle NinjaExtra, le comportement du contrôleur peut être contrôlé via le contenu de la liste `allowed_routes` dans l'option `model_config`.

  
Par exemple, vous pouvez créer un contrôleur en lecture seule comme ceci :

    from ninja_extra import api_controller, ModelControllerBase, ModelConfig, ModelSchemaConfig
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            allowed_routes=['find_one', 'list'],
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    

  
Cela ne créera que les routes `GET/{id}` et `GET/` pour le listage.

  
Vous pouvez également ajouter d'autres endpoints à un `EventModelController` existant. Par exemple :

    from ninja_extra import api_controller, http_get, ModelControllerBase, ModelConfig, ModelSchemaConfig
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            allowed_routes=['find_one', 'list'],
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    
        @http_get('/subtract',)
        def subtract(self, a: int, b: int):
            """Subtracts a from b"""
            return {"result": a - b}
    

**Service de modèle**
-----------------

  
Chaque contrôleur de modèle crée une instance de `ModelService` à l'exécution pour gérer l'interaction entre le modèle et le contrôleur. Typiquement, ces opérations de service de modèle feraient partie du contrôleur de modèle, mais elles sont abstraites dans un service pour permettre une approche plus dynamique.

    class ModelService(ModelServiceBase):
        """
        Model Service for Model Controller model CRUD operations with simple logic for simple models.
    
        It's advised to override this class if you have a complex model.
        """
        def __init__(self, model: Type[DjangoModel]) -> None:
            self.model = model
    
        # ... (other CRUD methods)
    

  
Ces opérations sont appelées en fonction de l'opération en cours sur le contrôleur de modèle ou de la requête que le contrôleur de modèle traite.

### **Utiliser un service de modèle personnalisé**

  
Surcharger le `ModelService` dans un contrôleur de modèle est plus important que de surcharger les opérations de route. Le `ModelService` par défaut utilisé dans les contrôleurs de modèle est conçu pour des modèles Django simples. Si le modèle est complexe, il est recommandé de surcharger le `ModelService`.

  
Par exemple, si vous souhaitez modifier la manière dont le modèle `Event` est enregistré :

    from ninja_extra import ModelService
    
    class EventModelService(ModelService):
        def create(self, schema: PydanticModel, **kwargs: Any) -> Any:
            data = schema.dict(by_alias=True)
            data.update(kwargs)
            
            instance = self.model._default_manager.create(**data)
            return instance
    
            
    

  
Puis dans `api.py`

    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
    )
    from .service import EventModelService
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        service = EventModelService(model=Event)
        model_config = ModelConfig(
            model=Event,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    

### **Activer les routes asynchrones**

  
Dans `model_config`, définissez `async_routes` à `True`

    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
    )
    from .service import EventModelService
    from .models import Event
    
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        service = EventModelService(model=Event)
        model_config = ModelConfig(
            model=Event,
            async_routes=True,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    

  
En définissant le paramètre `async_routes` à `True` dans `model_config`, le `ModelController` bascule dynamiquement entre `ModelAsyncEndpointFactory` et `ModelEndpointFactory` en fonction de la configuration pour générer des endpoints async ou sync.

### **Contrôleur de modèle et service de modèle ensemble**

  
Si nécessaire, le contrôleur et le service de modèle peuvent également être fusionnés ensemble :

  
Par exemple, en utilisant le `EventModelService` que nous avons créé

    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
    )
    from .service import EventModelService
    from .models import Event
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase, EventModelService):
        model_config = ModelConfig(
            model=Event,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
        
        def __init__(self):
            EventModelService.__init__(self, model=Event)
            self.service = self  # This will expose the functions to the service attribute
    

**Fabrique d'endpoints de modèle**
-----------

  
`ModelEndpointFactory` est une classe de fabrique utilisée par le contrôleur de modèle pour générer des endpoints de manière transparente. Elle peut également être utilisée directement dans tout contrôleur NinjaExtra dans le même but.

  
Par exemple, si nous voulons ajouter un `Event` à une nouvelle `Category`, cela peut être fait comme suit :

    from typing import Any
    from pydantic import BaseModel
    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
        ModelEndpointFactory
    )
    from .models import Event, Category
    
    class CreateCategorySchema(BaseModel):
        title: str
    
    class CategorySchema(BaseModel):
        id: str
        title: str
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    
        add_event_to_new_category = ModelEndpointFactory.create(
            path="/{int:event_id}/new-category",
            schema_in=CreateCategorySchema,
            schema_out=CategorySchema,
            custom_handler=lambda self, data, **kw: self.handle_add_event_to_new_category(data, **kw)
        )
    
        def handle_add_event_to_new_category(self, data: CreateCategorySchema, **kw: Any) -> Category:
            event = self.service.get_one(pk=kw['event_id'])
            category = Category.objects.create(title=data.title)
            event.category = category
            event.save()
            return category
    

  
Dans l'exemple ci-dessus, nous avons utilisé `ModelEndpointFactory.create` pour créer un endpoint `POST /{int:event_id}/new-category`, en passant les schémas d'entrée et de sortie ainsi qu'un gestionnaire personnalisé. En passant `custom_handler`, la fonction de route générée délègue son opération de traitement au `custom_handler` fourni au lieu d'appeler `service.create`.

**  
Fabrique d'endpoints de modèle asynchrone**
---------------

  
`ModelAsyncEndpointFactory` possède la même interface d'API que `ModelEndpointFactory`, mais est spécialement conçu pour générer des endpoints asynchrones.

  
Nous pouvons créer le même exemple qu'avec `ModelEndpointFactory`

Par exemple :

    from typing import Any
    from pydantic import BaseModel
    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
        ModelAsyncEndpointFactory
    )
    from .models import Event, Category
    
    class CreateCategorySchema(BaseModel):
        title: str
    
    class CategorySchema(BaseModel):
        id: str
        title: str
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    
        add_event_to_new_category = ModelAsyncEndpointFactory.create(
            path="/{int:event_id}/new-category",
            schema_in=CreateCategorySchema,
            schema_out=CategorySchema,
            custom_handler=lambda self, data, **kw: self.handle_add_event_to_new_category(data, **kw)
        )
    
        async def handle_add_event_to_new_category(self, data: CreateCategorySchema, **kw: Any) -> Category:
            event = await self.service.get_one_async(pk=kw['event_id'])
            category = Category.objects.create(title=data.title)
            event.category = category
            event.save()
            return category
    

  
Dans l'illustration ci-dessus, nous avons créé `add_event_to_new_category` comme une fonction asynchrone et avons également converti `handle_add_event_to_new_category` en fonction asynchrone.

**QueryGetter et ObjectGetter**
--------------------------------

  
`ModelEndpointFactory` expose une manière plus flexible d'obtenir un objet de modèle ou un filtre de queryset, respectivement dans le cas de `ModelEndpointFactory.find_one` et `ModelEndpointFactory.list`.

  
Par exemple, pour récupérer la catégorie d'un événement (pas très pratique, mais à titre d'illustration) :

    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
        ModelEndpointFactory
    )
    from .models import Event, Category
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    
        get_event_category = ModelEndpointFactory.find_one(
            path="/{int:event_id}/category",
            schema_out=CategorySchema,
            lookup_param='event_id',
            object_getter=lambda self, pk, **kw: self.service.get_one(pk=pk).category
        )
    

  
Dans l'exemple ci-dessus, nous avons utilisé `ModelEndpointFactory.find_one` pour créer un endpoint `get_event_category` et fourni un `object_getter` comme callback pour récupérer le modèle en fonction de `event_id`. Le `lookup_param` indique la clé dans `kwargs` utilisée pour définir la valeur du pk pour la récupération de l'objet modèle, si aucun gestionnaire `object_getter` n'est implémenté.

  
En revanche, vous pouvez rencontrer une situation où vous devez lister les événements par `category_id` :

    from ninja_extra import (
        ModelConfig,
        ModelControllerBase,
        ModelSchemaConfig,
        api_controller,
        ModelEndpointFactory
    )
    from .models import Event, Category
    
    @api_controller("/events")
    class EventModelController(ModelControllerBase):
        model_config = ModelConfig(
            model=Event,
            schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
        )
    
        get_events_by_category = ModelEndpointFactory.list(
            path="/category/{int:category_id}/",
            schema_out=model_config.retrieve_schema,
            lookup_param='category_id',
            queryset_getter=lambda self, **kw: Category.objects.filter(pk=kw['category_id']).first().events.all()
        )
    

  
En utilisant `ModelEndpointFactory.list` avec `queryset_getter`, vous pouvez rapidement mettre en place un endpoint de liste qui renvoie les événements appartenant à une catégorie. Notez que si un ID invalide est fourni, notre `queryset_getter` peut échouer car ce n'est qu'un exemple.

  
De plus, gardez à l'esprit qu'après l'instanciation du ModelConfig, des paramètres comme `model_config` peuvent toujours être utilisés, tels que `create_schema`, `retrieve_schema`, `patch_schema` et `update_schema`.

**  
Paramètres de chemin et de requête**
--------------

  
Dans `ModelEndpointFactory`, les paramètres de chemin sont analysés pour identifier les paramètres `path` et `query`. Ces paramètres sont ensuite créés comme des champs dans le schéma d'entrée Ninja et analysés pendant la requête, en les passant comme kwargs au gestionnaire.

Par exemple,

    list_post_tags = ModelEndpointFactory.list(
        path="/{int:id}/tags/{post_id}?query=int&query1=int",
        schema_out=model_config.retrieve_schema,
        queryset_getter=lambda self, **kw: self.list_post_tags_query(**kw)
    )
    
    def list_post_tags_query(self, **kwargs):
        assert kwargs['id']
        assert kwargs['query']
        assert kwargs['query1']
        post_id = kwargs['post_id']
        return Post.objects.filter(id=post_id).first().tags.all()
    

  
Dans cet exemple, le chemin `/{int:id}/tags/{post_id}?query=int&query1=int` génère deux paramètres de chemin `['id:int', 'post_id:str']` et deux paramètres de requête `['query:int', 'query1:int']`. Ces paramètres sont regroupés dans le schéma d'entrée Ninja et analysés pendant la requête, en les passant comme kwargs au gestionnaire de route.

  
Notez que lorsque les paramètres `path` et `query` sont définis, ils sont ajoutés comme champs requis au schéma d'entrée ninja, et non comme optionnels. De plus, les types de données de chemin et de requête doivent être compatibles avec les convertisseurs d'URL de Django.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
