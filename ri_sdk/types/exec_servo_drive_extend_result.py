import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecServoDriveExtendResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # descriptor - Указатель на компонент сервопривода, который
    #    получится в результате расширения
    descriptor: int
