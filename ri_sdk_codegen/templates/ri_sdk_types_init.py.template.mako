"""
Autogenerated!
Do not edit manually.
## this is the template. it may and should be edited manually.
"""

__all__ = (
% for method in sdk_methods:
    "${method.py_return_type_cls_name}",
% endfor
)

% for method in sdk_methods:
from .${method.py_module_name} import ${method.py_return_type_cls_name}
% endfor
