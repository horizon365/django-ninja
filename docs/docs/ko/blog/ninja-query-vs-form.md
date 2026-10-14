Ninja에서 `query`와 `form`의 차이
==========================================================
```python
gene_set_db: List[GeneSetLiteral] = Field(
default=['GO_Biological_Process_2023', 'GO_Cellular_Component_2023', 'GO_Molecular_Function_2023'])
```
`query`에서는 다음과 같이 변환됩니다(GET 또는 POST 요청과 함께 사용 가능):

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task?name=goenrich_abc&permutation_type=phenotype&gene_set_db=GO_Biological_Process_2023&gene_set_db=GO_Cellular_Component_2023&gene_set_db=GO_Molecular_Function_2023&out_format=pdf' \
-H 'Content-Type: multipart/form-data' \
```

`form`에서는 다음과 같이 변환됩니다(POST 요청과만 함께 사용 가능):

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task' \
-H 'Content-Type: multipart/form-data' \
-F 'gene_set_db=GO_Biological_Process_2023,GO_Cellular_Component_2023,GO_Molecular_Function_2023'
```


두 경우 모두 타입은 `form-data`이지만, 후자에서는 여러 파라미터가 쉼표로 연결되어 더 구분하기 쉽습니다. 따라서 FORM을 명시적으로 사용하는 것이 더 나은 선택입니다.
