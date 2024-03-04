from typing import Literal

from pydantic import BaseModel


class ParamOptions(BaseModel):
    direction: Literal["input", "output"] | None = None


class MethodOptions(BaseModel):
    params: dict[str, ParamOptions] = {}
