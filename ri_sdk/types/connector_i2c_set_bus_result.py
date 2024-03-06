import dataclasses


@dataclasses.dataclass(frozen=True)
class ConnectorI2cSetBusResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # nextBus - Указатель на установленный номер шины
    next_bus: int
    # prevBus - Указатель на предыдущий номер шины
    prev_bus: int
