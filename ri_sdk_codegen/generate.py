import logging
from pathlib import Path

from mako.template import Template

from ri_sdk_codegen.types import MethodSDK
from ri_sdk_codegen.doc_page_crawler import DocPageCrawler

log = logging.getLogger(__name__)


class Codegen:
    def __init__(
        self,
        sdk_template_path: Path,
        sdk_output_file_path: Path,
        sort_by_name: bool = True,
    ):

        self.sdk_template_path: Path = sdk_template_path
        self.sdk_output_file_path: Path = sdk_output_file_path
        self.sort_by_name: bool = sort_by_name

    def get_method_params(self, urls: list[str]) -> list[MethodSDK]:
        """
        Fetch every doc url and parse params

        :param urls:
        :return:
        """

        methods = []
        for page in urls:
            if not (url := page.strip()):
                continue
            method = DocPageCrawler(url).prepare_method_sdk_info()
            methods.append(method)

        return methods

    def render_methods_to_sdk_script(
        self,
        sdk_methods: list[MethodSDK],
    ) -> None:
        """
        :param sdk_methods:
        :return:
        """

        template = Template(filename=str(self.sdk_template_path))

        if self.sort_by_name:
            sdk_methods.sort(key=lambda m: m.name)
        # Render the template with the function name and parameters
        result = template.render(
            sdk_methods=sdk_methods,
        )
        # Write the rendered content to a new Python script
        self.sdk_output_file_path.write_text(result)

        log.info("New Python script generated at %s", self.sdk_output_file_path)

    def generate_sdk_script(self, urls: list[str]) -> list[MethodSDK]:
        """
        :param urls:
        :return:
        """

        methods = self.get_method_params(urls)
        self.render_methods_to_sdk_script(sdk_methods=methods)
        return methods
