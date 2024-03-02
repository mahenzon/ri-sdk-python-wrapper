import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import partial
from typing import Callable, Protocol, TypeVar

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


@dataclass
class DescriptionBlockBase(ABC):
    values: list[str]
    separator: str = "\n"
    initial_indent = FUNC_BODY_INDENT
    subsequent_indent = FUNC_BODY_INDENT

    def get_renderer(self, max_width: int) -> Callable:
        return partial(
            textwrap.fill,
            width=max_width,
            initial_indent=self.initial_indent,
            subsequent_indent=self.subsequent_indent,
            fix_sentence_endings=True,
            drop_whitespace=True,
            replace_whitespace=True,
        )

    @abstractmethod
    def process(self, max_width: int) -> ReturnType:
        raise NotImplementedError


@dataclass
class DescriptionTextBlock(DescriptionBlockBase):
    def process(self, max_width: int) -> ReturnType:
        process_string: TextProcessorProtocol = self.get_renderer(max_width)
        return self.separator.join(map(process_string, self.values))


@dataclass
class DescriptionListBlockBase(DescriptionBlockBase):
    subsequent_indent = PARAM_SUBSEQUENT_INDENT

    def process(self, max_width: int) -> ReturnType:
        process_string: TextProcessorProtocol = self.get_renderer(max_width)
        return self.separator.join(map(process_string, self.values))


@dataclass
class DescriptionUnorderedListBlock(DescriptionListBlockBase):
    def process(self, max_width: int) -> ReturnType:
        process_string: TextProcessorProtocol = self.get_renderer(max_width)
        bullet_elems = (f"- {value}" for value in self.values)
        return self.separator.join(map(process_string, bullet_elems))


@dataclass
class DescriptionOrderedListBlock(DescriptionListBlockBase):
    def process(self, max_width: int) -> ReturnType:
        process_string: TextProcessorProtocol = self.get_renderer(max_width)
        numbered_elems = (
            f"{idx}. {value}" for idx, value in enumerate(self.values, start=1)
        )
        return self.separator.join(map(process_string, numbered_elems))
