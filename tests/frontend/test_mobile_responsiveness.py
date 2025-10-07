import importlib

import streamlit as st


def test_get_mobile_base_css_contains_rules():
    mod = importlib.import_module("crm_svc.frontend.components.mobile_components")
    importlib.reload(mod)
    css = mod.get_mobile_base_css()
    assert isinstance(css, str)
    assert "@media (max-width: 768px)" in css
    assert ".stButton > button" in css
    assert "min-height: 44px" in css
    assert ".mobile-only" in css and ".desktop-only" in css


def test_inject_mobile_base_css_calls_markdown(monkeypatch):
    calls = []

    def fake_markdown(content, unsafe_allow_html=False):
        calls.append((content, unsafe_allow_html))

    monkeypatch.setattr(st, "markdown", fake_markdown)

    mod = importlib.import_module("crm_svc.frontend.components.mobile_components")
    importlib.reload(mod)

    mod.inject_mobile_base_css()
    assert len(calls) == 1
    content, unsafe = calls[0]
    assert unsafe is True
    assert "<style>" in content
    assert "@media (max-width: 768px)" in content


def test_inject_mobile_base_css_noop_when_empty(monkeypatch):
    calls = []

    def fake_markdown(*a, **k):
        calls.append(True)

    # ensure our module returns empty css
    mod = importlib.import_module("crm_svc.frontend.components.mobile_components")
    # patch the getter to simulate empty css
    monkeypatch.setattr(mod, "get_mobile_base_css", lambda: "")
    monkeypatch.setattr(st, "markdown", fake_markdown)

    # call injection; should be no-op when CSS empty
    mod.inject_mobile_base_css()
    assert calls == []


def test_inject_viewport_meta_calls_markdown(monkeypatch):
    calls = []

    def fake_markdown(content, unsafe_allow_html=False):
        calls.append((content, unsafe_allow_html))

    monkeypatch.setattr(st, "markdown", fake_markdown)

    mod = importlib.import_module("crm_svc.frontend.components.mobile_components")
    importlib.reload(mod)

    mod.inject_viewport_meta()
    assert any("meta name=\"viewport\"" in c[0] for c in calls)


def test_set_get_screen_width_and_mobile_logic():
    mu = importlib.import_module("crm_svc.frontend.utils.mobile_utils")
    importlib.reload(mu)

    # clean up any prior session state
    if "screen_width" in st.session_state:
        del st.session_state["screen_width"]

    # default when not set
    assert mu.get_screen_width(default=800) == 800

    # set and retrieve
    mu.set_screen_width(375)
    assert mu.get_screen_width(default=1024) == 375

    # direct width checks
    assert mu.is_mobile_view(threshold=768, width=320) is True
    assert mu.is_mobile_view(threshold=768, width=1024) is False

    # session-state based checks
    st.session_state["screen_width"] = 600
    assert mu.is_mobile_view() is True
    st.session_state["screen_width"] = 1200
    assert mu.is_mobile_view() is False


def test_breakpoint_thresholds_returns_map():
    mu = importlib.import_module("crm_svc.frontend.utils.mobile_utils")
    bp = mu.breakpoint_thresholds()
    assert isinstance(bp, dict)
    assert bp["md"] == 768
