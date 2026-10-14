`ninja_schema` und das Schema in `ninja` fühlen sich sehr unterschiedlich an — bei ninja funktioniert es, aber das aus `ninja_schema` löst einen Fehler aus
==========================================================

A: Ist `ninja_schema` ein separates Paket?
B: Ja, es muss per pip installiert werden. Ich habe mir den Quellcode angesehen, und es scheint einige Dinge aus pydantic übernommen zu haben. Aber ich verstehe pydantic nicht, daher bin ich mir nicht sicher, welche Funktionalität die neu hinzugekommenen Dinge implementieren.

A: Ich denke, das Schema von Ninja reicht völlig aus.
B: Zum Glätten (Flattening) von Fremdschlüssel-Ausgaben verwendet die Dokumentation es so: `owner_first_name: str = Field(None, alias="owner.first_name")`
B: Mit dem aus `ninja_schema` kommt immer wieder ein Fehler, dass die Eingabe ein `str` sein soll, aber übergeben wird ein Objekt.
B: Ich hätte nie erwartet, dass dieses `Schema` aus `ninja_schema` die Ursache ist.
