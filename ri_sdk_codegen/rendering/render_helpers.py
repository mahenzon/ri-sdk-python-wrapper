import textwrap
from functools import cache
from typing import TYPE_CHECKING

from ri_sdk_codegen.rendering.render_configs import (
    DEFAULT_MAX_WIDTH,
    IN_METHOD_COMMENT,
    IN_METHOD_SUBSEQUENT_COMMENT,
    PARAM_PREFIX_TEMPLATE,
    REGULAR_INDENT,
)
from ri_sdk_codegen.utils.case_converter import camel_case_to_snake_case

if TYPE_CHECKING:
    from ri_sdk_codegen.types import (
        MethodParamSDK,
        MethodSDK,
    )


@cache
def make_indent(indent_size: int) -> str:
    return indent_size * REGULAR_INDENT


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


def param_text_doc(
    p: "MethodParamSDK",
    max_width: int = DEFAULT_MAX_WIDTH,
    indent_size: int = 2,
    add_param_prefix: bool = True,
) -> str:
    if add_param_prefix:
        initial_indent_tpl = PARAM_PREFIX_TEMPLATE
        subsequent_indent_tpl = "{indent}"
    else:
        initial_indent_tpl = IN_METHOD_COMMENT
        subsequent_indent_tpl = f"{{indent}}#{REGULAR_INDENT}"

    return textwrap.fill(
        text=p.description,
        width=max_width,
        initial_indent=initial_indent_tpl.format(
            indent=make_indent(indent_size),
            name=p.py_name,
        ),
        subsequent_indent=subsequent_indent_tpl.format(
            indent=make_indent(indent_size + 1),
        ),
        fix_sentence_endings=True,
    )


def receiver_var_comment(
    p: "MethodParamSDK",
    max_width: int = DEFAULT_MAX_WIDTH,
    indent_size: int = 2,
) -> str:
    return textwrap.fill(
        text=p.description,
        width=max_width,
        initial_indent=IN_METHOD_COMMENT.format(
            indent=make_indent(indent_size),
            name=p.name,
        ),
        subsequent_indent=IN_METHOD_SUBSEQUENT_COMMENT.format(
            indent=make_indent(indent_size),
        ),
        fix_sentence_endings=True,
    )


def prepare_param_for_sdk_call(m: "MethodSDK", p: "MethodParamSDK") -> str:
    if m.is_auto_len_param(p):
        param_to_take_len = m.param_to_take_len_from(p)
        return f"len({param_to_take_len.py_name})"
    if p.py_ctype in ("c_uint8", "c_bool"):
        return f"ctypes.{p.py_ctype}({p.py_name})"
    if p.python_type in ("bool", "int", "float"):
        return p.py_name
    if p.python_type == "str":
        return f"{p.py_name}.encode()"
    if p.python_type == "bytes":
        if m.is_receive_type(p):
            return p.py_name
        else:
            return f"utils.convert_python_bytes_to_c_ulonglong({p.py_name})"
    msg = f"Unexpected python type {p.python_type!r} for method {m.name} param {p}"
    raise AssertionError(msg)


def prepare_param_for_sdk_call_result(
    m: "MethodSDK",
    p: "MethodParamSDK",
) -> str:
    if p.python_type == "bool":
        return f"bool({p.py_name})"
    if p.python_type in ("int", "float"):
        return f"{p.py_name}.value"
    if p.python_type == "bytes":
        if "[len]" in p.shared_object_type:
            # convert using len (as in docs)
            len_param: "MethodParamSDK" = m.param_u_long_long_length_param(p)
            return f"""utils.convert_c_ulonglong_of_len_to_python_bytes(
                {p.py_name},
                {len_param.py_name},
            )"""
        else:
            return f"utils.convert_c_ulonglong_to_python_bytes({p.py_name})"
    return p.py_name


def method_description(
    m: "MethodSDK",
    max_width: int = DEFAULT_MAX_WIDTH,
) -> str:
    prepared_string_blocks = (
        # call its own method
        block.process(max_width)
        # for each separate block
        for block in m.description_blocks
    )
    return "\n\n".join(prepared_string_blocks)
