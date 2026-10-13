`ninja_schema` and the schema inside `ninja` feel very different — ninja's works, but the one in `ninja_schema` raises an error
==========================================================

A: Is `ninja_schema` a separate package?
B: Yes, it needs to be pip-installed. I looked at the source code, and it seems to have pulled some things in from pydantic. But I don't understand pydantic, so I'm not sure exactly what functionality the newly added things implement.

A: I think ninja's schema is more than enough.
B: For flattening foreign key output, the documentation uses it like this: `owner_first_name: str = Field(None, alias="owner.first_name")`
B: Using the one from `ninja_schema` keeps raising an error, saying the input should be a `str`, but what's given is an object.
B: I never expected that this `Schema` from `ninja_schema` was the cause.
