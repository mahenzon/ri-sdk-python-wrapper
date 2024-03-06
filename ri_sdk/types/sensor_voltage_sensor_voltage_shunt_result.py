import dataclasses


@dataclasses.dataclass(frozen=True)
class SensorVoltageSensorVoltageShuntResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # voltageShunt - Указатель на значение напряжения на шунте
    #    (Вольт)
    voltage_shunt: float
