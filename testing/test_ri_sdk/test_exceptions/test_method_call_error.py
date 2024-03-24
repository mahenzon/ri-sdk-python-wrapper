import pytest

from ri_sdk.exceptions import MethodCallError


class TestMethodCallError:
    @pytest.mark.parametrize(
        ("error_code", "error_message", "method_name"),
        [
            (11223344, b"Error message", "method_name"),
            (55667788, b"Another error message", "another_method"),
        ],
    )
    def test_valid_parameters(self, error_code, error_message, method_name):
        err = MethodCallError(error_code, error_message, method_name)
        assert err.message_as_text == error_message.decode()

    def test_error_text_with_null_bytes_in_error_message(self):
        error_code = 123
        error_message_text = "This is an error message"
        error_message_encoded = error_message_text.encode()
        error_message = error_message_encoded + b"\x00with null bytes"
        method_name = "test_method"

        error = MethodCallError(error_code, error_message, method_name)

        assert error.error_code == error_code
        assert error.original_error_message == error_message
        assert error.error_message == error_message_encoded
        assert error.method_name == method_name
        assert error.message_as_text == error_message_text
