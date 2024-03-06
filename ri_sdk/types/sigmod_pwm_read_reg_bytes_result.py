import dataclasses


@dataclasses.dataclass(frozen=True)
class SigmodPWMReadRegBytesResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # buf - Указатель на массив байт для чтения
    buf: bytes
    # readBytesLen - Указатель на количество записанных байтов
    read_bytes_len: int
