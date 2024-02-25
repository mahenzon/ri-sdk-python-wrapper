import textwrap
from typing import TYPE_CHECKING

from ri_sdk_codegen.rendering.render_configs import (
    IN_FUNCTION_COMMENT,
    IN_FUNCTION_SUBSEQUENT_COMMENT,
    PARAM_PREFIX_TEMPLATE,
    PARAM_SUBSEQUENT_INDENT,
)
from ri_sdk_codegen.utils.case_converter import camel_case_to_snake_case

if TYPE_CHECKING:
    from ri_sdk_codegen.types import (
        MethodParamSDK,
        MethodSDK,
    )


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
    # TODO: Union[py_type, py_ctype]?
    line = f"{p.py_name}: {p.python_type}"
    if p.name == "async":
        line += " = False"
    return line


def function_param_doc(p: "MethodParamSDK", max_with: int = 69) -> str:
    return textwrap.fill(
        text=p.description,
        width=max_with,
        initial_indent=PARAM_PREFIX_TEMPLATE.format(name=p.py_name),
        subsequent_indent=PARAM_SUBSEQUENT_INDENT,
        fix_sentence_endings=True,
    )


def receiver_var_comment(p: "MethodParamSDK", max_with: int = 69) -> str:
    return textwrap.fill(
        text=p.description,
        width=max_with,
        initial_indent=IN_FUNCTION_COMMENT.format(name=p.name),
        subsequent_indent=IN_FUNCTION_SUBSEQUENT_COMMENT,
        fix_sentence_endings=True,
    )


def sdk_call_param_convert(p: "MethodParamSDK") -> str:
    if p.py_ctype == "c_char_p":
        return ".encode()"
    return ""


def method_description(m: "MethodSDK", max_width: int = 69) -> str:
    prepared_string_blocks = (
        # call its own method
        block.process(max_width)
        # for each separate block
        for block in m.description_blocks
    )
    return "\n\n".join(prepared_string_blocks)
