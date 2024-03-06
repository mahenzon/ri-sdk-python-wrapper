import dataclasses


@dataclasses.dataclass(frozen=True)
class SigmodPWMReadByteResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # value - Указатель на байт для чтения
    value: bytes
