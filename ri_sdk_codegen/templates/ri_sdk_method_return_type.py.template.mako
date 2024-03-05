import dataclasses
<%!
from ri_sdk_codegen.rendering.render_helpers import (
    receiver_var_comment,
)
%>

@dataclasses.dataclass(frozen=True)
class ${method.py_return_type_cls_name}:
    # Код ошибки. При успехе всегда 0
    error_code: int
    % for param in method.func_sdk_receivers:
${receiver_var_comment(param, indent_size=1)}
    ${param.py_name}: ${param.python_type}
    % endfor
