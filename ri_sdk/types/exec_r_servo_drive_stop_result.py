import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecRServoDriveStopResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
