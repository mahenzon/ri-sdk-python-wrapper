import dataclasses


@dataclasses.dataclass(frozen=True)
class SensorVoltageSensorReadRegBytesResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # buf - Указатель на массив байт для чтения
    buf: bytes
    # readBytesLen - Указатель на количество прочитанных байтов
    read_bytes_len: int
