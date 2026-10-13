ninja_schema和ninja里面的shcema感觉有很大不同啊，ninja的能跑，ninja_schema里面的就报错了
==========================================================

A: ninja_schema是另一个包？
B: 嗯，需要pip，看了下源码，感觉是从pydantic那里又弄了些东西进来，但是pydantic不懂，新加的东西具体实现了哪些功能不是很确定

A: 我觉得ninja的schema挺够用了
B: 外键的展平输出，文档上这么用：owner_first_name: str = Field(None, alias="owner.first_name")
B: 用了ninja_schema的一直报错，提示输入的要是str，但是给到的是对象
B: 死活没想到是ninja_schema的这个Schema导致的