import importlib

import streamlit as st

from crm_svc.frontend.components.mobile_components import get_mobile_base_css


def test_get_mobile_base_css_contains_rules():
    css = get_mobile_base_css()
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

    # reload module to ensure functions bound
    importlib.reload(importlib.import_module("crm_svc.frontend.components.mobile_components"))
    mod = importlib.import_module("crm_svc.frontend.components.mobile_components")

    # call injection
    mod.inject_mobile_base_css()
    assert len(calls) == 1
    content, unsafe = calls[0]
    assert unsafe is True
    assert "@media (max-width: 768px)" in content


def test_inject_viewport_meta_calls_markdown(monkeypatch):
    calls = []

    def fake_markdown(content, unsafe_allow_html=False):
        calls.append((content, unsafe_allow_html))

    monkeypatch.setattr(st, "markdown", fake_markdown)

    mod = importlib.import_module("crm_svc.frontend.components.mobile_components")
    importlib.reload(mod)

    mod.inject_viewport_meta()
    assert any("meta name=\"viewport\"" in c[0] for c in calls)
