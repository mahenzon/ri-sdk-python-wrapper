import logging
from ctypes import CDLL
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


class RoboHand:
    def __init__(self, lib: CDLL) -> None:
        self.ri_sdk = RoboIntellectSDK(
            lib=lib,
            setup_methods_args=True,
        )
        self.ri_sdk.init_sdk(log_level=1)

        self.servo_rotate = ServoInfo(
            port=SERVO_ROTATE_PORT,
            descriptor=0,
            start_position_pulse=BODY_START_PULSE,
        )
        self.servo_claw = ServoInfo(
            port=SERVO_CLAW_PORT,
            descriptor=0,
            start_position_pulse=CLAW_START_PULSE,
        )
        self.servo_pull = ServoInfo(
            port=SERVO_ARROW_R_PORT,
            descriptor=0,
            start_position_pulse=ARROW_R_START_PULSE,
        )
        self.servo_raise = ServoInfo(
            port=SERVO_ARROW_L_PORT,
            descriptor=0,
            start_position_pulse=ARROW_L_START_PULSE,
        )

        self.servos = [
            self.servo_rotate,
            self.servo_claw,
            self.servo_pull,
            self.servo_raise,
        ]

        self.pwm_descriptor = self.init_pwm()
        self.i2c_descriptor = self.init_i2c()
        self.led_descriptor = self.init_led()

    def init_pwm(self) -> int:
        """
        Создаём компонент ШИМ с конкретной моделью
        как исполняемое устройство,
        получаем дескриптор сервопривода

        :return:
        """
        create_pwm_result = self.ri_sdk.create_model_component(
            group="connector",
            device_name="pwm",
            model_name="pca9685",
        )
        return create_pwm_result.descriptor

    def init_i2c(self) -> int:
        """
        Создаём компонент i2c адаптера
        примитивное определение подключенной модели адаптера
        пробуем создать i2c адаптер модели ch341 и связать с ним ШИМ
        если не прокатило, то пробуем создать i2c адаптер модели cp2112

        :return:
        """
        create_i2c_result = self.ri_sdk.create_model_component(
            group="connector",
            device_name="i2c_adapter",
            model_name="ch341",
        )

        # связываем i2c адаптер с ШИМ по адресу 0x40
        try:
            self.ri_sdk.link_pwm_to_controller(
                descriptor=self.pwm_descriptor,
                to=create_i2c_result.descriptor,
                addr=DEFAULT_PWM_ADDRESS,
            )
        except MethodCallError:
            pass
        else:
            return create_i2c_result.descriptor

        create_i2c_result = self.ri_sdk.create_model_component(
            group="connector",
            device_name="i2c_adapter",
            model_name="cp2112",
        )

        # связываем i2c адаптер с ШИМ по адресу 0x40
        self.ri_sdk.link_pwm_to_controller(
            descriptor=self.pwm_descriptor,
            to=create_i2c_result.descriptor,
            addr=DEFAULT_PWM_ADDRESS,
        )
        return create_i2c_result.descriptor

    def init_led(self) -> int:
        """
        Создаём компонент светодиода с конкретной моделью (ky016)
        как исполняемое устройство и получаем дескриптор светодиода

        :return:
        """
        create_led_result = self.ri_sdk.create_model_component(
            group="executor",
            device_name="led",
            model_name="ky016",
        )
        # связываем светодиод с ШИМ,
        # передаем значения трех пинов к которым подключен светодиод
        self.ri_sdk.link_led_to_controller(
            descriptor=create_led_result.descriptor,
            pwm=self.pwm_descriptor,
            rport=RED_LED_PORT,  # red
            gport=GREEN_LED_PORT,  # green
            bport=BLUE_LED_PORT,  # blue
        )
        return create_led_result.descriptor

    def init_servos(self) -> None:
        """
        Создает сервоприводы и линкует их.
        Модифицирует объекты ServoInfo (обновляет дескриптор)
        """
        for servo in self.servos:
            create_servo_result = self.ri_sdk.create_model_component(
                group="executor",
                device_name="servodrive",
                model_name="mg90s",
            )
            servo.descriptor = create_servo_result.descriptor
            self.ri_sdk.link_servodrive_to_controller(
                descriptor=create_servo_result.descriptor,
                pwm=self.pwm_descriptor,
                port=servo.port,
            )

    def start_position(self, servo: ServoInfo) -> None:
        """
        Переводит сервопривод в стартовое положение.

        Выполняем поворот сервопривода в заданный угол,
        передаем дескриптор сервопривода, значение угла

        :param servo:
        :return:
        """
        self.ri_sdk.exec_servo_drive_turn_by_pulse(
            descriptor=servo.descriptor,
            pulse=servo.start_position_pulse,
        )

    def servos_to_start_position(self) -> None:
        """
        Проходим по известным сервам и устанавливаем в стартовую позицию

        :return:
        """
        for servo in self.servos:
            self.start_position(servo)

    def destruct_servos(self) -> None:
        """
        Уничтожает сервоприводы

        :return:
        """
        for servo in self.servos:
            self.ri_sdk.destroy_component(
                descriptor=servo.descriptor,
            )

    def destruct(self) -> None:
        """
        Красивое завершение через destruct - уничтожает все компоненты и библиотеку

        :return:
        """
        # уничтожаем сервоприводы
        self.destruct_servos()

        # останавливаем свечение светодиода с определенным дескриптором
        self.ri_sdk.exec_rgb_led_stop(self.led_descriptor)
        # удаляем компонент светодиода по дескриптору
        self.ri_sdk.destroy_component(self.led_descriptor)

        # сбрасываем все порты на ШИМ
        self.ri_sdk.sigmod_pwm_reset_all(self.pwm_descriptor)
        # удаляем компонент ШИМ
        self.ri_sdk.destroy_component(self.pwm_descriptor)

        # удаляем компонент i2c
        self.ri_sdk.destroy_component(self.i2c_descriptor)

        # удаляем sdk со всеми компонентами в реестре компонентов
        self.ri_sdk.destroy_sdk(is_force=True)

    def set_led(self, red: int, green: int, blue: int) -> None:
        """
        :param red:
        :param green:
        :param blue:
        :return:
        """
        self.ri_sdk.exec_rgb_led_single_pulse(
            descriptor=self.led_descriptor,
            r=red,
            g=green,
            b=blue,
            duration=0,
            run_async=True,
        )

    def turn_servo_with_relative_speed(
        self,
        servo_descriptor: int,
        angle: int,
        speed: int,
    ) -> None:
        """
        Поворот на заданный угол с заданной угловой скоростью.

        :param servo_descriptor: дескриптор сервопривода
        :param angle: угол
        :param speed: Угловая скорость поворота (процент от максимальной скорости)
        :return:
        """
        self.ri_sdk.exec_servo_drive_turn_with_relative_speed(
            descriptor=servo_descriptor,
            angle=angle,
            speed=speed,
        )

    def turn_servo(
        self,
        servo_descriptor: int,
        angle: int,
        speed: int,
    ) -> None:
        """

        :param servo_descriptor: дескриптор сервопривода
        :param angle: угол
        :param speed: Угловая скорость поворота (градус / секунда)
        :return:
        """
        self.ri_sdk.exec_servo_drive_turn(
            descriptor=servo_descriptor,
            angle=angle,
            speed=speed,
        )


def main() -> None:
    lib = contrib.get_lib()
    robohand = RoboHand(lib)

    # Устанавливаем фиолетовый цвет светодиода
    robohand.set_led(255, 0, 255)
    # инициализируем сервоприводы
    robohand.init_servos()
    # переводим сервоприводы в стартовое положение
    robohand.servos_to_start_position()

    # поворачиваем башню на угол 75 со скоростью 30%
    robohand.turn_servo_with_relative_speed(
        servo_descriptor=robohand.servo_rotate.descriptor,
        angle=75,
        speed=30,
    )

    # поднять башню на угол -40º со скоростью 50 г/с
    robohand.turn_servo(
        servo_descriptor=robohand.servo_raise.descriptor,
        angle=-40,
        speed=50,
    )

    # готовимся к завершению, включаем красный свет
    robohand.set_led(255, 0, 0)

    # Красиво завершаем работу через destruct
    robohand.destruct()


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
