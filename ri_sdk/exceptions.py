class BaseRiSDKException(Exception):
    pass


class MethodCallError(BaseRiSDKException):
    def __init__(
        self,
        error_code: int,
        error_message: bytes,
        method_name: str,
    ) -> None:
        stripped_error_message = self.stripped_bytes(error_message)
        super().__init__(error_code, stripped_error_message, method_name)
        self.original_error_message = error_message
        self.error_message = stripped_error_message
        self.error_code = error_code
        self.method_name = method_name

    @classmethod
    def stripped_bytes(cls, error: bytes) -> bytes:
        """
        Читаем байты до первого нулевого.
        Изначально строка задаётся длиной 1000 символов.
        Текст ошибки займёт 100-200-300 символов. Остальное -- нули.

        Читаем до первого нуля, остальное нас не интересует.

        :param error:
        :return: Bytes until zero
        """
        for idx, byte in enumerate(error):
            if byte == 0:
                return error[:idx]
        return error

    @property
    def message_as_text(self) -> str:
        return self.error_message.decode()
