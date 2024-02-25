import logging
from pathlib import Path

from mako.template import Template

from ri_sdk_codegen import types

log = logging.getLogger(__name__)


def generate_sdk_script(
    sdk_methods: list[types.MethodSDK],
    sdk_template_path: Path,
    sdk_output_file_path: Path,
    sort_by_name: bool = True,
) -> None:
    """
    :param sdk_methods:
    :param sdk_template_path:
    :param sdk_output_file_path:
    :param sort_by_name:
    :return:
    """

    template = Template(filename=str(sdk_template_path))

    if sort_by_name:
        sdk_methods.sort(key=lambda m: m.name)
    # Render the template with the function name and parameters
    result = template.render(
        sdk_methods=sdk_methods,
    )
    # Write the rendered content to a new Python script
    sdk_output_file_path.write_text(result)

    log.info("New Python script generated at %s", sdk_output_file_path)
