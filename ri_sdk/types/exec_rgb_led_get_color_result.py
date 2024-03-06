import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecRGBLEDGetColorResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # r - Указатель на значение яркости для красного цвета (0 -255)
    r: int
    # g - Указатель на значение яркости для зеленого цвета (0 -255)
    g: int
    # b - Указатель на значение яркости для синего цвета (0 -255)
    b: int
