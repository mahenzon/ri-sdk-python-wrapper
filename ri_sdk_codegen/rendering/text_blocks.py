import textwrap
from functools import cached_property, partial
from typing import Callable, Literal

from pydantic import BaseModel, Field

from ri_sdk_codegen.rendering.render_configs import (
    METHOD_BODY_INDENT,
    METHOD_PARAM_SUBSEQUENT_INDENT,
)

DescriptionBlockType = Literal[
    "block",
    "list-block",
    "unordered-list-block",
    "ordered-list-block",
]


class DescriptionBlock(BaseModel):
    values: list[str]
    type: DescriptionBlockType = "block"

    separator: str = Field("\n", exclude=True)

    @classmethod
    def get_initial_indent(cls) -> str:
        return METHOD_BODY_INDENT

    def get_subsequent_indent(self) -> str:
        if self.type.endswith("list-block"):
            return METHOD_PARAM_SUBSEQUENT_INDENT
        return METHOD_BODY_INDENT

    def get_renderer(self, max_width: int) -> Callable[[str], str]:
        return partial(
            textwrap.fill,
            width=max_width,
            initial_indent=self.get_initial_indent(),
            subsequent_indent=self.get_subsequent_indent(),
            fix_sentence_endings=True,
            drop_whitespace=True,
            replace_whitespace=True,
        )

    def process(self, max_width: int) -> str:
        return self.processors[self.type](max_width)

    def process_text_block(self, max_width: int) -> str:
        process_string = self.get_renderer(max_width)
        return self.separator.join(map(process_string, self.values))

    def process_list_block(self, max_width: int) -> str:
        process_string = self.get_renderer(max_width)
        return self.separator.join(map(process_string, self.values))

    def process_unordered_list_block(self, max_width: int) -> str:
        process_string = self.get_renderer(max_width)
        bullet_elems = (f"- {value}" for value in self.values)
        return self.separator.join(map(process_string, bullet_elems))

    def process_ordered_list_block(self, max_width: int) -> str:
        process_string = self.get_renderer(max_width)
        numbered_elems = (
            f"{idx}. {value}" for idx, value in enumerate(self.values, start=1)
        )
        return self.separator.join(map(process_string, numbered_elems))

    # TODO: cover in tests that all keys are used
    @cached_property
    def processors(self) -> dict[DescriptionBlockType, Callable[[int], str]]:
        return {
            "block": self.process_text_block,
            "list-block": self.process_list_block,
            "unordered-list-block": self.process_unordered_list_block,
            "ordered-list-block": self.process_ordered_list_block,
        }
