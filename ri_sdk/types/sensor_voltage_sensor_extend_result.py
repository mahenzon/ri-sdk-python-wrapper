import dataclasses


@dataclasses.dataclass(frozen=True)
class SensorVoltageSensorExtendResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # descriptor - Указатель на компонент датчика тока, напряжения и
    #    мощности, который получится в результате расширения
    descriptor: int
