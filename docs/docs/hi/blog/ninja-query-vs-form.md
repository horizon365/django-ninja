Ninja में `query` और `form` के बीच का अंतर
==========================================================
```python
gene_set_db: List[GeneSetLiteral] = Field(
default=['GO_Biological_Process_2023', 'GO_Cellular_Component_2023', 'GO_Molecular_Function_2023'])
```
`query` में, यह इस रूप में बदल जाता है (GET या POST request के साथ जोड़ा जा सकता है):

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task?name=goenrich_abc&permutation_type=phenotype&gene_set_db=GO_Biological_Process_2023&gene_set_db=GO_Cellular_Component_2023&gene_set_db=GO_Molecular_Function_2023&out_format=pdf' \
-H 'Content-Type: multipart/form-data' \
```

`form` में, यह इस रूप में बदल जाता है (केवल POST request के साथ जोड़ा जा सकता है):

```shell
curl -X 'POST' \
'http://local.cngb.org:10496/genebank_human/api/go/post_task' \
-H 'Content-Type: multipart/form-data' \
-F 'gene_set_db=GO_Biological_Process_2023,GO_Cellular_Component_2023,GO_Molecular_Function_2023'
```


हालाँकि दोनों ही मामलों में type `form-data` है, लेकिन बाद वाले मामले में कई parameters को comma से जोड़ा जाता है, जिससे उन्हें अलग करना आसान हो जाता है। इसलिए, स्पष्ट रूप से FORM का उपयोग करना बेहतर विकल्प है।
