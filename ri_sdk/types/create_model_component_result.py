import dataclasses


@dataclasses.dataclass(frozen=True)
class CreateModelComponentResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # descriptor - Указатель на компонент, который будет создан
    descriptor: int
