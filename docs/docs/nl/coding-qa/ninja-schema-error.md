`ninja_schema` en het schema in `ninja` voelen heel verschillend aan — dat van ninja werkt, maar die in `ninja_schema` geeft een fout
==========================================================

A: Is `ninja_schema` een apart pakket?
B: Ja, het moet met pip worden geïnstalleerd. Ik heb naar de broncode gekeken en het lijkt erop dat het een aantal dingen uit pydantic heeft overgenomen. Maar ik begrijp pydantic niet, dus ik weet niet precies welke functionaliteit de nieuw toegevoegde dingen implementeren.

A: Ik vind het schema van ninja meer dan genoeg.
B: Voor het afvlakken van foreign key-uitvoer gebruikt de documentatie het zo: `owner_first_name: str = Field(None, alias="owner.first_name")`
B: Als ik die van `ninja_schema` gebruik, blijf ik een foutmelding krijgen dat de invoer een `str` moet zijn, maar wat er wordt gegeven is een object.
B: Ik had nooit verwacht dat deze `Schema` uit `ninja_schema` de oorzaak was.
