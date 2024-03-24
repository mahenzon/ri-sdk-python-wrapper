import inspect

import pytest

from ri_sdk import RoboIntellectSDK
from testing.conftest import (
    ALL_METHOD_CALL_NAMES,
    ALL_SETUP_METHODS_NAMES,
    RI_SDK_METHOD_NAMES,
)


@pytest.fixture()
def sdk_lib(mocker):
    return mocker.MagicMock(name="lib")


@pytest.fixture()
def sdk(sdk_lib):
    return RoboIntellectSDK(sdk_lib)


@pytest.fixture()
def sdk_method(request, sdk):
    name = request.param
    method = getattr(sdk.lib, name)
    method.__name__ = name
    # successful result status code
    method.return_value = 0
    return method


class TestSetupArgsRoboIntellectSDK:
    def test_setup_all_methods_args_types(self, mocker, sdk):
        # watch for cls methods
        spy_methods = [
            # spy for each
            mocker.spy(sdk, name)
            # in known
            for name in ALL_SETUP_METHODS_NAMES
        ]

        # prepare methods args types prop (set None)
        for ri_sdk_method_name in RI_SDK_METHOD_NAMES:
            method = getattr(sdk.lib, ri_sdk_method_name)
            method.argtypes = None

        # call the method
        sdk.setup_all_methods_args_types()

        # assert all methods were called
        for meth in spy_methods:
            meth.assert_called_once()

        # assert argtypes prop is configured
        for ri_sdk_method_name in RI_SDK_METHOD_NAMES:
            method = getattr(sdk.lib, ri_sdk_method_name)
            assert hasattr(method, "argtypes")
            assert isinstance(method.argtypes, list)
            assert len(method.argtypes) > 0

    @pytest.mark.parametrize("setup_method_name", ALL_SETUP_METHODS_NAMES)
    def test_sdk_has_all_setup_methods_args(self, sdk, setup_method_name):
        assert hasattr(sdk, setup_method_name)

    def test_auto_setup_all_methods_args_types_on_init(self, mocker, sdk_lib):
        spy_setup_all_methods_args_types = mocker.spy(
            RoboIntellectSDK,
            "setup_all_methods_args_types",
        )
        sdk = RoboIntellectSDK(sdk_lib, setup_methods_args=True)
        # check called w/ sdk self
        spy_setup_all_methods_args_types.assert_called_once_with(sdk)


class TestCallMethodsRoboIntellectSDK:
    @pytest.mark.parametrize(
        ("method_name", "sdk_method"),
        zip(ALL_METHOD_CALL_NAMES, RI_SDK_METHOD_NAMES),
        indirect=["sdk_method"],
    )
    def test_call_sdk_method(
        self,
        sdk,
        method_name,
        sdk_method,
    ):
        method = getattr(sdk, method_name)
        # get method return type using inspect
        return_type = inspect.signature(method).return_annotation

        # create values from args types, only for those who don't have defaults
        # noinspection PyUnresolvedReferences
        args_values = {
            name: param.annotation()
            for name, param in inspect.signature(method).parameters.items()
            if param.default is inspect._empty
        }
        result = method(**args_values)
        assert isinstance(result, return_type)
        sdk_method.assert_called_once()
