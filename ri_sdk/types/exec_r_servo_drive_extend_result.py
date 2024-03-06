import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecRServoDriveExtendResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # descriptor - Указатель на компонент сервопривода вращения,
    #    который получится в результате расширения
    descriptor: int
