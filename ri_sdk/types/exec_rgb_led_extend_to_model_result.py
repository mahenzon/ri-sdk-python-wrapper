import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecRGBLEDExtendToModelResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # descriptor - Указатель на компонент светодиода конкретной
    #    модели, который получится в результате расширения
    descriptor: int
