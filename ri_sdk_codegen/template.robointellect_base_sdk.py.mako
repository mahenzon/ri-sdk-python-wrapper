import ctypes
from typing import NoReturn
<%!
from ri_sdk_codegen.rendering.render_helpers import (
    lib_ctype_param,
    function_param,
    function_param_doc,
    receiver_var_comment,
    sdk_call_param_convert,
    method_description,
    comment_ctype_param,
)
%>

class RoboIntellectBaseSDK:
    def __init__(self, lib: ctypes.CDLL) -> None:
        self.lib = lib

    @classmethod
    def raise_on_error(cls, error_text_c: ctypes.Array) -> NoReturn:
        """
        # todo: more details?

        :param error_text_c:
        :return:
        """
        raise ValueError(error_text_c.raw.decode())

    @classmethod
    def process_result(
        cls,
        error_code: int,
        error_text_c: ctypes.Array,
    ) -> None:
        """
        :param error_code:
        :param error_text_c:
        :return:
        """
        if error_code:
            cls.raise_on_error(error_text_c)
% for sdk_method in sdk_methods:

    def ${sdk_method.py_method_name}(
        self,
    % for param in sdk_method.func_call_params:
        ${function_param(param)},
    % endfor
    ) -> ${sdk_method.py_method_return_type}:
        ${'"""'}
${method_description(sdk_method)}

        ${sdk_method.url}

    % for param in sdk_method.func_call_params:
${function_param_doc(param)}
    % endfor
        # TODO: describe return value
        ${'"""'}
        # Инициализация получателей
        % for param in sdk_method.func_sdk_receivers:
% if loop.first:
## empty line for spacing

% endif
${receiver_var_comment(param)}
        ${param.py_name} = ctypes.${param.py_ctype}()
% if loop.last:
## empty line for spacing

% endif
        % endfor
        # Текст ошибки. Передается как параметр
        # если происходит ошибка, метод записывает текст в этот параметр
        error_text_c = ctypes.create_string_buffer(1000)
        # Код ошибки
        error_code = self.lib.${sdk_method.name}(
        % for param in sdk_method.func_sdk_call_args:
            ${param.py_name}${sdk_call_param_convert(param)},
        % endfor
            error_text_c,
        )
        self.process_result(error_code, error_text_c)
        ## return ${sdk_method.py_method_return_value}
        return (
            error_code,
            % for param in sdk_method.func_sdk_receivers:
            ${param.py_name},
            % endfor
        )
% endfor
% for sdk_method in sdk_methods:

    def setup_arg_types_for_${sdk_method.py_method_name}(self) -> None:
        ${'"""'}
        Инициализация метода ${sdk_method.name}

        Обращение и документация:
        >>> self.${sdk_method.py_method_name}

        ${sdk_method.url}
        ${'"""'}

        self.lib.${sdk_method.name}.argtypes = [
        % for param in sdk_method.params:
        % if param.name != 'errorCode':
            ${comment_ctype_param(param)}
            ${lib_ctype_param(param)},
        % endif
        % endfor
        ]
% endfor
