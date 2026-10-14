Ninja における `query` と `form` の違い
==========================================================
```python
gene_set_db: List[GeneSetLiteral] = Field(
default=['GO_Biological_Process_2023', 'GO_Cellular_Component_2023', 'GO_Molecular_Function_2023'])
```
`query` の場合、これは次のように変換されます（GET または POST リクエストと組み合わせることができます）:

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task?name=goenrich_abc&permutation_type=phenotype&gene_set_db=GO_Biological_Process_2023&gene_set_db=GO_Cellular_Component_2023&gene_set_db=GO_Molecular_Function_2023&out_format=pdf' \
-H 'Content-Type: multipart/form-data' \
```

`form` の場合、これは次のように変換されます（POST リクエストとしか組み合わせることができません）:

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task' \
-H 'Content-Type: multipart/form-data' \
-F 'gene_set_db=GO_Biological_Process_2023,GO_Cellular_Component_2023,GO_Molecular_Function_2023'
```


どちらの場合も型は `form-data` ですが、後者では複数のパラメータがカンマで連結されるため、より区別しやすくなっています。したがって、明示的に FORM を使う方が良い選択です。
