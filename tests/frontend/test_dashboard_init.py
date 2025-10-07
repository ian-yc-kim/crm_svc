import importlib


def test_dashboard_module_importable():
    """Ensure the dashboard module can be imported and exposes a render function."""
    module_name = "crm_svc.frontend.pages.dashboard"
    mod = importlib.import_module(module_name)
    importlib.reload(mod)
    assert hasattr(mod, "render_dashboard")
    assert callable(getattr(mod, "render_dashboard"))
    assert hasattr(mod, "_is_streamlit_runtime")
    assert callable(getattr(mod, "_is_streamlit_runtime"))
