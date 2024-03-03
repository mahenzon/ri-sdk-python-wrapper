INDENT_SIZE: int = 4
INDENT_VALUE: str = " "
REGULAR_INDENT: str = INDENT_VALUE * INDENT_SIZE
METHOD_BODY_INDENT: str = REGULAR_INDENT * 2
PARAM_PREFIX_TEMPLATE: str = "{indent}:param {name}: "
METHOD_PARAM_SUBSEQUENT_INDENT: str = REGULAR_INDENT * 3
IN_METHOD_COMMENT: str = "{indent}# {name} - "
IN_METHOD_SUBSEQUENT_COMMENT: str = f"{{indent}}#{REGULAR_INDENT}"
DEFAULT_MAX_WIDTH: int = 69
