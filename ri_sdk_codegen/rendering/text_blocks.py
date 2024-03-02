import textwrap
from functools import cached_property, partial
from typing import Callable, Literal, Protocol, TypeVar

from pydantic import BaseModel

from ri_sdk_codegen.rendering.render_configs import (
    FUNC_BODY_INDENT,
    PARAM_SUBSEQUENT_INDENT,
)

ReturnType = TypeVar("ReturnType", str, list[str])


class TextProcessorProtocol(Protocol):
    """
    Protocol for configured `TextWrapper.fill` or `TextWrapper.wrap`
    Called through `textwrap.fill` or `textwrap.wrap`
    """

    def __call__(
        self,
        text: str,
        width: int = 70,
        initial_indent: str = "",
        subsequent_indent: str = "",
        expand_tabs: bool = True,
        replace_whitespace: bool = True,
        fix_sentence_endings: bool = False,
        break_long_words: bool = True,
        drop_whitespace: bool = True,
        break_on_hyphens: bool = True,
        tabsize: int = 8,
        *,
        max_lines: int | None = None,
        placeholder: str = " [...]",
    ) -> ReturnType:
        pass


DescriptionBlockType = Literal[
    "block",
    "list-block",
    "unordered-list-block",
    "ordered-list-block",
]


class DescriptionBlock(BaseModel):
    values: list[str]
    type: DescriptionBlockType = "block"

    _separator: str = "\n"

    @property
    def separator(self) -> str:
        return self._separator

    @classmethod
    def get_initial_indent(cls) -> str:
        return FUNC_BODY_INDENT

    def get_subsequent_indent(self) -> str:
        if self.type.endswith("list-block"):
            return PARAM_SUBSEQUENT_INDENT
        return FUNC_BODY_INDENT

    def get_renderer(self, max_width: int) -> Callable:
        return partial(
            textwrap.fill,
            width=max_width,
            initial_indent=self.get_initial_indent(),
            subsequent_indent=self.get_subsequent_indent(),
            fix_sentence_endings=True,
            drop_whitespace=True,
            replace_whitespace=True,
        )

    def process(self, max_width: int) -> ReturnType:
        return self.processors[self.type](max_width)

    def process_text_block(self, max_width: int) -> ReturnType:
        process_string: TextProcessorProtocol = self.get_renderer(max_width)
        return self.separator.join(map(process_string, self.values))

    def process_list_block(self, max_width: int) -> ReturnType:
        process_string: TextProcessorProtocol = self.get_renderer(max_width)
        return self.separator.join(map(process_string, self.values))

    def process_unordered_list_block(self, max_width: int) -> ReturnType:
        process_string: TextProcessorProtocol = self.get_renderer(max_width)
        bullet_elems = (f"- {value}" for value in self.values)
        return self.separator.join(map(process_string, bullet_elems))

    def process_ordered_list_block(self, max_width: int) -> ReturnType:
        process_string: TextProcessorProtocol = self.get_renderer(max_width)
        numbered_elems = (
            f"{idx}. {value}" for idx, value in enumerate(self.values, start=1)
        )
        return self.separator.join(map(process_string, numbered_elems))

    # TODO: cover in tests that all keys are used
    @cached_property
    def processors(self) -> dict[DescriptionBlockType, Callable]:
        return {
            "block": self.process_text_block,
            "list-block": self.process_list_block,
            "unordered-list-block": self.process_unordered_list_block,
            "ordered-list-block": self.process_ordered_list_block,
        }
