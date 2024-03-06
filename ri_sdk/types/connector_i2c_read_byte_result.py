import dataclasses


@dataclasses.dataclass(frozen=True)
class ConnectorI2cReadByteResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # value - Указатель на байт, в который запишется прочитанный байт
    value: bytes
