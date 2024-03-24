from ctypes import cdll
from pathlib import Path

import pytest

from ri_sdk.contrib import get_lib
from ri_sdk.contrib.lib_finder import get_lib_path, validate_lib_filepath


@pytest.fixture()
def lib_filepath(tmpdir):
    path = tmpdir.mkdir("libpath").join("lib.so")
    path.write("")
    return path


@pytest.fixture()
def mocked_load_library(mocker):
    return mocker.patch.object(cdll, "LoadLibrary", autospec=True)


class TestGetLib:
    @pytest.mark.parametrize("platform_name", ["Darwin"])
    def test_get_lib_unsupported_platform(self, platform_name, mocker):
        mocker.patch(
            "ri_sdk.contrib.lib_finder.platform.system",
            return_value=platform_name,
        )
        with pytest.raises(
            RuntimeError,
            match=f"Unsupported platform {platform_name!r}",
        ):
            get_lib()

    def test_get_predefined_lib(self, lib_filepath, mocked_load_library):
        res = get_lib(library_filepath=lib_filepath)
        assert res is mocked_load_library.return_value
        mocked_load_library.assert_called_once_with(str(lib_filepath))

    @pytest.mark.parametrize("platform_name", ["Linux", "Windows"])
    def test_library_dir_defined(
        self,
        mocker,
        tmpdir,
        mocked_load_library,
        platform_name,
    ):
        mocker.patch(
            "ri_sdk.contrib.lib_finder.platform.system",
            return_value=platform_name,
        )
        mock_validate_lib_filepath = mocker.patch(
            "ri_sdk.contrib.lib_finder.validate_lib_filepath",
        )
        # Create a temporary directory for the library_dir
        library_dir = tmpdir.mkdir("library_dir")

        # Call the get_lib function with the library_dir parameter
        res = get_lib(library_dir=str(library_dir))
        assert res is mocked_load_library.return_value

        mock_validate_lib_filepath.assert_called_once()


class TestValidateLibFilepath:
    def test_valid_lib_filepath_raises(self):
        lib_filepath = Path("path/to/nonexistent_lib.so")
        assert lib_filepath.is_file() is False

        with pytest.raises(FileNotFoundError):
            validate_lib_filepath(lib_filepath)


class TestGetLibPath:
    def test_lib_path_with_defined_env(self, mocker):
        new_path = "some/path/to/binary"
        mocker.patch("ri_sdk.contrib.lib_finder.LIB_RISDK_PATH", new=new_path)

        library_dir = None
        default_lib_dir_path = Path("/default/path")

        result = get_lib_path(library_dir, default_lib_dir_path)

        assert result == Path(new_path)

    def test_lib_path_not_defined_in_env(self, mocker):
        mocker.patch("ri_sdk.contrib.lib_finder.LIB_RISDK_PATH", new=None)

        library_dir = None
        default_lib_dir_path = Path("/default/path")

        result = get_lib_path(library_dir, default_lib_dir_path)

        assert result == default_lib_dir_path
