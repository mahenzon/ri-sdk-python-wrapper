from __future__ import annotations

import ctypes
from typing import TYPE_CHECKING, Union

from ri_sdk import loggers
from ri_sdk.exceptions import MethodCallError

if TYPE_CHECKING:
    from typing import Protocol, TypeVar

    ErrorBufferType = TypeVar("ErrorBufferType", bound=ctypes.Array[ctypes.c_char])

    class MethodProtocol(Protocol):
        # method definitely has __name__ attribute
        __name__: str

        # method's call protocol looks like this:
        def __call__(self, *args: ArgsType | ErrorBufferType) -> int:
            pass


ArgsType = Union[
    int,
    bool,
    float,
    bytes,
    ctypes.c_uint8,
    ctypes.c_int,
    ctypes.c_bool,
    ctypes.c_float,
    ctypes.c_char_p,
    ctypes.c_ulonglong,
]


log = loggers.wrapper


class RoboIntellectBaseSDK:
    def __init__(
        self,
        lib: ctypes.CDLL,
    ) -> None:
        """
        :param lib: RI SDK library .dll or .so
        """
        self.lib = lib
        log.debug("Initialized RI SDK")

    @classmethod
    def process_result(
        cls,
        error_code: int,
        error_text_c: ErrorBufferType,
        method_name: str,
    ) -> None:
        """
        :param error_code:
        :param error_text_c:
        :param method_name:
        :return: None if error code is 0. otherwise raises
        :raises: MethodCallError
        """
        if not error_code:
            return

        log.debug("Non-zero error code %s for method %r", error_code, method_name)
        raise MethodCallError(
            error_code=error_code,
            error_message=error_text_c.raw,
            method_name=method_name,
        )

    def call_sdk_method(
        self,
        method: MethodProtocol,
        *args: ArgsType,
    ) -> int:
        """
        Вызывает метод, передавая ему все прокинутые аргументы.
        Если статус 0, возвращает этот статус.
        Если статус не 0, выкидывает исключение MethodCallError

        :param method: метод RI SDK
        :param args: all method args to be passed
        :return: error code
        :raises: MethodCallError
        """
        # error_text_c - Текст ошибки. Передается как параметр
        # если происходит ошибка, метод записывает текст в этот параметр
        error_text_c = ctypes.create_string_buffer(1000)
        # Код ошибки. Получаем по результату вызова метода
        error_code = method(*args, error_text_c)
        self.process_result(
            error_code=error_code,
            error_text_c=error_text_c,
            method_name=method.__name__,
        )
        return error_code
