Perbedaan Antara `query` dan `form` di Ninja
==========================================================
```python
gene_set_db: List[GeneSetLiteral] = Field(
default=['GO_Biological_Process_2023', 'GO_Cellular_Component_2023', 'GO_Molecular_Function_2023'])
```
Dengan `query`, ini dikonversi menjadi (dapat dipasangkan dengan request GET atau POST):

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task?name=goenrich_abc&permutation_type=phenotype&gene_set_db=GO_Biological_Process_2023&gene_set_db=GO_Cellular_Component_2023&gene_set_db=GO_Molecular_Function_2023&out_format=pdf' \
-H 'Content-Type: multipart/form-data' \
```

Dengan `form`, ini dikonversi menjadi (hanya dapat dipasangkan dengan request POST):

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task' \
-H 'Content-Type: multipart/form-data' \
-F 'gene_set_db=GO_Biological_Process_2023,GO_Cellular_Component_2023,GO_Molecular_Function_2023'
```


Meskipun keduanya bertipe `form-data`, pada kasus kedua parameter-parameter tersebut digabungkan dengan koma, sehingga lebih mudah dibedakan. Oleh karena itu, menggunakan FORM secara eksplisit adalah pilihan yang lebih baik.
