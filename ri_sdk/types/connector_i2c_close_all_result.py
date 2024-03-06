import dataclasses


@dataclasses.dataclass(frozen=True)
class ConnectorI2cCloseAllResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
