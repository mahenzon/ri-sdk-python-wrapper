import logging
from dataclasses import dataclass

from ri_sdk import RoboIntellectSDK, contrib
from ri_sdk.exceptions import MethodCallError

# Инициализируем глобальные переменные

# адрес ШИМ по умолчанию
DEFAULT_PWM_ADDRESS = 0x40

# порты сервоприводов:
# порт сервопривода тела
SERVO_ROTATE_PORT = 0
# порт сервопривода правой стрелы (выпад вперед)
SERVO_CLAW_PORT = 1
# порт сервопривода левой стрелы (подъем)
SERVO_ARROW_R_PORT = 2
# порт сервопривода клешни
SERVO_ARROW_L_PORT = 3

# стартовые позиции:
# стартовая позиция тела
# (середина; меньше - левее, больше - правее)
# левее - против часовой стрелке
# правее - по часовой стрелке
BODY_START_PULSE = 1500
# стартовая позиция клешни
# (раскрытие: больше - шире)
CLAW_START_PULSE = 1500
# стартовая позиция правой стрелы
# (выпад вперед: меньше - дальше)
ARROW_R_START_PULSE = 2000
# стартовая позиция левой стрелы
# (подъем: меньше - выше)
ARROW_L_START_PULSE = 1000

# порты подключения светодиода:
RED_LED_PORT = 15
GREEN_LED_PORT = 14
BLUE_LED_PORT = 13


@dataclass
class ServoInfo:
    port: int
    descriptor: int
    start_position_pulse: int


servo_rotate = ServoInfo(
    port=SERVO_ROTATE_PORT,
    descriptor=0,
    start_position_pulse=BODY_START_PULSE,
)
servo_claw = ServoInfo(
    port=SERVO_CLAW_PORT,
    descriptor=0,
    start_position_pulse=CLAW_START_PULSE,
)
servo_pull = ServoInfo(
    port=SERVO_ARROW_R_PORT,
    descriptor=0,
    start_position_pulse=ARROW_R_START_PULSE,
)
servo_raise = ServoInfo(
    port=SERVO_ARROW_L_PORT,
    descriptor=0,
    start_position_pulse=ARROW_L_START_PULSE,
)


SERVOS = [
    servo_rotate,
    servo_claw,
    servo_pull,
    servo_raise,
]


def init_pwm(ri_sdk: RoboIntellectSDK) -> int:
    """
    Создаём компонент ШИМ с конкретной моделью
    как исполняемое устройство,
    получаем дескриптор сервопривода

    :param ri_sdk:
    :return:
    """
    create_pwm_result = ri_sdk.create_model_component(
        group="connector",
        device_name="pwm",
        model_name="pca9685",
    )
    return create_pwm_result.descriptor


def init_i2c(ri_sdk: RoboIntellectSDK, pwm_descriptor: int) -> int:
    """
    Создаём компонент i2c адаптера
    примитивное определение подключенной модели адаптера
    пробуем создать i2c адаптер модели ch341 и связать с ним ШИМ
    если не прокатило, то пробуем создать i2c адаптер модели cp2112

    :param pwm_descriptor:
    :param ri_sdk:
    :return:
    """
    create_i2c_result = ri_sdk.create_model_component(
        group="connector",
        device_name="i2c_adapter",
        model_name="ch341",
    )

    # связываем i2c адаптер с ШИМ по адресу 0x40
    try:
        ri_sdk.link_pwm_to_controller(
            descriptor=pwm_descriptor,
            to=create_i2c_result.descriptor,
            addr=DEFAULT_PWM_ADDRESS,
        )
    except MethodCallError:
        pass
    else:
        return create_i2c_result.descriptor

    create_i2c_result = ri_sdk.create_model_component(
        group="connector",
        device_name="i2c_adapter",
        model_name="cp2112",
    )

    # связываем i2c адаптер с ШИМ по адресу 0x40
    ri_sdk.link_pwm_to_controller(
        descriptor=pwm_descriptor,
        to=create_i2c_result.descriptor,
        addr=DEFAULT_PWM_ADDRESS,
    )
    return create_i2c_result.descriptor


def init_led(ri_sdk: RoboIntellectSDK, pwm_descriptor: int) -> int:
    """
    Создаём компонент светодиода с конкретной моделью (ky016)
    как исполняемое устройство и получаем дескриптор светодиода

    :param ri_sdk:
    :param pwm_descriptor:
    :return:
    """
    create_led_result = ri_sdk.create_model_component(
        group="executor",
        device_name="led",
        model_name="ky016",
    )
    # связываем светодиод с ШИМ,
    # передаем значения трех пинов к которым подключен светодиод
    ri_sdk.link_led_to_controller(
        descriptor=create_led_result.descriptor,
        pwm=pwm_descriptor,
        rport=RED_LED_PORT,  # red
        gport=GREEN_LED_PORT,  # green
        bport=BLUE_LED_PORT,  # blue
    )
    return create_led_result.descriptor


