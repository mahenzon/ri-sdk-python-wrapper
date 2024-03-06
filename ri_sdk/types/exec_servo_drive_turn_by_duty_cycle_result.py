import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecServoDriveTurnByDutyCycleResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
