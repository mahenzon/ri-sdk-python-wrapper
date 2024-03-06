import dataclasses


@dataclasses.dataclass(frozen=True)
class SensorVoltageSensorWriteRegBytesResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # wroteBytesLen - Указатель на количество записанных байтов
    wrote_bytes_len: int
