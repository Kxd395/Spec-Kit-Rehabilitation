"""Integration tests for banner and basic flow"""
from specify_cli.ui.banner import show_banner
from rich.console import Console

def test_banner_displays_without_error():
    """Ensure banner can be displayed"""
    try:
        show_banner()
        assert True
    except Exception as e:
        assert False, f"Banner failed: {e}"

def test_banner_accepts_custom_console():
    """Ensure banner works with custom console"""
    console = Console()
    show_banner(console)
    # If no exception, test passes
    assert True

def test_banner_import_from_compat():
    """Ensure backward compatibility through compat module"""
    from specify_cli.compat import show_banner as banner_compat
    try:
        banner_compat()
        assert True
    except Exception as e:
        assert False, f"Compat import failed: {e}"
