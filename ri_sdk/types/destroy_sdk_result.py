import dataclasses


@dataclasses.dataclass(frozen=True)
class DestroySDKResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
