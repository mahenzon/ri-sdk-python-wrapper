import dataclasses


@dataclasses.dataclass(frozen=True)
class SigmodPWMGetPortDutyCycleResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # on - Указатель на количество тактов до перевода выхода в
    #    состояние логической «1»
    on: int
    # off - Указатель на количество тактов до перевода выхода в
    #    состояние логического «0»
    off: int
