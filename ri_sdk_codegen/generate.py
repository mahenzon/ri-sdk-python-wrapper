import logging
from dataclasses import dataclass
from pathlib import Path

from mako.template import Template

from ri_sdk_codegen.doc_page_crawler import DocPageCrawler
from ri_sdk_codegen.types import MethodSDK

log = logging.getLogger(__name__)


@dataclass
class JsonDumpParams:
    indent: int = 2
    sort_keys: bool = False
    ensure_ascii: bool = False


class Codegen:
    def __init__(
        self,
        codegen_base_dir: Path,
        sdk_template_path: Path,
        sdk_output_file_path: Path,
        sort_by_name: bool = True,
        json_dump_params: JsonDumpParams | None = None,
        method_file_name: str = "method.json",
    ) -> None:
        self.codegen_base_dir: Path = codegen_base_dir
        self.sdk_template_path: Path = sdk_template_path
        self.sdk_output_file_path: Path = sdk_output_file_path
        self.sort_by_name: bool = sort_by_name
        self.json_dump_params: JsonDumpParams = (
            json_dump_params or JsonDumpParams()
        )
        self.method_file_name: str = method_file_name

    @classmethod
    def parse_methods_from_doc(cls, urls: list[str]) -> list[MethodSDK]:
        """
        Fetch every doc url and parse params

        :param urls:
        :return:
        """
        methods = []
        for page in urls:
            if not (url := page.strip()):
                continue
            log.info("Parse page %s", url)
            method = DocPageCrawler(url).prepare_method_sdk_info()
            methods.append(method)

        return methods

    def read_methods_from_json(self) -> list[MethodSDK]:
        pass

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

        log.info(
            "New Python script generated at %s",
            self.sdk_output_file_path,
        )

    def save_method_to_file(self, method: MethodSDK) -> None:
        method_filepath = (
            self.codegen_base_dir / method.name / self.method_file_name
        )
        method_filepath.parent.mkdir(parents=True, exist_ok=True)
        method_filepath.write_text(
            method.model_dump_json(
                indent=self.json_dump_params.indent,
            ),
        )

    def save_methods_to_json_cache(self, methods: list[MethodSDK]) -> None:
        for method in methods:
            self.save_method_to_file(method)

    def parse_docs_and_save_methods_to_json_cache(
        self,
        urls: list[str],
    ) -> None:
        methods = self.parse_methods_from_doc(urls)
        self.save_methods_to_json_cache(methods)

    def generate_sdk_script(self) -> list[MethodSDK]:
        # TODO: check for repeated method name params
        #   (is there even a chance?)
        methods = self.read_methods_from_json()
        self.render_methods_to_sdk_script(sdk_methods=methods)
        return methods
