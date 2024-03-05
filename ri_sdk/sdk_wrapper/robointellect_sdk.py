"""
Autogenerated!
Do not edit manually.
"""

import ctypes

from .robointellect_base_sdk import RoboIntellectBaseSDK


class RoboIntellectSDK(RoboIntellectBaseSDK):
    def __init__(
        self,
        lib: ctypes.CDLL,
        setup_methods_args: bool = False,
    ) -> None:
        """
        :param lib: RI SDK library .dll or .so
        :param setup_methods_args: whether to configure methods args on init
        """
        super().__init__(lib)
        if setup_methods_args:
            self.setup_all_methods_args_types()

    def setup_all_methods_args_types(self) -> None:
        """
        Установка типов аргументов всех методов.
        :return:
        """
        for name in dir(self):
            if not name.startswith("setup_arg_types_"):
                continue
            method = getattr(self, name)
            method()
