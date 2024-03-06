import dataclasses


@dataclasses.dataclass(frozen=True)
class SensorVoltageSensorExtendToModelResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # descriptor - Указатель на компонент датчика тока, напряжения и
    #    мощности конкретной модели, который получится в результате
    #    расширения
    descriptor: int
