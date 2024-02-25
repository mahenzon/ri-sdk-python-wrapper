from dataclasses import dataclass

from ri_sdk_codegen.rendering.render_helpers import create_param_python_name
from ri_sdk_codegen.rendering.text_blocks import DescriptionBlockBase
from ri_sdk_codegen.utils import method_name_to_snake_case

KNOWN_TYPES: set[str] = {
    "*int (тип C",
    "*int (тип C)",
    "*long long unsigned  (тип C)",
    "*long long unsigned (тип C)",
    "*long long unsigned[len]  (тип C)",
    "bool (тип C)",
    "bool(тип C)",
    "char[1000] (тип C)",
    "char[] (тип C)",
    "float (тип C)",
    "int (тип C",
    "int (тип C)",
    "long long unsigned  (тип C)",
    "long long unsigned (тип C)",
    "uint8_t (тип C)",
}


# shared object type to python ctype
TYPES_TO_C_TYPE_MAP: dict[str, str] = {
    "*int (тип C": "c_int",
    "*int (тип C)": "c_int",
    "*long long unsigned  (тип C)": "c_ulonglong",
    "*long long unsigned (тип C)": "c_ulonglong",
    "*long long unsigned[len]  (тип C)": "c_ulonglong",
    "bool (тип C)": "c_bool",
    "bool(тип C)": "c_bool",
    "char[1000] (тип C)": "c_char_p",
    "char[] (тип C)": "c_char_p",
    "float (тип C)": "c_float",
    "int (тип C": "c_int",
    "int (тип C)": "c_int",
    "long long unsigned  (тип C)": "c_ulonglong",
    "long long unsigned (тип C)": "c_ulonglong",
    "uint8_t (тип C)": "c_uint8",
}

# shared object type to python native type
TYPES_TO_PYTHON_TYPE_MAP: dict[str, str] = {
    "*int (тип C": "int",
    "*int (тип C)": "int",
    "*long long unsigned  (тип C)": "bytes",
    "*long long unsigned (тип C)": "bytes",
    "*long long unsigned[len]  (тип C)": "bytes",
    "bool (тип C)": "bool",
    "bool(тип C)": "bool",
    "char[1000] (тип C)": "str",
    "char[] (тип C)": "str",
    "float (тип C)": "float",
    "int (тип C": "int",
    "int (тип C)": "int",
    "long long unsigned  (тип C)": "bytes",
    "long long unsigned (тип C)": "bytes",
    "uint8_t (тип C)": "int",
}


@dataclass
class BaseParam:
    py_ctype: str

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        param_type = kwargs.get("type")
        if param_type is None:
            msg = "Parameter type should not be None"
            raise ValueError(msg)
        cls.__param_type__ = param_type

    @property
    def type(self) -> str:
        return self.__param_type__


@dataclass
class MethodParamSDK(BaseParam, type="generic"):
    name: str
    python_type: str
    shared_object_type: str
    description: str

    is_pointer: bool = False
    pointer_py_ctype: str = "POINTER"

    @property
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
        if shared_object_type.strip().startswith("*"):
            is_pointer = True
        py_ctype = TYPES_TO_C_TYPE_MAP[shared_object_type]
        python_type = TYPES_TO_PYTHON_TYPE_MAP[shared_object_type]
        # lol
        # ruff: noqa: RUF003
        # replace cyrillic "с" with latin "c"
        name = name.replace(chr(1089), chr(99))
        return cls(
            name=name,
            py_ctype=py_ctype,
            python_type=python_type,
            shared_object_type=shared_object_type,
            description=description,
            is_pointer=is_pointer,
        )


@dataclass
class MethodSDK:
    name: str
    url: str
    description_blocks: list[DescriptionBlockBase]
    params: list[MethodParamSDK]

    @property
    def py_method_name(self):
        return method_name_to_snake_case(self.name).removeprefix("ri_sdk_")
