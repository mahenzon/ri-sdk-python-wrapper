import dataclasses


@dataclasses.dataclass(frozen=True)
class SigmodPWMExtendResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # descriptor - Указатель на компонент ШИМ, который получится в
    #    результате расширения
    descriptor: int
