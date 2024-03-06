import dataclasses


@dataclasses.dataclass(frozen=True)
class SigmodPWMGetFreqResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # freq - Указатель на частоту ШИМ
    freq: int
