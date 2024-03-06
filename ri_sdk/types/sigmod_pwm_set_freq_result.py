import dataclasses


@dataclasses.dataclass(frozen=True)
class SigmodPWMSetFreqResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
