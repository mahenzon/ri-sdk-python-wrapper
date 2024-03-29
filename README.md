# RI SDK wrapper (autogenerated)

Parse RI SDK docs (https://docs.robointellect.ru/) and autogen Python wrapper.


[![PyPI - Version](https://img.shields.io/pypi/v/ri-sdk?style=for-the-badge&logo=pypi)](https://pypi.org/project/ri-sdk/)
[![PyPI - Status](https://img.shields.io/pypi/status/ri-sdk?style=for-the-badge)](https://pypi.org/project/ri-sdk/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ri-sdk?style=for-the-badge&logo=python)](https://pypi.org/project/ri-sdk/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge)](https://docs.astral.sh/ruff/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000?style=for-the-badge)](https://black.readthedocs.io/)
[![mypy](https://img.shields.io/badge/mypy-checked-1F5082?style=for-the-badge)](https://mypy.readthedocs.io/)
[![codecov](https://img.shields.io/codecov/c/github/mahenzon/ri-sdk-python-wrapper?token=K736Q6JF26&style=for-the-badge&logo=codecov)](https://codecov.io/gh/mahenzon/ri-sdk-python-wrapper)

### TODO:

- coverage for ri_sdk_codegen

### Install

```shell
pip install ri-sdk
```

### Run


#### Other examples
- GUI Control (PyQt / PySide) example: https://github.com/mahenzon/robohand-gui-control


#### Minimal example

Full example at [examples/robohand-example.py](https://github.com/mahenzon/ri-sdk-python-wrapper/blob/master/examples/robohand-example.py).

Another example with RoboHand class at [examples/robohand-class-example.py](https://github.com/mahenzon/ri-sdk-python-wrapper/blob/master/examples/robohand-class-example.py).

```python
"""
Смотри полный пример в папке examples
"""
from ri_sdk import RoboIntellectSDK, contrib

lib = contrib.get_lib()
ri_sdk = RoboIntellectSDK(
    lib=lib,
    setup_methods_args=True,
)
ri_sdk.init_sdk(log_level=1)
# pwm_descriptor = init_pwm(ri_sdk)
pwm_descriptor = 0
# i2c_descriptor = init_i2c(ri_sdk, pwm_descriptor)
i2c_descriptor = 0
# led_descriptor = init_led(ri_sdk, pwm_descriptor)
led_descriptor = 0

# Устанавливаем фиолетовый цвет светодиода
ri_sdk.exec_rgb_led_single_pulse(
    descriptor=led_descriptor,
    r=255,
    g=0,
    b=255,
    duration=0,
    run_async=True,
)

# инициализируем сервоприводы
# init_servos(ri_sdk, pwm_descriptor)

# переводим сервоприводы в стартовое положение
# servos_to_start_position(ri_sdk)

servo_rotate_descriptor = 0
# поворачиваем башню на угол 60 со скоростью 30
ri_sdk.exec_servo_drive_turn_with_relative_speed(
    descriptor=servo_rotate_descriptor,
    # угол 60º
    angle=60,
    # скорость в градусах в секунду
    speed=30,
)

# готовимся к завершению, включаем красный свет
ri_sdk.exec_rgb_led_single_pulse(
    descriptor=led_descriptor,
    r=255,
    g=0,
    b=0,
    duration=0,
    run_async=True,
)

# Красиво завершаем работу через destruct
# destruct(
#     ri_sdk=ri_sdk,
#     led_descriptor=led_descriptor,
#     pwm_descriptor=pwm_descriptor,
#     i2c_descriptor=i2c_descriptor,
# )
ri_sdk.destroy_sdk(is_force=True)
```

### Notes

#### Features to implement

- TODO: handy angle control (like in adafruit-servokit)
- TODO: code tests coverage


## Codegen

#### Install dependencies

```shell
poetry install
```

#### Full RI SDK codegen:

```shell
main.py --update-links --parse-docs --remove-unknown-methods-cache --generate-sdk
```

Each stage can be used separately:

- `--update-links`
- `--parse-docs [--remove-unknown-methods-cache]`
- `--generate-sdk`

Add `-v` flag for verbose output.


## Testing

Run tests

```shell
hatch run test:run
```

Run coverage

```shell
hatch run test:cov
```

Run coverage and export html report

```shell
hatch run test:cov-html
```
