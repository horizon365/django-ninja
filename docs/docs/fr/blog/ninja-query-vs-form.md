La différence entre `query` et `form` dans Ninja
==========================================================
```python
gene_set_db: List[GeneSetLiteral] = Field(
default=['GO_Biological_Process_2023', 'GO_Cellular_Component_2023', 'GO_Molecular_Function_2023'])
```
Avec `query`, ceci est converti en (peut être associé à une requête GET ou POST) :

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task?name=goenrich_abc&permutation_type=phenotype&gene_set_db=GO_Biological_Process_2023&gene_set_db=GO_Cellular_Component_2023&gene_set_db=GO_Molecular_Function_2023&out_format=pdf' \
-H 'Content-Type: multipart/form-data' \
```

Avec `form`, ceci est converti en (ne peut être associé qu'à une requête POST) :

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task' \
-H 'Content-Type: multipart/form-data' \
-F 'gene_set_db=GO_Biological_Process_2023,GO_Cellular_Component_2023,GO_Molecular_Function_2023'
```


Bien que le type soit `form-data` dans les deux cas, dans le second cas, les multiples paramètres sont joints par des virgules, ce qui les rend plus faciles à distinguer. Par conséquent, utiliser explicitement FORM est le meilleur choix.
