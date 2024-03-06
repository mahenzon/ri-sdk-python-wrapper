import logging

from pre_commit.main import main as run_pre_commit

from ri_sdk_codegen import config
from ri_sdk_codegen.codegen_params import CodegenParams, get_params
from ri_sdk_codegen.crawl_for_urls import DocsUrlCrawler
from ri_sdk_codegen.generate import Codegen

log = logging.getLogger(__name__)


def post_run_formatting(codegen_params: CodegenParams) -> None:
    run_pre_commit(
        [
            "run",
            "--files",
            *(
                str(f)
                for f in codegen_params.ri_sdk_python_code_src_dir.glob(
                    "**/*.py",
                )
                if f.is_file()
            ),
            *(
                str(f)
                for f in codegen_params.ri_sdk_codegen_dir.glob("**/*.json")
                if f.is_file()
            ),
            *(
                str(f)
                for f in codegen_params.ri_sdk_codegen_dir.glob("**/*.yaml")
                if f.is_file()
            ),
            *(
                str(f)
                for f in codegen_params.ri_sdk_codegen_dir.glob("**/*.txt")
                if f.is_file()
            ),
        ],
    )


def main() -> None:
    codegen_params = get_params()
    logging.basicConfig(
        level=logging.DEBUG if codegen_params.verbose else logging.INFO,
        datefmt=config.DATE_FORMAT,
        format=config.LOG_FORMAT,
    )

    log.debug("Codegen params: %s", codegen_params)

    if codegen_params.update_links:
        log.warning("-- Update links")
        crawler = DocsUrlCrawler(base_url=codegen_params.base_url)
        crawler.find_and_write_urls(
            docs_crawl_start_url=codegen_params.docs_crawl_start_url,
            filepath=codegen_params.ri_sdk_pages_file_path,
        )

    log.info("Init codegen")
    codegen = Codegen(
        codegen_base_dir=codegen_params.ri_sdk_codegen_dir,
        sdk_template_path=codegen_params.sdk_template_filepath,
        method_return_type_template_path=codegen_params.method_return_type_template_filepath,
        method_return_types_init_template_path=codegen_params.method_return_types_init_filepath,
        sdk_output_file_path=codegen_params.output_py_script,
        sdk_return_types_output_path=codegen_params.ri_sdk_python_types_dir,
        sort_by_name=codegen_params.sort_methods,
        remove_existing_types=codegen_params.remove_existing_types,
    )

    if codegen_params.parse_docs:
        log.warning("-- Parse docs to caches files")
        urls = codegen_params.ri_sdk_pages_file_path.read_text().splitlines()
        codegen.parse_docs_and_save_methods_to_json_cache(urls)

    if codegen_params.generate_sdk:
        log.warning("-- Generate SDK Wrapper")
        codegen.generate_sdk_script()

    log.warning("Almost done.. formatting")
    post_run_formatting(codegen_params)
    log.warning("Done!")


if __name__ == "__main__":
    main()
