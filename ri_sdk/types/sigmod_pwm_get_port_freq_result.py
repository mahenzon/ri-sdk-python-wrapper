import dataclasses


@dataclasses.dataclass(frozen=True)
class SigmodPWMGetPortFreqResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # freq - Указатель на частоту ШИМ на порту port
    freq: int
