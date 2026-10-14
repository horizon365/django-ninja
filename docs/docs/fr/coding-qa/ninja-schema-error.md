`ninja_schema` et le schéma à l'intérieur de `ninja` semblent très différents — celui de ninja fonctionne, mais celui de `ninja_schema` lève une erreur
==========================================================

A : `ninja_schema` est-il un paquet séparé ?
B : Oui, il doit être installé avec pip. J'ai regardé le code source, et il semble avoir tiré certaines choses de pydantic. Mais je ne comprends pas pydantic, donc je ne sais pas exactement quelle fonctionnalité les choses nouvellement ajoutées implémentent.

A : Je pense que le schéma de ninja est largement suffisant.
B : Pour aplatir la sortie d'une clé étrangère, la documentation l'utilise ainsi : `owner_first_name: str = Field(None, alias="owner.first_name")`
B : En utilisant celui de `ninja_schema`, une erreur ne cesse d'être levée, disant que l'entrée devrait être un `str`, mais ce qui est fourni est un objet.
B : Je ne m'attendais jamais à ce que ce `Schema` de `ninja_schema` soit la cause.
