import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecServoDriveGetCurrentAngleResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # angle - Указатель на код состояния сервопривода
    angle: int
