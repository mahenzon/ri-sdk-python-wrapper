import pytest

from ri_sdk.contrib import get_lib


@pytest.fixture()
def lib_filepath(tmpdir):
    path = tmpdir.mkdir("libpath").join("lib.so")
    path.write("")
    return path


class TestGetLib:
    @pytest.mark.parametrize("platform_name", ["Darwin"])
    def test_get_lib_unsupported_platform(self, platform_name, mocker):
        mock_platform = mocker.patch("ri_sdk.contrib.lib_finder.platform", autospec=True)
        mock_platform.system.return_value = platform_name
        with pytest.raises(
            RuntimeError,
            match=f"Unsupported platform {platform_name!r}",
        ):
            get_lib()

    def test_get_predefined_lib(self, lib_filepath, mocker):
        mock_cdll = mocker.patch("ri_sdk.contrib.lib_finder.cdll", autospec=True)
        res = get_lib(library_filepath=lib_filepath)
        assert res is mock_cdll.LoadLibrary.return_value
        mock_cdll.LoadLibrary.assert_called_once_with(str(lib_filepath))
