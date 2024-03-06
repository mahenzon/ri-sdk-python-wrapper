import dataclasses


@dataclasses.dataclass(frozen=True)
class SigmodPWMGetResolutionResult:
    # Код ошибки. При успехе всегда 0
    error_code: int
    # resolution - Указатель на разрешение ШИМ
    resolution: int
