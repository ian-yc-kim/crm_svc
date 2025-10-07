import logging
from typing import Dict, Optional

import streamlit as st

logger = logging.getLogger(__name__)


def set_screen_width(width: int) -> None:
    """Store the detected client screen width into Streamlit session state.

    Use this function (for example) from a small JS bridge that reports screen
    width. Tests may call this directly to simulate different devices.
    """
    try:
        st.session_state["screen_width"] = int(width)
    except Exception as e:
        logger.error(e, exc_info=True)


def get_screen_width(default: int = 1024) -> int:
    """Retrieve stored screen width from session state or return default.

    Ensures int value is returned and logs exceptions per coding rules.
    """
    try:
        val = st.session_state.get("screen_width", default)
        return int(val)
    except Exception as e:
        logger.error(e, exc_info=True)
        return default


def is_mobile_view(threshold: int = 768, width: Optional[int] = None) -> bool:
    """Return True when the provided or stored width is less than or equal threshold.

    If width is None, the function will try to read from session state.
    """
    try:
        w = width if width is not None else get_screen_width()
        return int(w) <= int(threshold)
    except Exception as e:
        logger.error(e, exc_info=True)
        # Fail-safe: treat as desktop when uncertain
        return False


def breakpoint_thresholds() -> Dict[str, int]:
    """Return commonly used breakpoint thresholds.

    Useful for consistent usage across components.
    """
    return {"sm": 576, "md": 768, "lg": 992}
