import ctypes
from typing import NoReturn
<%! 
from ri_sdk_codegen.render_helpers import (
    lib_ctype_param,
    function_param,
    function_param_doc,
    sdk_call_param,
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
    def process_result(cls, error_code: int, error_text_c: ctypes.Array) -> int:
        """
        :param error_code:
        :param error_text_c:
        :return:
        """
        if not error_code:
            return error_code
        cls.raise_on_error(error_text_c)
% for sdk_method in sdk_methods:

    def ${sdk_method.py_method_name}(
        self,
    % for param in sdk_method.params:
    % if param.name not in ('errorCode', 'errorText'):
        ${function_param(param)},
    % endif
    % endfor
    ) -> int:
        ${'"""'}
${method_description(sdk_method)}

        ${sdk_method.url}

    % for param in sdk_method.params:
    % if param.name not in ('errorCode', 'errorText'):
${function_param_doc(param)}
    % endif
    % endfor
        ${'"""'}

        # Текст ошибки. Передается как параметр
        # если происходит ошибка, метод записывает текст в этот параметр
        error_text_c = ctypes.create_string_buffer(1000)
        # Код ошибки
        error_code = self.lib.${sdk_method.name}(
        % for param in sdk_method.params:
        % if param.name not in ('errorCode', 'errorText'):
            ${sdk_call_param(param)}${sdk_call_param_convert(param)},
        % endif
        % endfor
            error_text_c,
        )
        return self.process_result(error_code, error_text_c)
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
