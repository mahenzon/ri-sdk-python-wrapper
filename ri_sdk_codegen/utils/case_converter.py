def camel_case_to_snake_case(input_str: str) -> str:
    """
    >>> camel_case_to_snake_case("SomeSDK")
    'some_sdk'
    >>> camel_case_to_snake_case("RServoDrive")
    'r_servo_drive'
    >>> camel_case_to_snake_case("SDKDemo")
    'sdk_demo'
    """
    chars = []
    for c_idx, char in enumerate(input_str):
        if c_idx and char.isupper():
            nxt_idx = c_idx + 1
            # idea of the flag is to separate abbreviations
            # as new words, show them in lower case
            flag = nxt_idx >= len(input_str) or input_str[nxt_idx].isupper()
            prev_char = input_str[c_idx - 1]
            if prev_char.isupper() and flag:
                pass
            else:
                chars.append("_")
        chars.append(char.lower())
    return "".join(chars)


def method_name_to_snake_case(input_str: str) -> str:
    """
    >>> method_name_to_snake_case("Check_InitSDK")
    'check_init_sdk'
    >>> method_name_to_snake_case("Check_Init_SDK")
    'check_init_sdk'
    >>> method_name_to_snake_case("Check_Init_SomeSDK")
    'check_init_some_sdk'
    >>> method_name_to_snake_case("exec_RServoDrive")
    'exec_r_servo_drive'
    >>> method_name_to_snake_case("RI_SDK_exec_RGB_LED_GetState")
    'ri_sdk_exec_rgb_led_get_state'
    """
    parts = input_str.split("_")
    for idx, part in enumerate(parts):
        parts[idx] = part.lower() if part.isupper() else camel_case_to_snake_case(part)

    return "_".join(parts)


def method_name_to_upper_camel_case(input_str: str) -> str:
    if input_str.lower().startswith("ri_sdk_"):
        # we can't use .removeprefix here because of the case (upper / lower)
        prefix_size = len("ri_sdk_")
        input_str = input_str[prefix_size:]
    return "".join(w[0].upper() + w[1:] for w in input_str.split("_"))
