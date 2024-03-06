import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecRServoDriveCustomDeviceInitResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
