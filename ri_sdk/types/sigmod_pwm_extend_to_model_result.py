import dataclasses


@dataclasses.dataclass(frozen=True)
class SigmodPWMExtendToModelResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # descriptor - Указатель на компонент ШИМ конкретной модели,
    #    который получится в результате расширения
    descriptor: int
