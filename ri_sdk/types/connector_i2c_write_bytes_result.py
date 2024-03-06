import dataclasses


@dataclasses.dataclass(frozen=True)
class ConnectorI2cWriteBytesResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # wroteBytesLen - Указатель на количество записаных байтов
    wrote_bytes_len: int
