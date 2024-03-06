import dataclasses


@dataclasses.dataclass(frozen=True)
class LinkVoltageSensorToControllerResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
