import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecServoDriveExtendToModelResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # descriptor - Указатель на компонент сервопривода конкретной
    #    модели, который получится в результате расширения
    descriptor: int
