import dataclasses


@dataclasses.dataclass(frozen=True)
class SensorVoltageSensorCurrentResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # current - Указатель на значение силы тока (Ампер)
    current: float
