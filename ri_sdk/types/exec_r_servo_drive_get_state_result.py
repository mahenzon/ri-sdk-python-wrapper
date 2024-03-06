import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecRServoDriveGetStateResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # state - Указатель код состояния сервопривода
    state: int
