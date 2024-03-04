from functools import cached_property

from pydantic import BaseModel, Field

from ri_sdk_codegen.config import TYPES_MODULE_NAME
from ri_sdk_codegen.rendering.text_blocks import DescriptionBlock
from ri_sdk_codegen.types.options_override import MethodOptions, ParamOptions
from ri_sdk_codegen.types.sdk_method_param import MethodParamSDK
from ri_sdk_codegen.utils import (
    method_name_to_snake_case,
    method_name_to_upper_camel_case,
)


class MethodSDK(BaseModel):
    name: str
    url: str
    description_blocks: list[DescriptionBlock]
    params: list[MethodParamSDK]

    # service info, not method info
    options: MethodOptions = Field(
        default_factory=MethodOptions,
        exclude=True,
    )

    def is_receive_type(self, param: MethodParamSDK) -> bool:
        if param.name not in self.options.params:
            return param.is_pointer
        opt: ParamOptions = self.options.params[param.name]
        return opt.direction == "output"

    @cached_property
    def func_call_params(self) -> list[MethodParamSDK]:
        return [
            param
            for param in self.params
            # skip service param
            if (
                not param.is_service_param
                # check if is not receive type
                and not self.is_receive_type(param)
            )
        ]

    @cached_property
    def func_sdk_receivers(self) -> list[MethodParamSDK]:
        return [
            param
            for param in self.params
            # skip service param
            if (
                not param.is_service_param
                # check if is of receive type
                and self.is_receive_type(param)
            )
        ]

    @cached_property
    def func_sdk_call_args(self) -> list[MethodParamSDK]:
        return [
            param
            for param in self.params
            # skip service param
            if not param.is_service_param
        ]

    @cached_property
    def py_method_name(self) -> str:
        return method_name_to_snake_case(self.name).removeprefix("ri_sdk_")

    @cached_property
    def py_module_name(self) -> str:
        return f"{self.py_method_name}_result"

    @cached_property
    def py_module_filename(self) -> str:
        return f"{self.py_module_name}.py"

    @cached_property
    def py_return_type_cls_name(self) -> str:
        return f"{method_name_to_upper_camel_case(self.name)}Result"

    @cached_property
    def py_method_return_type(self) -> str:
        return f"{TYPES_MODULE_NAME}.{self.py_return_type_cls_name}"

    @cached_property
    def py_method_return_value(self) -> str:
        # TODO: if getter, set real return value
        return "None"
