from crm_svc.frontend.utils.mobile_utils import (
    set_screen_width,
    get_screen_width,
    is_mobile_view,
    breakpoint_thresholds,
)
import streamlit as st


def test_set_and_get_screen_width(monkeypatch):
    # ensure session_state clean
    if "screen_width" in st.session_state:
        del st.session_state["screen_width"]

    # default when not set
    assert get_screen_width(default=800) == 800

    set_screen_width(375)
    assert get_screen_width(default=1024) == 375


def test_is_mobile_view_with_direct_width():
    assert is_mobile_view(threshold=768, width=320) is True
    assert is_mobile_view(threshold=768, width=1024) is False


def test_is_mobile_view_using_session_state():
    st.session_state["screen_width"] = 600
    assert is_mobile_view() is True
    st.session_state["screen_width"] = 1200
    assert is_mobile_view() is False


def test_breakpoint_thresholds_returns_map():
    bp = breakpoint_thresholds()
    assert isinstance(bp, dict)
    assert bp["md"] == 768
