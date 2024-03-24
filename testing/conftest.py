__all__ = (
    "LOWER_THAN_39",
    "ALL_SETUP_METHODS_NAMES",
    "ALL_METHOD_CALL_NAMES",
)

import sys
from collections.abc import Iterable

from ri_sdk_codegen.codegen_params import RI_SDK_CODEGEN_METHODS_CACHE_DIR
from ri_sdk_codegen.rendering.render_configs import SETUP_ARGS_METHOD_NAME_PREFIX
from ri_sdk_codegen.utils import method_name_to_snake_case


def create_setup_methods_names(sdk_methods_names: "Iterable[str]") -> "tuple[str, ...]":
    pref_len = len("ri_sdk_")
    names = []
    for sdk_method_name in sdk_methods_names:
        name = method_name_to_snake_case(sdk_method_name)[pref_len:]
        names.append(f"{SETUP_ARGS_METHOD_NAME_PREFIX}{name}")
    return tuple(names)


LOWER_THAN_39 = sys.version_info < (3, 9)

# for py < 3.9 compatibility
setup_prefix_len = len(SETUP_ARGS_METHOD_NAME_PREFIX)
RI_SDK_METHOD_NAMES = tuple(
    # as string
    path.name
    # refer cached names
    for path in RI_SDK_CODEGEN_METHODS_CACHE_DIR.iterdir()
    # validate it's RI SDK method
    if path.is_dir() and path.name.startswith("RI_SDK_")
)

ALL_SETUP_METHODS_NAMES = create_setup_methods_names(RI_SDK_METHOD_NAMES)
ALL_METHOD_CALL_NAMES = tuple(
    # remove prefix
    name[setup_prefix_len:]
    # consider all as ref
    for name in ALL_SETUP_METHODS_NAMES
)
