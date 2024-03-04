from functools import cached_property

from pydantic import BaseModel

from ri_sdk_codegen.rendering.render_helpers import create_param_python_name
from ri_sdk_codegen.types.constants import (
    KNOWN_TYPES,
    TYPES_TO_C_TYPE_MAP,
    TYPES_TO_PYTHON_TYPE_MAP,
)


class BaseParam(BaseModel):
    py_ctype: str


class MethodParamSDK(BaseParam):
    name: str
    python_type: str
    shared_object_type: str
    description: str

    is_pointer: bool = False
    pointer_py_ctype: str = "POINTER"

    @cached_property
    def py_name(self) -> str:
        return create_param_python_name(self.name)

    @classmethod
    def from_info(
        cls,
        name: str,
        shared_object_type: str,
        description: str,
    ) -> "MethodParamSDK":
        is_pointer = False
        if shared_object_type.startswith("*"):
            is_pointer = True
        if shared_object_type not in KNOWN_TYPES:
            msg = f"Unrecognized shared_object_type: {shared_object_type!r}"
            raise ValueError(msg)

        py_ctype = TYPES_TO_C_TYPE_MAP[shared_object_type]
        python_type = TYPES_TO_PYTHON_TYPE_MAP[shared_object_type]
        return cls(
            name=name,
            py_ctype=py_ctype,
            python_type=python_type,
            shared_object_type=shared_object_type,
            description=description,
            is_pointer=is_pointer,
        )
