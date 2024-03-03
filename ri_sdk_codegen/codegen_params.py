import argparse
from dataclasses import dataclass
from pathlib import Path

from .config import TYPES_MODULE_NAME

BASE_DIR = Path(__file__).resolve().parent.parent
RI_SDK_CODEGEN_DIR = BASE_DIR / ".ri_sdk_codegen"
RI_SDK_PYTHON_CODE_SRC_DIR = BASE_DIR / "ri_sdk"
RI_SDK_PYTHON_TYPES_DIR = RI_SDK_PYTHON_CODE_SRC_DIR / TYPES_MODULE_NAME

ALL_RI_SDK_PAGES_FILENAME = "ri_sdk_pages.txt"
RI_SDK_PAGES_FILEPATH = RI_SDK_CODEGEN_DIR / ALL_RI_SDK_PAGES_FILENAME
URL_BASE = "https://docs.robointellect.ru"

ROBOINTELLECT_BASE_SDK_FILENAME = "robointellect_base_sdk.py"
ROBOINTELLECT_SDK_OUTPUT_FILEPATH = Path(
    RI_SDK_PYTHON_CODE_SRC_DIR / ROBOINTELLECT_BASE_SDK_FILENAME,
)
MAKO_TEMPLATE_RI_SDK_FILENAME = "ri_sdk_base_wrapper.py.template.mako"
MAKO_TEMPLATE_RI_SDK_METHOD_RETURN_TYPE_FILENAME = (
    "ri_sdk_method_return_type.py.template.mako"
)
MAKO_TEMPLATE_RI_SDK_METHOD_RETURN_TYPES_INIT_FILENAME = (
    "ri_sdk_types_init.py.template.mako"
)
TEMPLATE_FOLDER_NAME = "templates"
TEMPLATE_FOLDER_DIR = BASE_DIR / "ri_sdk_codegen" / TEMPLATE_FOLDER_NAME
MAKO_TEMPLATE_RI_SDK_FILEPATH = (
    TEMPLATE_FOLDER_DIR / MAKO_TEMPLATE_RI_SDK_FILENAME
)
MAKO_TEMPLATE_RI_SDK_METHOD_RETURN_TYPE_FILEPATH = (
    TEMPLATE_FOLDER_DIR / MAKO_TEMPLATE_RI_SDK_METHOD_RETURN_TYPE_FILENAME
)
MAKO_TEMPLATE_RI_SDK_METHOD_RETURN_TYPES_INIT_FILEPATH = (
    TEMPLATE_FOLDER_DIR
    / MAKO_TEMPLATE_RI_SDK_METHOD_RETURN_TYPES_INIT_FILENAME
)
DOCS_ENTRY_PATH = "/docs/category/ri-sdk-api"

parser = argparse.ArgumentParser(
    description="Generate SDK for RI SDK based on docs.",
)
parser.add_argument(
    "--update-links",
    action="store_true",
    help="Update links (default: False). "
    "Crawls RI SDK docs for all RI_SDK_ pages.",
)
parser.add_argument(
    "--parse-docs",
    action="store_true",
    help="Pars SDK docs and create json files w/ info (default: False). "
    "Rewrites existing json files.",
)
parser.add_argument(
    "--generate-sdk",
    action="store_true",
    help="Generate SDK (default: False). Rewrites existing code.",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Show verbose output (debug logs).",
)
parser.add_argument(
    "--sort-methods",
    action="store_true",
    default=True,
    help="Generate SDK with sorted methods.",
)
parser.add_argument(
    "--base-url",
    default=URL_BASE,
    help=f"Base URL (default: {URL_BASE})",
    type=str,
)
parser.add_argument(
    "--docs-entry-path",
    default=DOCS_ENTRY_PATH,
    help=f"Where to start crawling from (default: {DOCS_ENTRY_PATH})",
    type=str,
)
parser.add_argument(
    "--pages-urls-filepath",
    default=RI_SDK_PAGES_FILEPATH,
    help=f"Where to store known urls (default: {RI_SDK_PAGES_FILEPATH})",
    type=Path,
)
parser.add_argument(
    "--output-py-script",
    default=ROBOINTELLECT_SDK_OUTPUT_FILEPATH,
    help="File path for the output file script "
    f"(default: {ROBOINTELLECT_SDK_OUTPUT_FILEPATH})",
    type=Path,
)


@dataclass
class CodegenParams:
    update_links: bool = False
    parse_docs: bool = False
    generate_sdk: bool = False
    verbose: bool = False
    sort_methods: bool = True
    remove_existing_types: bool = True
    base_url: str = URL_BASE
    docs_entry_path: str = DOCS_ENTRY_PATH
    ri_sdk_pages_file_path: Path = RI_SDK_PAGES_FILEPATH
    output_py_script: Path = ROBOINTELLECT_SDK_OUTPUT_FILEPATH
    sdk_template_filepath: Path = MAKO_TEMPLATE_RI_SDK_FILEPATH
    method_return_type_template_filepath: Path = (
        MAKO_TEMPLATE_RI_SDK_METHOD_RETURN_TYPE_FILEPATH
    )
    method_return_types_init_filepath: Path = (
        MAKO_TEMPLATE_RI_SDK_METHOD_RETURN_TYPES_INIT_FILEPATH
    )
    ri_sdk_codegen_dir: Path = RI_SDK_CODEGEN_DIR
    ri_sdk_python_code_src_dir: Path = RI_SDK_PYTHON_CODE_SRC_DIR
    ri_sdk_python_types_dir: Path = RI_SDK_PYTHON_TYPES_DIR

    @property
    def docs_crawl_start_url(self) -> str:
        return self.base_url + self.docs_entry_path


def get_params() -> CodegenParams:
    args = parser.parse_args()
    return CodegenParams(
        update_links=args.update_links,
        parse_docs=args.parse_docs,
        generate_sdk=args.generate_sdk,
        verbose=args.verbose,
        sort_methods=args.sort_methods,
        base_url=args.base_url,
        ri_sdk_pages_file_path=args.pages_urls_filepath,
        output_py_script=args.output_py_script,
    )
