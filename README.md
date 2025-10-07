# crm_svc

## Mobile-Friendly Responsive Design

Overview

This project includes a lightweight mobile-friendly responsive design layer for the Streamlit frontend to improve usability on small screens and touch devices. The goals are:
- Provide readable layouts on narrow screens
- Improve touch targets and spacing for finger input
- Offer simple utilities to detect mobile view and conditionally render UI
- Keep performance friendly for mobile devices

Responsive Layouts

We use a breakpoint-driven approach to adapt layouts and spacing. The mobile CSS and viewport meta tag should be injected early in a Streamlit page so that layout, spacing, and touch targets are applied immediately.

Key helpers

- src/crm_svc/frontend/components/mobile_components.py
  - MOBILE_BREAKPOINT: default breakpoint (768px)
  - get_mobile_base_css(): returns the base CSS string for responsive rules
  - inject_mobile_base_css(): injects the CSS into the Streamlit page using st.markdown
  - inject_viewport_meta(): injects a viewport meta tag so mobile browsers scale the app correctly

- src/crm_svc/frontend/utils/mobile_utils.py
  - set_screen_width(width): set the detected client width into Streamlit session_state
  - get_screen_width(default=1024): read stored width or return default
  - is_mobile_view(threshold=768, width=None): determine whether current/supplied width is mobile
  - breakpoint_thresholds(): common breakpoint thresholds map (sm/md/lg)

Typical placement

Place the viewport and CSS injection near the top of your Streamlit page (for example, in a page's render function) so that responsive rules take effect before most UI renders. Example:

```python
import streamlit as st
from crm_svc.frontend.components.mobile_components import (
    inject_viewport_meta,
    inject_mobile_base_css,
)
from crm_svc.frontend.utils.mobile_utils import set_screen_width, is_mobile_view

st.set_page_config(page_title="CRM Reporting Dashboard", layout="wide")

# Inject meta and CSS for mobile-friendly behavior
inject_viewport_meta()
inject_mobile_base_css()

# Optionally set screen width reported by client-side JS bridge
# set_screen_width(375)  # Example: test or JS-reported value

mobile = is_mobile_view()
if mobile:
    # adjust UI for stacked layout and larger controls
    pass
```

Mobile-Optimized Navigation

- Avoid relying on hover-only interactions; on mobile, ensure critical actions are accessible via taps.
- Consider collapsing secondary controls into mobile-only panels using the utility CSS classes (.mobile-only, .desktop-only).
- Keep primary actions within thumb-reachable areas and avoid deep nested menus.

Touch-Friendly Interface Elements

- CSS increases minimum heights, padding, and font sizes of buttons and form controls to meet common touch target recommendations (~44px).
- Use wider spacing and larger touch targets for important actions (e.g. primary buttons) via provided CSS or additional rules.
- Prefer single-column stacked inputs for small screens to reduce accidental taps and scrolling friction.

Performance Considerations

- Minimize heavy components in initial render on mobile. Lazy-load or collapse non-critical widgets.
- Cache network calls and large data transformations (Streamlit's st.cache_data is used in dashboard fetchers).
- Use simplified chart variants for mobile (less series, fewer markers) and rely on use_container_width=True for responsive charts.

File Overview

- frontend/components/mobile_components.py: Contains CSS and meta injection helpers. Keep CSS conservative and test across device widths.
- frontend/utils/mobile_utils.py: Session-state helpers and detection logic. Tests simulate widths via set_screen_width.

Usage Examples

- Inject viewport and CSS as shown above near the page start.
- Use set_screen_width(width) from a small JS bridge to report client width when available. Fall back to get_screen_width(default).
- Branch UI logic with is_mobile_view() to pick stacked vs multi-column layouts.

Extending and Maintenance Guide

- Adjust MOBILE_BREAKPOINT in mobile_components.py to change the primary breakpoint.
- Add new responsive CSS rules in get_mobile_base_css(); keep rules scoped and additive to avoid conflicts with Streamlit classes.
- Extend breakpoint_thresholds() to expose additional breakpoints and reference them across components for consistency.
- Add tests whenever you change class names, API functions, or CSS semantics; tests in tests/frontend/ already validate CSS presence and injection behavior.

Testing

- There is a small test added to tests/docs/ that asserts README contains the Mobile-Friendly Responsive Design header and references to the new modules and key helper functions. Keep documentation updated when code APIs change.

Maintenance tips

- Document any new utility functions or CSS classes you add in this section so future maintainers know where to look and how to test.
- Use the existing frontend unit tests to validate injection points and mobile utility behavior when you change thresholds or CSS.
