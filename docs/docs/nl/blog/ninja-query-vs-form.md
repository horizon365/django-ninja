Het verschil tussen `query` en `form` in Ninja
==========================================================
```python
gene_set_db: List[GeneSetLiteral] = Field(
default=['GO_Biological_Process_2023', 'GO_Cellular_Component_2023', 'GO_Molecular_Function_2023'])
```
In `query` wordt dit omgezet naar (kan worden gecombineerd met een GET- of POST-request):

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task?name=goenrich_abc&permutation_type=phenotype&gene_set_db=GO_Biological_Process_2023&gene_set_db=GO_Cellular_Component_2023&gene_set_db=GO_Molecular_Function_2023&out_format=pdf' \
-H 'Content-Type: multipart/form-data' \
```

In `form` wordt dit omgezet naar (kan alleen worden gecombineerd met een POST-request):

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task' \
-H 'Content-Type: multipart/form-data' \
-F 'gene_set_db=GO_Biological_Process_2023,GO_Cellular_Component_2023,GO_Molecular_Function_2023'
```


Hoewel het type in beide gevallen `form-data` is, worden in het laatste geval meerdere parameters met komma's aan elkaar geplakt, waardoor ze beter van elkaar te onderscheiden zijn. Daarom is het expliciet gebruiken van FORM de betere keuze.
