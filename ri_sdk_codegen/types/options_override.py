from typing import Literal

from pydantic import BaseModel, Field


class ParamOptions(BaseModel):
    direction: Literal["input", "output"] | None = None
    auto_len: str | None = Field(
        default=None,
        description="If set, find var named after this value "
        "and replace it with automatically calculated value based on the param name",
    )


class MethodOptions(BaseModel):
    params: dict[str, ParamOptions] = {}
