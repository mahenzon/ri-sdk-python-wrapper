import logging
import re

import requests
from bs4 import BeautifulSoup, Tag

from ri_sdk_codegen.rendering.text_blocks import (
    DescriptionListBlockBase,
    DescriptionOrderedListBlock,
    DescriptionUnorderedListBlock,
    DescriptionBlockBase,
    DescriptionTextBlock,
)
from ri_sdk_codegen.types import MethodParamSDK, MethodSDK

log = logging.getLogger(__name__)


class DocPageCrawler:
    def __init__(self, url: str):
        self.url = url
        self.h1_method_name_regex = re.compile("^RI_SDK_")
        # lol cyrillic id
        self.description_h2_tag_id = "описание-метода"
        self.params_h2_tag_id = "параметры-и-возвращаемые-значения"
        # params table col indexes
        self.param_name_col_idx = 0
        self.param_shared_object_type_col_idx = 1
        self.golang_grpc_object_type_col_idx = 2
        self.param_description_col_idx = 3

    def _get_method_name(self, soup: BeautifulSoup) -> str:
        """
        :param soup:
        :return:
        """
        h1_tag: Tag = soup.find("h1", string=self.h1_method_name_regex)
        if not h1_tag:
            log.warning("error for url, no header with RI SDK. URL: %s", self.url)
            raise ValueError(f"No header with RI_SDK_. URL: {self.url}")
        return h1_tag.string

    def _get_description_tag(self, soup: BeautifulSoup) -> Tag:
        description_h2 = soup.find("h2", id=self.description_h2_tag_id)
        if not description_h2:
            log.warning(
                "error for url, no h2 with id=%r, url: %s",
                self.description_h2_tag_id,
                self.url,
            )
            raise ValueError(f"No h2 with id={self.description_h2_tag_id}")

        return description_h2

    def _get_list_description_block(self, tag: Tag) -> DescriptionListBlockBase:

        all_lis = tag.find_all("li")
        values = [li.text for li in all_lis]
        if tag.name == "ol":
            cls = DescriptionOrderedListBlock
        elif tag.name == "ul":
            cls = DescriptionUnorderedListBlock
        else:
            raise ValueError(f"unexpected list tag {tag.name}")
        return cls(values=values)

    def _get_description_blocks(
        self, soup: BeautifulSoup
    ) -> list[DescriptionBlockBase]:
        description_h2 = self._get_description_tag(soup)
        # Closest "p" is description
        next_tag = description_h2.find_next("p")
        description_blocks: list[DescriptionBlockBase] = []
        # probably "h2" is the where description ends
        while next_tag is not None and next_tag.name != "h2":
            if next_tag.name == "p":
                description_blocks.append(DescriptionTextBlock(next_tag.text))
            elif next_tag.name in ("ol", "ul"):
                description_blocks.append(self._get_list_description_block(next_tag))
            else:
                log.warning("Unexpected sibling tag %s", next_tag)
            next_tag = next_tag.next_sibling
        log.debug("+ Description lines", description_blocks)
        return description_blocks

    def _prepare_method_param_details(self, row: Tag) -> MethodParamSDK:
        table_row = row.find_all("td")
        param_name = table_row[self.param_name_col_idx].get_text()
        param_shared_object_type = table_row[
            self.param_shared_object_type_col_idx
        ].get_text()
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
        params_h2 = soup.find("h2", id=self.params_h2_tag_id)
        table_soup = params_h2.find_next_sibling("table")
        params = self._prepare_method_params(table_soup)
        return params

    def prepare_method_sdk_info(self) -> MethodSDK:
        log.debug("Read url %s", self.url)
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        method_name = self._get_method_name(soup)
        log.debug("* Method name: %r", method_name)
        all_description_lines = self._get_description_blocks(soup)
        params = self._get_params(soup)
        return MethodSDK(
            name=method_name,
            url=self.url,
            description_blocks=all_description_lines,
            params=params,
        )
