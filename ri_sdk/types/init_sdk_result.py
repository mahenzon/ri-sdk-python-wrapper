import dataclasses


@dataclasses.dataclass(frozen=True)
class InitSDKResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