def init_servos(ri_sdk: RoboIntellectSDK, pwm_descriptor: int) -> None:
    """
    Создает сервоприводы и линкует их.
    Модифицирует объекты ServoInfo (обновляет дескриптор)
    """
    for servo in SERVOS:
        create_servo_result = ri_sdk.create_model_component(
            group="executor",
            device_name="servodrive",
            model_name="mg90s",
        )
        servo.descriptor = create_servo_result.descriptor
        ri_sdk.link_servodrive_to_controller(
            descriptor=create_servo_result.descriptor,
            pwm=pwm_descriptor,
            port=servo.port,
        )


def start_position(ri_sdk: RoboIntellectSDK, servo: ServoInfo) -> None:
    """
    Переводит сервопривод в стартовое положение.

    Выполняем поворот сервопривода в заданный угол,
    передаем дескриптор сервопривода, значение угла

    :param ri_sdk:
    :param servo:
    :return:
    """
    ri_sdk.exec_servo_drive_turn_by_pulse(
        descriptor=servo.descriptor,
        pulse=servo.start_position_pulse,
    )


def servos_to_start_position(ri_sdk: RoboIntellectSDK) -> None:
    """
    Проходим по известным сервам и устанавливаем в стартовую позицию

    :param ri_sdk:
    :return:
    """
    for servo in SERVOS:
        start_position(ri_sdk, servo)


def destruct_servos(ri_sdk: RoboIntellectSDK) -> None:
    """
    Уничтожает сервоприводы

    :param ri_sdk:
    :return:
    """
    for servo in SERVOS:
        ri_sdk.destroy_component(
            descriptor=servo.descriptor,
        )


def destruct(
    ri_sdk: RoboIntellectSDK,
    led_descriptor: int,
    pwm_descriptor: int,
    i2c_descriptor: int,
) -> None:
    """
    Красивое завершение через destruct - уничтожает все компоненты и библиотеку

    :param ri_sdk:
    :param led_descriptor:
    :param pwm_descriptor:
    :param i2c_descriptor:
    :return:
    """
    # уничтожаем сервоприводы
    destruct_servos(ri_sdk)

    # останавливаем свечение светодиода с определенным дескриптором
    ri_sdk.exec_rgb_led_stop(led_descriptor)
    # удаляем компонент светодиода по дескриптору
    ri_sdk.destroy_component(led_descriptor)

    # сбрасываем все порты на ШИМ
    ri_sdk.sigmod_pwm_reset_all(pwm_descriptor)
    # удаляем компонент ШИМ
    ri_sdk.destroy_component(pwm_descriptor)

    # удаляем компонент i2c
    ri_sdk.destroy_component(i2c_descriptor)

    # удаляем sdk со всеми компонентами в реестре компонентов
    ri_sdk.destroy_sdk(is_force=True)


def main() -> None:
    lib = contrib.get_lib()
    ri_sdk = RoboIntellectSDK(
        lib=lib,
        setup_methods_args=True,
    )
    ri_sdk.init_sdk(log_level=1)
    pwm_descriptor = init_pwm(ri_sdk)
    i2c_descriptor = init_i2c(ri_sdk, pwm_descriptor)
    led_descriptor = init_led(ri_sdk, pwm_descriptor)

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
    init_servos(ri_sdk, pwm_descriptor)

    # переводим сервоприводы в стартовое положение
    servos_to_start_position(ri_sdk)

    # поворачиваем башню на угол 75 со скоростью 30%
    ri_sdk.exec_servo_drive_turn_with_relative_speed(
        descriptor=servo_rotate.descriptor,
        # угол 75º
        angle=75,
        # Угловая скорость поворота (процент от максимальной скорости)
        speed=30,
    )

    # поднять башню на угол -40º со скоростью 50 г/с
    ri_sdk.exec_servo_drive_turn(
        descriptor=servo_raise.descriptor,
        # угол -40º
        angle=-40,
        # Угловая скорость поворота (градус / секунда)
        speed=50,
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
    destruct(
        ri_sdk=ri_sdk,
        led_descriptor=led_descriptor,
        pwm_descriptor=pwm_descriptor,
        i2c_descriptor=i2c_descriptor,
    )


if __name__ == "__main__":
    log_format = (
        "[%(asctime)s.%(msecs)03d] [%(name)s] "
        "%(module)s:%(lineno)d %(levelname)s - %(message)s"
    )
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
    )
    main()
