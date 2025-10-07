import logging
from typing import Final

import streamlit as st

logger = logging.getLogger(__name__)

MOBILE_BREAKPOINT: Final[int] = 768


def get_mobile_base_css() -> str:
    """Return base responsive CSS string for mobile-friendly Streamlit UI.

    The CSS includes a mobile breakpoint for max-width: 768px, utility classes
    (.mobile-only, .desktop-only), touch-friendly rules for buttons/inputs and
    container spacing adjustments.
    """
    try:
        css = """
/* Base adjustments for touch-friendly UI */
.stButton > button,
input[type="text"],
input[type="email"],
input[type="number"],
select,
textarea {
  min-height: 44px !important; /* Android/iOS recommended touch target */
  padding: 12px 14px !important;
  font-size: 16px !important;
  border-radius: 8px !important;
}

.block-container {
  padding-left: 1.25rem !important;
  padding-right: 1.25rem !important;
}

/* Utility classes to selectively show/hide content */
.mobile-only { display: none !important; }
.desktop-only { display: block !important; }

/* Responsive rules for narrow screens */
@media (max-width: 768px) {
  .stApp, .main, .block-container {
    padding-left: 0.75rem !important;
    padding-right: 0.75rem !important;
  }

  .mobile-only { display: block !important; }
  .desktop-only { display: none !important; }

  /* Increase spacing and legibility */
  h1, h2, h3, h4, h5, h6 {
    line-height: 1.2 !important;
  }

  .stButton > button {
    width: 100% !important;
    min-height: 48px !important;
    padding: 14px 16px !important;
    font-size: 18px !important;
  }

  input[type="text"], select, textarea {
    font-size: 16px !important;
    min-height: 44px !important;
    padding: 12px 12px !important;
  }
}
"""
        return css
    except Exception as e:
        logger.error(e, exc_info=True)
        # On unexpected error, return minimal safe CSS
        return ""


def inject_mobile_base_css() -> None:
    """Inject mobile base CSS into the Streamlit app using st.markdown.

    Wrapped in try/except to avoid import-time errors when Streamlit is not
    available at runtime.
    """
    try:
        css = get_mobile_base_css()
        if not css:
            return
        # wrap in style tag so markdown injection applies CSS
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception as e:
        logger.error(e, exc_info=True)


def inject_viewport_meta() -> None:
    """Inject viewport meta tag for proper mobile scaling via st.markdown.

    This helps mobile browsers render the Streamlit app at the device width and
    appropriate initial scale.
    """
    try:
        meta = '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">'
        st.markdown(meta, unsafe_allow_html=True)
    except Exception as e:
        logger.error(e, exc_info=True)
