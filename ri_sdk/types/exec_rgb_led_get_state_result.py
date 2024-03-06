import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecRGBLEDGetStateResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # state - Указатель на код состояния светодиода
    state: int
