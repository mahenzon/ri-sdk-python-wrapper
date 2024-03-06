import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecServoDriveCustomDeviceInitResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
