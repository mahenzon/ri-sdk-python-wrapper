import dataclasses


@dataclasses.dataclass(frozen=True)
class ConnectorI2cReadBytesResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # buf - Указатель на массив байт, в который будет записаны
    #    прочитанные байты
    buf: bytes
    # readBytesLen - Указатель на количество прочитанных байтов
    read_bytes_len: int
