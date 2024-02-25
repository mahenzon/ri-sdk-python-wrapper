import textwrap
from functools import partial
from typing import TYPE_CHECKING

from utils.case_converter import camel_case_to_snake_case

if TYPE_CHECKING:
    from ri_sdk_codegen.types import (
        MethodParamSDK,
        MethodSDK,
    )

FUNC_BODY_INDENT = " " * 2 * 4
PARAM_PREFIX_TEMPLATE = f"{FUNC_BODY_INDENT}:param {{name}}: "
PARAM_SUBSEQUENT_INDENT = " " * 3 * 4


def create_param_python_name(name: str) -> str:
    if name == "exec":
        return "executor"
    if name == "async":
        return "run_async"
    if name == "len":
        return "length"
    return camel_case_to_snake_case(name)


def comment_ctype_param(p: "MethodParamSDK") -> str:
    return f"# name: {p.name}; object type: {p.shared_object_type}"


def lib_ctype_param(p: "MethodParamSDK") -> str:
    line = f"ctypes.{p.py_ctype}"
    if p.is_pointer:
        line = f"ctypes.{p.pointer_py_ctype}({line})"
    return line


def function_param(p: "MethodParamSDK") -> str:
    line = f"{p.py_name}: {p.python_type}"
    if p.name == "async":
        line += " = False"
    return line


def function_param_doc(p: "MethodParamSDK", max_with=69) -> str:
    return textwrap.fill(
        text=p.description,
        width=max_with,
        initial_indent=PARAM_PREFIX_TEMPLATE.format(name=p.py_name),
        subsequent_indent=PARAM_SUBSEQUENT_INDENT,
        fix_sentence_endings=True,
    )


def sdk_call_param(p: "MethodParamSDK"):
    return p.py_name


def sdk_call_param_convert(p: "MethodParamSDK") -> str:
    if p.py_ctype == "c_char_p":
        return ".encode()"
    return ""


def method_description(m: "MethodSDK", max_with=69) -> str:
    fill = partial(
        textwrap.fill,
        width=max_with,
        initial_indent=FUNC_BODY_INDENT,
        subsequent_indent=FUNC_BODY_INDENT,
        fix_sentence_endings=True,
        drop_whitespace=True,
        replace_whitespace=False,
    )
    filled_paragraphs = list(map(fill, m.description_blocks))
    return "\n\n".join(filled_paragraphs)
