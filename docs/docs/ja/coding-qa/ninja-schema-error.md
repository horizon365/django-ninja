`ninja_schema` の schema と `ninja` 内の schema は全く違うもののように感じます — ninja の方は動作するのに、`ninja_schema` の方はエラーが発生します
==========================================================

A: `ninja_schema` は独立したパッケージですか？
B: はい、pip でインストールする必要があります。ソースコードを見たところ、pydantic からいくつかのものを取り込んでいるようです。しかし私は pydantic を理解していないので、新しく追加されたものがどんな機能を実装しているのか正確にはわかりません。

A: 私は ninja の schema で十分だと思います。
B: 外部キーの出力をフラット化する場合、ドキュメントでは次のように使われています：`owner_first_name: str = Field(None, alias="owner.first_name")`
B: `ninja_schema` のものを使うと、入力は `str` であるべきなのにオブジェクトが与えられている、というエラーが出続けます。
B: まさかこの `ninja_schema` の `Schema` が原因だったとは思いませんでした。
