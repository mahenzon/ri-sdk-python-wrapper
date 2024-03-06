import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecServoDriveStopResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
