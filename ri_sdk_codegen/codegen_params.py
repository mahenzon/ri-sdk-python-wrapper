import argparse
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ALL_RI_SDK_PAGES_FILE_NAME = "ri_sdk_pages.txt"
RI_SDK_PAGES_FILE_PATH = BASE_DIR / ALL_RI_SDK_PAGES_FILE_NAME
URL_BASE = "https://docs.robointellect.ru"

ROBOINTELLECT_BASE_SDK_FILENAME = "robointellect_base_sdk.py"
ROBOINTELLECT_SDK_OUTPUT_FILEPATH = Path(
    BASE_DIR / "src" / ROBOINTELLECT_BASE_SDK_FILENAME
)
MAKO_TEMPLATE_FILENAME = "template.robointellect_base_sdk.py.mako"
MAKO_TEMPLATE_FILEPATH = BASE_DIR / "ri_sdk_codegen" / MAKO_TEMPLATE_FILENAME


parser = argparse.ArgumentParser(
    description="Generate SDK for RI SDK based on docs.",
)
parser.add_argument(
    "--update-links",
    action="store_true",
    help="Update links (default: False). Crawls RI SDK docs for all RI_SDK_ pages.",
)
parser.add_argument(
    "--generate-sdk",
    action="store_true",
    help="Generate SDK (default: False). Rewrites existing code.",
)
parser.add_argument(
    "--base-url",
    default=URL_BASE,
    help=f"Base URL (default: {URL_BASE})",
    type=str,
)
parser.add_argument(
    "--pages-urls-filepath",
    default=RI_SDK_PAGES_FILE_PATH,
    help=f"Where to store known urls (default: {RI_SDK_PAGES_FILE_PATH})",
    type=Path,
)
parser.add_argument(
    "--output-py-script",
    default=ROBOINTELLECT_SDK_OUTPUT_FILEPATH,
    help=f"File path for the output file script (default: {ROBOINTELLECT_SDK_OUTPUT_FILEPATH})",
    type=Path,
)
parser.add_argument(
    "--sdk-template-filepath",
    default=MAKO_TEMPLATE_FILEPATH,
    help=f"File path for the Mako template (default: {MAKO_TEMPLATE_FILEPATH})",
    type=Path,
)


@dataclass
class CodegenParams:
    update_links: bool = False
    generate_sdk: bool = False
    base_url: str = URL_BASE
    ri_sdk_pages_file_path: Path = RI_SDK_PAGES_FILE_PATH
    output_py_script: Path = ROBOINTELLECT_SDK_OUTPUT_FILEPATH
    sdk_template_filepath: Path = MAKO_TEMPLATE_FILEPATH


def get_params() -> CodegenParams:
    args = parser.parse_args()
    return CodegenParams(
        update_links=args.update_links,
        generate_sdk=args.generate_sdk,
        base_url=args.base_url,
        ri_sdk_pages_file_path=args.pages_urls_filepath,
        output_py_script=args.output_py_script,
        sdk_template_filepath=args.sdk_template_filepath,
    )