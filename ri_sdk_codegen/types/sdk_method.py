from functools import cached_property

from pydantic import BaseModel, Field

from ri_sdk_codegen.config import TYPES_MODULE_NAME
from ri_sdk_codegen.rendering.text_blocks import DescriptionBlock
from ri_sdk_codegen.types.options_override import MethodOptions, ParamOptions
from ri_sdk_codegen.types.sdk_method_param import MethodParamSDK
from ri_sdk_codegen.utils import (
    method_name_to_upper_camel_case,
    ri_sdk_method_name_wo_prefix,
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

    @cached_property
    def params_by_names(self) -> dict[str, MethodParamSDK]:
        return {param.name: param for param in self.params}

    @cached_property
    def len_params_to_be_replaced(self) -> dict[str, MethodParamSDK]:
        return {
            # example "len": buff_param
            param_options.auto_len: self.params_by_names[param_name]
            for param_name, param_options in self.options.params.items()
            if param_options.auto_len
        }

    def is_auto_len_param(self, param: MethodParamSDK) -> bool:
        return param.name in self.len_params_to_be_replaced

    def param_to_take_len_from(self, len_param: MethodParamSDK) -> MethodParamSDK:
        if len_param.name in self.len_params_to_be_replaced:
            return self.len_params_to_be_replaced[len_param.name]
        msg = (
            f"Cannot find len of what param is {len_param!r}"
            f" on method {self.name!r}, {self!r}"
        )
        raise ValueError(msg)

    def is_receive_type(self, param: MethodParamSDK) -> bool:
        if param.name not in self.options.params:
            return param.is_pointer
        opt: ParamOptions = self.options.params[param.name]
        return opt.direction == "output"

    def param_u_long_long_length_param(
        self,
        param: MethodParamSDK,
    ) -> MethodParamSDK:
        """
        If needed, can be overridden in options.yaml
        (not needed right now)

        :param param:
        :return:
        """
        for p in self.func_sdk_receivers:
            # hardcoded for now, because there's no other name
            if p.name == "readBytesLen":
                return p

        msg = f"No len param for param {param.name} {param} on method {self}"
        raise ValueError(msg)

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
                # wrapper call, skip auto param
                and not self.is_auto_len_param(param)
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
        return ri_sdk_method_name_wo_prefix(self.name)

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
