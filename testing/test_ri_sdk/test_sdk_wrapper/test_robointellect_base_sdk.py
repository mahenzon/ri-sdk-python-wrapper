import pytest

from ri_sdk.exceptions import MethodCallError
from ri_sdk.sdk_wrapper.robointellect_base_sdk import RoboIntellectBaseSDK, ctypes


@pytest.fixture()
def sdk(mocker) -> RoboIntellectBaseSDK:
    lib = mocker.MagicMock()
    sdk = RoboIntellectBaseSDK(lib)
    return sdk


@pytest.fixture()
def sdk_method(mocker):
    # Mock the method to be called
    method = mocker.MagicMock()
    method_name = "RI_SDK_some_method"
    method.__name__ = method_name
    return method


@pytest.fixture()
def mock_create_string_buffer(mocker):
    return mocker.patch.object(ctypes, "create_string_buffer")


class TestRoboIntellectBaseSDK:
    def test_call_sdk_method(self, sdk, sdk_method, mock_create_string_buffer):
        return_code = 0
        sdk_method.return_value = return_code

        # some args
        args = (1, 2, 3)
        # Call the method
        result = sdk.call_sdk_method(sdk_method, *args)
        assert result == return_code
        mock_create_string_buffer.assert_called_once_with(
            sdk.error_string_buffer_size,
        )
        # Assert that the method was called with the correct arguments
        sdk_method.assert_called_once_with(
            *args,
            # error_text_c
            mock_create_string_buffer.return_value,
        )

    def test_call_sdk_method_with_error(
        self,
        sdk,
        sdk_method,
        mock_create_string_buffer,
    ):
        return_code = 1
        sdk_method.return_value = return_code

        # Call the method and expect a MethodCallError to be raised
        args = (1, 2, 3)
        with pytest.raises(MethodCallError):
            sdk.call_sdk_method(sdk_method, *args)

        mock_create_string_buffer.assert_called_once_with(
            sdk.error_string_buffer_size,
        )
        # Assert that the method was called with the correct arguments
        sdk_method.assert_called_once_with(
            *args,
            # error_text_c
            mock_create_string_buffer.return_value,
        )
