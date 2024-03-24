__all__ = (
    "LOWER_THAN_39",
    "ALL_SETUP_NAMES",
)

import sys

from ri_sdk import RoboIntellectSDK
from ri_sdk_codegen.rendering.render_configs import SETUP_ARGS_METHOD_NAME_PREFIX

LOWER_THAN_39 = sys.version_info < (3, 9)

ALL_SETUP_NAMES = tuple(
    name
    for name in dir(RoboIntellectSDK)
    if name.startswith(SETUP_ARGS_METHOD_NAME_PREFIX)
)
