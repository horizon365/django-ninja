Разница между `query` и `form` в Ninja
==========================================================
```python
gene_set_db: List[GeneSetLiteral] = Field(
default=['GO_Biological_Process_2023', 'GO_Cellular_Component_2023', 'GO_Molecular_Function_2023'])
```
В случае с `query` это преобразуется в (может использоваться как с GET-, так и с POST-запросом):

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task?name=goenrich_abc&permutation_type=phenotype&gene_set_db=GO_Biological_Process_2023&gene_set_db=GO_Cellular_Component_2023&gene_set_db=GO_Molecular_Function_2023&out_format=pdf' \
-H 'Content-Type: multipart/form-data' \
```

В случае с `form` это преобразуется в (может использоваться только с POST-запросом):

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task' \
-H 'Content-Type: multipart/form-data' \
-F 'gene_set_db=GO_Biological_Process_2023,GO_Cellular_Component_2023,GO_Molecular_Function_2023'
```


Хотя в обоих случаях типом является `form-data`, во втором варианте несколько параметров объединяются запятыми, что делает их более различимыми. Поэтому явное использование FORM является более удачным выбором.
