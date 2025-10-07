import logging
from datetime import date
from typing import Optional, Dict, Any

import httpx
import streamlit as st

logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000/api"


def _is_streamlit_runtime() -> bool:
    """Return True when running inside a Streamlit script runtime."""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        return get_script_run_ctx() is not None
    except Exception as e:
        # Log minimal errors per coding rules and return False for non-Streamlit contexts
        logger.error(e, exc_info=True)
        return False


@st.cache_data
def fetch_sales_performance_data(start_date: date, end_date: date) -> Optional[Dict[str, Any]]:
    """Fetch sales performance metrics from backend API for given date range."""
    url = f"{BASE_URL}/sales-performance"
    params = {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()}
    try:
        with st.spinner("Loading sales performance..."):
            resp = httpx.get(url, params=params, timeout=10.0)
            resp.raise_for_status()
            return resp.json()
    except httpx.RequestError as e:
        logger.error(e, exc_info=True)
        st.error("Network error while fetching sales performance. Please try again.")
        return None
    except httpx.HTTPStatusError as e:
        logger.error(e, exc_info=True)
        st.error("Failed to fetch sales performance: server returned an error.")
        return None
    except Exception as e:
        logger.error(e, exc_info=True)
        st.error("Unexpected error while fetching sales performance.")
        return None


@st.cache_data
def fetch_team_productivity_data(start_date: date, end_date: date) -> Optional[Dict[str, Any]]:
    """Fetch team productivity metrics from backend API for given date range."""
    url = f"{BASE_URL}/team-productivity"
    params = {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()}
    try:
        with st.spinner("Loading team productivity..."):
            resp = httpx.get(url, params=params, timeout=10.0)
            resp.raise_for_status()
            return resp.json()
    except httpx.RequestError as e:
        logger.error(e, exc_info=True)
        st.error("Network error while fetching team productivity. Please try again.")
        return None
    except httpx.HTTPStatusError as e:
        logger.error(e, exc_info=True)
        st.error("Failed to fetch team productivity: server returned an error.")
        return None
    except Exception as e:
        logger.error(e, exc_info=True)
        st.error("Unexpected error while fetching team productivity.")
        return None


@st.cache_data
def fetch_customer_interaction_data(start_date: date, end_date: date) -> Optional[Dict[str, Any]]:
    """Fetch customer interaction metrics from backend API for given date range."""
    url = f"{BASE_URL}/customer-interaction"
    params = {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()}
    try:
        with st.spinner("Loading customer interaction..."):
            resp = httpx.get(url, params=params, timeout=10.0)
            resp.raise_for_status()
            return resp.json()
    except httpx.RequestError as e:
        logger.error(e, exc_info=True)
        st.error("Network error while fetching customer interaction. Please try again.")
        return None
    except httpx.HTTPStatusError as e:
        logger.error(e, exc_info=True)
        st.error("Failed to fetch customer interaction: server returned an error.")
        return None
    except Exception as e:
        logger.error(e, exc_info=True)
        st.error("Unexpected error while fetching customer interaction.")
        return None


@st.cache_data
def fetch_pipeline_analytics_data(start_date: date, end_date: date) -> Optional[Dict[str, Any]]:
    """Fetch pipeline analytics metrics from backend API for given date range."""
    url = f"{BASE_URL}/pipeline-analytics"
    params = {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()}
    try:
        with st.spinner("Loading pipeline analytics..."):
            resp = httpx.get(url, params=params, timeout=10.0)
            resp.raise_for_status()
            return resp.json()
    except httpx.RequestError as e:
        logger.error(e, exc_info=True)
        st.error("Network error while fetching pipeline analytics. Please try again.")
        return None
    except httpx.HTTPStatusError as e:
        logger.error(e, exc_info=True)
        st.error("Failed to fetch pipeline analytics: server returned an error.")
        return None
    except Exception as e:
        logger.error(e, exc_info=True)
        st.error("Unexpected error while fetching pipeline analytics.")
        return None


def render_dashboard() -> None:
    """Render a simple CRM Reporting Dashboard.

    This function is safe to import and does not run automatically
    unless executed inside a Streamlit runtime.
    """
    # Best-effort page configuration
    try:
        st.set_page_config(page_title="CRM Reporting Dashboard", layout="wide")
    except Exception as e:
        logger.error(e, exc_info=True)

    # Placeholder authentication check using session_state
    authenticated = st.session_state.get("authenticated", False)
    if not authenticated:
        st.warning("Please log in to view the dashboard.")
        return

    # Main UI
    st.header("CRM Reporting Dashboard")

    today = date.today()
    start_date = st.date_input("Start date", value=today, key="start_date")
    end_date = st.date_input("End date", value=today, key="end_date")

    # Sales performance section
    st.subheader("Sales Performance")
    sales = fetch_sales_performance_data(start_date, end_date)
    if sales:
        st.json(sales)
    else:
        st.info("No sales performance data available")

    # Team productivity section
    st.subheader("Team Productivity")
    team = fetch_team_productivity_data(start_date, end_date)
    if team:
        st.json(team)
    else:
        st.info("No team productivity data available")

    # Customer interaction section
    st.subheader("Customer Interaction")
    customer = fetch_customer_interaction_data(start_date, end_date)
    if customer:
        st.json(customer)
    else:
        st.info("No customer interaction data available")

    # Pipeline analytics section
    st.subheader("Pipeline Analytics")
    pipeline = fetch_pipeline_analytics_data(start_date, end_date)
    if pipeline:
        st.json(pipeline)
    else:
        st.info("No pipeline analytics data available")


# Only auto-run UI when inside a Streamlit runtime
if _is_streamlit_runtime():
    try:
        render_dashboard()
    except Exception as e:
        logger.error(e, exc_info=True)
