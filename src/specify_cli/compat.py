# Backward compatible re-exports to cushion the refactor for one minor release
from .ui.banner import show_banner
from .github.auth import get_github_token as _github_token
from .github.auth import get_auth_headers as _github_auth_headers
from .github.download import download_template_from_github
from .github.extraction import download_and_extract_template, handle_vscode_settings, merge_json_files

__all__ = [
    "show_banner",
    "_github_token",
    "_github_auth_headers",
    "download_template_from_github",
    "download_and_extract_template",
    "handle_vscode_settings",
    "merge_json_files",
]

