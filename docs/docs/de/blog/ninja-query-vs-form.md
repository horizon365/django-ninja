Der Unterschied zwischen `query` und `form` in Ninja
==========================================================
```python
gene_set_db: List[GeneSetLiteral] = Field(
default=['GO_Biological_Process_2023', 'GO_Cellular_Component_2023', 'GO_Molecular_Function_2023'])
```
In `query` wird dies umgewandelt in (kann mit einer GET- oder POST-Anfrage kombiniert werden):

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task?name=goenrich_abc&permutation_type=phenotype&gene_set_db=GO_Biological_Process_2023&gene_set_db=GO_Cellular_Component_2023&gene_set_db=GO_Molecular_Function_2023&out_format=pdf' \
-H 'Content-Type: multipart/form-data' \
```

In `form` wird dies umgewandelt in (kann nur mit einer POST-Anfrage kombiniert werden):

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task' \
-H 'Content-Type: multipart/form-data' \
-F 'gene_set_db=GO_Biological_Process_2023,GO_Cellular_Component_2023,GO_Molecular_Function_2023'
```


Obwohl der Typ in beiden Fällen `form-data` ist, werden bei letzterem mehrere Parameter durch Kommata verbunden, wodurch sie besser unterscheidbar sind. Daher ist die explizite Verwendung von FORM die bessere Wahl.
