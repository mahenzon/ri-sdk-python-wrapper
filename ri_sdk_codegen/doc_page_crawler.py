import logging
import re
from functools import cached_property
from pathlib import Path
from typing import Literal

import requests
import yaml
from bs4 import BeautifulSoup, NavigableString, PageElement, Tag

from ri_sdk_codegen.rendering.text_blocks import DescriptionBlock
from ri_sdk_codegen.types import MethodParamSDK, MethodSDK, MethodsOptions

log = logging.getLogger(__name__)


class DocPageCrawler:
    def __init__(
        self,
        url: str,
        methods_options_filepath: Path,
        request_timeout: int = 10,
    ) -> None:
        self.url = url
        self.request_timeout = request_timeout
        self.h1_method_name_regex = re.compile("^RI_SDK_")
        # lol cyrillic id
        self.description_h2_tag_id = "описание-метода"
        self.params_h2_tag_id = "параметры-и-возвращаемые-значения"
        # params table col indexes
        self.param_name_col_idx = 0
        self.param_shared_object_type_col_idx = 1
        self.golang_grpc_object_type_col_idx = 2
        self.param_description_col_idx = 3
        self.methods_options_filepath = methods_options_filepath

    @classmethod
    def _ensure_is_tag_type(cls, val: Tag | NavigableString | None) -> Literal[True]:
        if isinstance(val, Tag):
            return True
        msg = f"Expected Tag, got {type(val)}: {val}"
        raise ValueError(msg)

    def _get_method_name(self, soup: BeautifulSoup) -> str:
        """
        :param soup:
        :return:
        """
        h1_tag = soup.find("h1", string=self.h1_method_name_regex)
        if not isinstance(h1_tag, Tag):
            log.warning(
                "error for url, no header with RI SDK. URL: %s",
                self.url,
            )
            msg = f"No header with RI_SDK_. URL: {self.url}"
            raise ValueError(msg)
        if not h1_tag.string:
            msg = f"No header value with RI_SDK_. URL: {self.url}, tag: {h1_tag}"
            raise ValueError(msg)
        return h1_tag.string

    @cached_property
    def _methods_options(self) -> MethodsOptions:
        """
        Read and save methods options
        :return:
        """
        if not self.methods_options_filepath.is_file():
            return MethodsOptions()
        with self.methods_options_filepath.open() as f:
            return MethodsOptions.model_validate(yaml.safe_load(f).get("methods", {}))

    def _validate_method_name(self, method_name: str) -> str:
        """
        Method name can be overridden

        :param method_name:
        :return:
        """
        if method_name in self._methods_options.names_overrides:
            return self._methods_options.names_overrides[method_name]
        return method_name

    def _get_description_tag(self, soup: BeautifulSoup) -> Tag:
        description_h2 = soup.find("h2", id=self.description_h2_tag_id)
        if not isinstance(description_h2, Tag):
            log.warning(
                "error for url, no h2 with id=%r, url: %s",
                self.description_h2_tag_id,
                self.url,
            )
            msg = f"No h2 with id={self.description_h2_tag_id}"
            raise ValueError(msg)

        return description_h2

    @classmethod
    def _get_list_description_block(cls, tag: Tag) -> DescriptionBlock:
        all_lis = tag.find_all("li")
        values = [li.text for li in all_lis]
        # other types are not supported yet
        block_type: Literal[
            "ordered-list-block",
            "unordered-list-block",
        ]
        if tag.name == "ol":
            block_type = "ordered-list-block"
        elif tag.name == "ul":
            block_type = "unordered-list-block"
        else:
            msg = f"unexpected list tag {tag.name}"
            raise ValueError(msg)
        return DescriptionBlock(values=values, type=block_type)

    @classmethod
    def _get_table_description_block(cls, tag: Tag) -> DescriptionBlock:
        rows = tag.find_all("tr")

        table_data = []
        header_found = bool(tag.find("th"))
        # Extract table content into a list of lines
        for row in rows:
            cells = row.find_all(["th", "td"])
            row_data = tuple(cell.text.strip() for cell in cells)
            table_data.append(row_data)

        return DescriptionBlock.from_table_rows(
            table_data,
            first_row_is_header=header_found,
        )

    def _process_description_tag(self, tag: Tag) -> DescriptionBlock | None:
        if tag.name in ("p", "h3"):
            return DescriptionBlock(values=tag.text.split("\n"))
        if tag.name in ("ol", "ul"):
            return self._get_list_description_block(tag)
        if tag.name == "table":
            return self._get_table_description_block(tag)
        log.warning("Unexpected sibling tag %s", tag)
        return None  # lol mypy

    @classmethod
    def _get_as_tag(cls, tag: PageElement | Tag | NavigableString | None) -> Tag:
        if isinstance(tag, Tag):
            return tag
        msg = f"Unexpected tag type: {type(tag)}: {tag}"
        raise ValueError(msg)

    def _get_description_blocks(
        self,
        soup: BeautifulSoup,
    ) -> list[DescriptionBlock]:
        description_h2 = self._get_description_tag(soup)
        # Closest "p" is description
        next_tag: Tag = self._get_as_tag(
            # just for MyPy (extra validation)
            description_h2.find_next("p"),
        )
        description_blocks: list[DescriptionBlock] = []
        # probably "h2" is the where description ends
        while next_tag is not None and next_tag.name != "h2":
            block = self._process_description_tag(next_tag)
            if block:
                description_blocks.append(block)
            next_tag = self._get_as_tag(next_tag.next_sibling)
        log.debug("+ Description lines %s", description_blocks)
        return description_blocks

    def _prepare_method_param_details(self, row: Tag) -> MethodParamSDK:
        table_row = row.find_all("td")
        param_name = table_row[self.param_name_col_idx].get_text()
        param_shared_object_type = table_row[
            self.param_shared_object_type_col_idx
        ].get_text()
        # ruff: noqa: ERA001
        # golang_grpc_object_type = table_row[2].get_text()
        param_description = table_row[self.param_description_col_idx].get_text()
        return MethodParamSDK.from_info(
            name=param_name,
            shared_object_type=param_shared_object_type,
            description=param_description,
        )

    def _prepare_method_params(self, table_soup: Tag) -> list[MethodParamSDK]:
        return [
            # parse each one
            self._prepare_method_param_details(row)
            # go through table, skip header row
            for row in table_soup.find_all("tr")[1:]
        ]

    def _get_params(self, soup: BeautifulSoup) -> list[MethodParamSDK]:
        """
        TODO: handle "read" actions like RI_SDK_connector_i2c_ReadByte
            and return the value

        :param soup:
        :return:
        """
        params_h2: Tag = self._get_as_tag(
            # just for MyPy (extra validation)
            soup.find("h2", id=self.params_h2_tag_id),
        )
        table_soup: Tag = self._get_as_tag(
            # just for MyPy (extra validation)
            params_h2.find_next_sibling("table"),
        )
        return self._prepare_method_params(table_soup)

    def prepare_method_sdk_info(self) -> MethodSDK:
        log.debug("Read url %s", self.url)
        response = requests.get(self.url, timeout=self.request_timeout)
        soup = BeautifulSoup(response.content, "html.parser")
        method_name = self._get_method_name(soup)
        method_name = self._validate_method_name(method_name)
        log.debug("* Method name: %r", method_name)
        all_description_lines = self._get_description_blocks(soup)
        params = self._get_params(soup)
        return MethodSDK(
            name=method_name,
            url=self.url,
            description_blocks=all_description_lines,
            params=params,
        )
