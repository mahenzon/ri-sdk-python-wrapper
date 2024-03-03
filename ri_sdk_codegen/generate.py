import json
import logging
from dataclasses import dataclass
from pathlib import Path

import yaml
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
        method_return_type_template_path: Path,
        method_return_types_init_template_path: Path,
        sdk_output_file_path: Path,
        sdk_return_types_output_path: Path,
        sort_by_name: bool = True,
        json_dump_params: JsonDumpParams | None = None,
        method_file_name: str = "method.json",
        method_options_file_name: str = "options.yaml",
        remove_existing_types: bool = True,
    ) -> None:
        self.codegen_base_dir: Path = codegen_base_dir
        self.sdk_template_path: Path = sdk_template_path
        self.method_return_type_template_path: Path = (
            method_return_type_template_path
        )
        self.method_return_types_init_template_path: Path = (
            method_return_types_init_template_path
        )
        self.sdk_output_file_path: Path = sdk_output_file_path
        self.sdk_return_types_output_path: Path = sdk_return_types_output_path
        self.sort_by_name: bool = sort_by_name
        self.json_dump_params: JsonDumpParams = (
            json_dump_params or JsonDumpParams()
        )
        self.method_file_name: str = method_file_name
        self.method_options_file_name: str = method_options_file_name
        self.remove_existing_types: bool = remove_existing_types

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

    @classmethod
    def make_method_sdk_from_json_file(
        cls,
        method_file_path: Path,
        method_options_file_path: Path,
    ) -> MethodSDK:
        with method_file_path.open() as f:
            method_data = json.load(f)

        if method_options_file_path.is_file():
            with method_options_file_path.open() as f:
                method_data.update(options=yaml.safe_load(f))

        return MethodSDK(**method_data)

    def read_methods_from_json(self) -> list[MethodSDK]:
        methods = []
        for method_dir in self.codegen_base_dir.iterdir():
            if not method_dir.is_dir():
                continue
            method_file = method_dir / self.method_file_name
            if not method_file.is_file():
                log.warning("Skipping %s because is not file!", method_file)
                continue
            method_options_file = method_dir / self.method_options_file_name
            methods.append(
                self.make_method_sdk_from_json_file(
                    method_file,
                    method_options_file,
                ),
            )
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

        log.info(
            "New Python script generated at %s",
            self.sdk_output_file_path,
        )

    def create_method_return_type(
        self,
        template: Template,
        method: MethodSDK,
    ) -> None:
        """
        :param template:
        :param method:
        :return:
        """
        result = template.render(method=method)
        module_path = (
            self.sdk_return_types_output_path / method.py_module_filename
        )
        module_path.write_text(result)

        log.debug("Created new Python return type at %s", module_path)

    def generate_return_types_init(
        self,
        sdk_methods: list[MethodSDK],
    ) -> None:
        """

        :param sdk_methods:
        :return:
        """
        template = Template(
            filename=str(self.method_return_types_init_template_path),
        )
        filepath = self.sdk_return_types_output_path / "__init__.py"
        sorted_methods = sorted(sdk_methods, key=lambda m: m.py_method_name)
        result = template.render(sdk_methods=sorted_methods)
        filepath.write_text(result)

    def generate_return_types(
        self,
        sdk_methods: list[MethodSDK],
    ) -> None:
        """
        :param sdk_methods:
        :return:
        """
        if self.remove_existing_types:
            for path in self.sdk_return_types_output_path.iterdir():
                if path.is_file() and path.suffix == ".py":
                    path.unlink()

        template = Template(
            filename=str(self.method_return_type_template_path),
        )

        for method in sdk_methods:
            self.create_method_return_type(
                template=template,
                method=method,
            )

        self.generate_return_types_init(sdk_methods=sdk_methods)
        log.info(
            "Python return types generated at %s",
            self.sdk_return_types_output_path,
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
        methods: list[MethodSDK] = self.read_methods_from_json()
        self.generate_return_types(sdk_methods=methods)
        self.render_methods_to_sdk_script(sdk_methods=methods)
        return methods
