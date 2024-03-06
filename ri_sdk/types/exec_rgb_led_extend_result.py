import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecRGBLEDExtendResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # descriptor - Указатель на компонент светодиода, который
    #    получится в результате расширения
    descriptor: int
