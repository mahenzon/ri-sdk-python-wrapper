import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecServoDriveGetStateResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # state - Указатель на код состояния сервопривода
    state: int
