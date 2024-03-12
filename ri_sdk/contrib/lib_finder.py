from __future__ import annotations

import os
import platform
from ctypes import CDLL, cdll
from pathlib import Path

from ri_sdk import loggers

log = loggers.utils

LIB_RISDK_DLL_FILENAME = os.getenv("LIB_RISDK_DLL_FILENAME", "librisdk.dll")
LIB_RISDK_SO_FILENAME = os.getenv("LIB_RISDK_SO_FILENAME", "librisdk.so")
LIB_RISDK_PATH = os.getenv("LIB_RISDK_DIR")

WINDOWS_LIB_DEFAULT_PATH = os.getenv(
    # https://docs.robointellect.ru/docs/risdk/getting-started/install_risdk/rrc_install/windows/
    "WINDOWS_LIB_DEFAULT_PATH",
    r"C:\Program Files (x86)\RoboIntellect\ri_sdk\ri_sdk_x64",
)
LINUX_LIB_DEFAULT_PATH = os.getenv(
    # https://docs.robointellect.ru/docs/risdk/getting-started/install_risdk/rrc_install/linux/
    "LINUX_LIB_DEFAULT_PATH",
    "/usr/local/robohand_remote_control/",
)


def get_lib(
    *,
    library_dir: Path | str | None = None,
    library_filepath: Path | str | None = None,
) -> CDLL:
    """
    Поиск внешней библиотеки для работы с SDK

    Настройки переменных окружения:
    LIB_RISDK_DLL_FILENAME - имя dll файла, по умолчанию librisdk.dll
    LIB_RISDK_SO_FILENAME - имя so файла, по умолчанию librisdk.so
    LIB_RISDK_DIR - путь для поиска RI SDK файла (путь к папке).
        Если не указан, поиск будет выполнен в папке по умолчанию.

    :param library_dir: путь к папке,
        где искать файл LIB_RISDK_DLL_FILENAME (librisdk.dll)
        или LIB_RISDK_SO_FILENAME (librisdk.so)
        (в зависимости от системы)
    :param library_filepath: полный путь до файла .so / .dll,
        например: Path("/home/repka/projects/robocontrol/librisdk.so")
    :return:
    """
    if library_filepath and Path(library_filepath).is_file():
        log.info("load pre-defined library %s", library_filepath)
        return cdll.LoadLibrary(str(library_filepath))

    my_platform = platform.system()
    if my_platform == "Windows":
        lib_name = LIB_RISDK_DLL_FILENAME
        default_lib_dir_path = Path(WINDOWS_LIB_DEFAULT_PATH)
    elif my_platform == "Linux":
        lib_name = LIB_RISDK_SO_FILENAME
        default_lib_dir_path = Path(LINUX_LIB_DEFAULT_PATH)
    else:
        log.warning("Unsupported platform %r", my_platform)
        msg = f"Unsupported platform {my_platform!r}"
        raise RuntimeError(msg)

    if library_dir and Path(library_dir).is_dir():
        lib_path = Path(library_dir)
        log.info("Load library from pre-defined dir %s", lib_path)
    else:
        if LIB_RISDK_PATH:
            lib_path = Path(LIB_RISDK_PATH)
        else:
            log.debug(
                "LIB_RISDK_DIR env not specified, defaulting to %s",
                default_lib_dir_path,
            )
            lib_path = default_lib_dir_path
        log.info("Load library from default dir %s", lib_path)

    lib_filepath = lib_path / lib_name
    if not lib_filepath.is_file():
        log.warning("Could not find librisdk at %s", lib_filepath)
        raise FileNotFoundError(lib_filepath)

    log.info("load sdk library binary %s", lib_filepath)
    lib = cdll.LoadLibrary(str(lib_filepath))
    return lib
