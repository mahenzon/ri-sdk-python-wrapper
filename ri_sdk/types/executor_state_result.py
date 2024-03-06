import dataclasses


@dataclasses.dataclass(frozen=True)
class ExecutorStateResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # state - Указатель на код состояния исполнителя
    state: int
