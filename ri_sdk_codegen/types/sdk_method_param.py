from functools import cached_property

from pydantic import BaseModel

from ri_sdk_codegen.rendering.render_helpers import create_param_python_name
from ri_sdk_codegen.types.constants import (
    KNOWN_TYPES,
    SERVICE_PARAMS_NAMES,
    TYPES_TO_C_TYPE_MAP,
    TYPES_TO_PYTHON_TYPE_MAP,
    KnownCPythonTypes,
    KnownPythonTypes,
    KnownSharedTypesType,
)


class BaseParam(BaseModel):
    name: str
    python_type: KnownPythonTypes
    py_ctype: KnownCPythonTypes
    shared_object_type: KnownSharedTypesType
    description: str


class MethodParamSDK(BaseParam):
    is_pointer: bool = False
    pointer_py_ctype: str = "POINTER"

    @cached_property
    def py_name(self) -> str:
        return create_param_python_name(self.name)

    @cached_property
    def is_service_param(self) -> bool:
        return self.name in SERVICE_PARAMS_NAMES

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

        known_shared_type: KnownSharedTypesType = shared_object_type  # type: ignore[assignment]
        assert known_shared_type in KNOWN_TYPES

        py_ctype = TYPES_TO_C_TYPE_MAP[known_shared_type]
        python_type = TYPES_TO_PYTHON_TYPE_MAP[known_shared_type]
        return cls(
            name=name,
            py_ctype=py_ctype,
            python_type=python_type,
            shared_object_type=known_shared_type,
            description=description,
            is_pointer=is_pointer,
        )
