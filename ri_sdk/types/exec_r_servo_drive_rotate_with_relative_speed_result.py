import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecRServoDriveRotateWithRelativeSpeedResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
