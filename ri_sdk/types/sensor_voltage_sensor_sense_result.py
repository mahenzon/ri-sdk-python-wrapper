import dataclasses


@dataclasses.dataclass(frozen=True)
class SensorVoltageSensorSenseResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # voltage - Указатель на значение напряжения в цепи (Вольт)
    voltage: float
    # voltageShunt - Указатель на значение напряжения на шунте
    #    (Вольт)
    voltage_shunt: float
    # current - Указатель на значение силы тока (Ампер)
    current: float
    # power - Указатель на значение мощности (Ватт)
    power: float
