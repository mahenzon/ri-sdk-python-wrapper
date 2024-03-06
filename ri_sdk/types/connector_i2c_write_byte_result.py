import dataclasses


@dataclasses.dataclass(frozen=True)
class ConnectorI2cWriteByteResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
