from pydantic import BaseModel


class MethodsOptions(BaseModel):
    names_overrides: dict[str, str] = {}
