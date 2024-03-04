import typing
from typing import Literal

KnownPythonTypes = Literal[
    "bool",
    "int",
    "float",
    "str",
    "bytes",
]

KnownCPythonTypes = Literal[
    "c_bool",
    "c_uint8",
    "c_int",
    "c_float",
    "c_char_p",
    "c_ulonglong",
]

KnownSharedTypesType = Literal[
    "bool (тип C)",
    "uint8_t (тип C)",
    "int (тип C)",
    "*int (тип C)",
    "float (тип C)",
    "*float (тип C)",
    "char[] (тип C)",
    "char[1000] (тип C)",
    "*long long unsigned (тип C)",
    "*long long unsigned[len] (тип C)",
]

KNOWN_TYPES: set[KnownSharedTypesType] = set(
    typing.get_args(KnownSharedTypesType),
)


# shared object type to python ctype
TYPES_TO_C_TYPE_MAP: dict[KnownSharedTypesType, KnownCPythonTypes] = {
    "bool (тип C)": "c_bool",
    "uint8_t (тип C)": "c_uint8",
    "int (тип C)": "c_int",
    "*int (тип C)": "c_int",
    "float (тип C)": "c_float",
    "*float (тип C)": "c_float",
    "char[] (тип C)": "c_char_p",
    "char[1000] (тип C)": "c_char_p",
    "*long long unsigned (тип C)": "c_ulonglong",
    "*long long unsigned[len] (тип C)": "c_ulonglong",
}

# shared object type to python native type
TYPES_TO_PYTHON_TYPE_MAP: dict[KnownSharedTypesType, KnownPythonTypes] = {
    "bool (тип C)": "bool",
    "uint8_t (тип C)": "int",
    "int (тип C)": "int",
    "*int (тип C)": "int",
    "float (тип C)": "float",
    "*float (тип C)": "float",
    "char[] (тип C)": "str",
    "char[1000] (тип C)": "str",
    "*long long unsigned (тип C)": "bytes",
    "*long long unsigned[len] (тип C)": "bytes",
}


# TODO: assert KNOWN_TYPES contains all known
#  and other maps contain all from KNOWN_TYPES

# TODO: tests
assert set(TYPES_TO_C_TYPE_MAP) == KNOWN_TYPES
assert set(TYPES_TO_PYTHON_TYPE_MAP) == KNOWN_TYPES

SERVICE_PARAMS_NAMES = {
    "errorCode",
    "errorText",
}
