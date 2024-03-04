import ctypes


def convert_python_bytes_to_c_ulonglong(value: bytes) -> ctypes.c_ulonglong:
    return ctypes.c_ulonglong(int.from_bytes(value, "little"))


def convert_c_ulonglong_to_python_bytes(value: ctypes.c_ulonglong) -> bytes:
    # Extract the integer value from the ctypes.c_ulonglong object
    int_value = value.value
    # Convert the integer value to a bytes object
    bytes_value = int_value.to_bytes((int_value.bit_length() + 7) // 8, "big")
    return bytes_value
