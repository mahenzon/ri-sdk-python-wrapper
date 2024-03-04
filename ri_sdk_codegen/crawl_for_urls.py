import logging
from collections.abc import Generator
from pathlib import Path

import requests
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)


class DocsUrlCrawler:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.already_visited = set()

    def fetch_sdk_url_pages(self, url: str) -> Generator[str, None, None]:
        if url in self.already_visited:
            return
        self.already_visited.add(url)
        log.debug("* Visit url %s", url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        h1_tag = soup.find("h1")
        if h1_tag and h1_tag.text.startswith("RI_SDK"):
            log.info(
                "! Found page where 'h1' tag text starts with 'RI_SDK'.\nUrl: %s",
                url,
            )
            yield url

        links = soup.find_all(
            "a",
            href=lambda href: href and href.startswith("/docs/"),
        )
        for link in links:
            next_url = link["href"]
            if not next_url.startswith("/docs/"):
                continue

            yield from self.fetch_sdk_url_pages(self.base_url + next_url)

    def find_and_write_urls(
        self,
        docs_crawl_start_url: str,
        filepath: Path,
    ) -> None:
        self.already_visited = set()
        urls = list(self.fetch_sdk_url_pages(docs_crawl_start_url))
        log.info("Found URLs: %s", urls)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text("\n".join(urls))
        log.warning("All URLs written to %s", filepath)
