import dataclasses


@dataclasses.dataclass(frozen=True)
class SensorVoltageSensorPowerResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # power - Указатель на значение мощности (Ватт)
    power: float
