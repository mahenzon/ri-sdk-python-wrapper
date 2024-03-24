import pytest

from ri_sdk import RoboIntellectSDK
from ri_sdk_codegen.codegen_params import RI_SDK_CODEGEN_METHODS_CACHE_DIR
from ri_sdk_codegen.rendering.render_configs import SETUP_ARGS_METHOD_NAME_PREFIX
from ri_sdk_codegen.utils.case_converter import ri_sdk_method_name_wo_prefix
from testing.conftest import ALL_SETUP_NAMES, LOWER_THAN_39


@pytest.fixture()
def sdk_lib(mocker):
    return mocker.MagicMock(name="lib")


@pytest.fixture()
def sdk(sdk_lib):
    return RoboIntellectSDK(sdk_lib)


@pytest.fixture()
def ri_sdk_method_names():
    return [
        # as string
        path.name
        # refer cached names
        for path in RI_SDK_CODEGEN_METHODS_CACHE_DIR.iterdir()
        # validate it's RI SDK method
        if path.is_dir() and path.name.startswith("RI_SDK_")
    ]


class TestSetupArgsRoboIntellectSDK:
    def test_setup_all_methods_args_types(
        self,
        mocker,
        sdk,
        ri_sdk_method_names,
    ):
        # watch for cls methods
        spy_methods = [
            # spy for each
            mocker.spy(sdk, name)
            # in known
            for name in ALL_SETUP_NAMES
        ]

        # prepare methods args types prop (set None)
        for ri_sdk_method_name in ri_sdk_method_names:
            method = getattr(sdk.lib, ri_sdk_method_name)
            method.argtypes = None

        # call the method
        sdk.setup_all_methods_args_types()

        # assert all methods were called
        for meth in spy_methods:
            meth.assert_called_once()

        # assert argtypes prop is configured
        for ri_sdk_method_name in ri_sdk_method_names:
            method = getattr(sdk.lib, ri_sdk_method_name)
            assert hasattr(method, "argtypes")
            assert isinstance(method.argtypes, list)
            assert len(method.argtypes) > 0

    @pytest.mark.skipif(LOWER_THAN_39, reason="no removeprefix in py < 3.9")
    def test_sdk_has_all_setup_methods_args(self, sdk, ri_sdk_method_names):
        for sdk_method in ri_sdk_method_names:
            name = ri_sdk_method_name_wo_prefix(sdk_method)
            assert hasattr(sdk, f"{SETUP_ARGS_METHOD_NAME_PREFIX}{name}")

    def test_auto_setup_all_methods_args_types_on_init(self, mocker, sdk_lib):
        spy_setup_all_methods_args_types = mocker.spy(
            RoboIntellectSDK,
            "setup_all_methods_args_types",
        )
        sdk = RoboIntellectSDK(sdk_lib, setup_methods_args=True)
        # check called w/ sdk self
        spy_setup_all_methods_args_types.assert_called_once_with(sdk)
