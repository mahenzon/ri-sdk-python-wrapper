import dataclasses


@dataclasses.dataclass(frozen=True)
class ConnectorI2cStateResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # state - Указатель на код состояния i2c адаптера
    state: int
