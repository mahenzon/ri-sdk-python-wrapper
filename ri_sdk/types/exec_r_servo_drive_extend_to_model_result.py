import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecRServoDriveExtendToModelResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # descriptor - Указатель на компонент сервопривода вращения
    #    конкретной модели, который получится в результате расширения
    descriptor: int
