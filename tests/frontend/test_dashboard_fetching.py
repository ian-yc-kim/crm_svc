import importlib
from datetime import date
from types import SimpleNamespace

import streamlit as st
import httpx


def _make_spinner_recorder(record):
    class Spinner:
        def __init__(self, msg):
            record.append(msg)

        def __enter__(self):
            return None

        def __exit__(self, exc_type, exc, tb):
            return False

    return Spinner


def test_fetchers_use_cache_decorator(monkeypatch):
    # patch streamlit.cache_data before importing module so decorator is applied
    def fake_cache_data(fn):
        fn._cached = True
        return fn

    monkeypatch.setattr(st, "cache_data", fake_cache_data)

    # minimal st.spinner to avoid actual spinner behavior
    monkeypatch.setattr(st, "spinner", lambda msg: _make_spinner_recorder([])(msg))

    mod = importlib.import_module("crm_svc.frontend.pages.dashboard")
    importlib.reload(mod)

    assert getattr(mod.fetch_sales_performance_data, "_cached", False) is True
    assert getattr(mod.fetch_team_productivity_data, "_cached", False) is True
    assert getattr(mod.fetch_customer_interaction_data, "_cached", False) is True
    assert getattr(mod.fetch_pipeline_analytics_data, "_cached", False) is True


def test_fetchers_call_httpx_with_params(monkeypatch):
    calls = []

    def fake_get(url, params=None, timeout=None):
        calls.append((url, params, timeout))

        class Resp:
            def raise_for_status(self):
                return None

            def json(self):
                return {"url": url, "params": params}

        return Resp()

    # ensure decorator and spinner are stubbed
    monkeypatch.setattr(st, "cache_data", lambda fn: fn)
    spinner_calls = []
    monkeypatch.setattr(st, "spinner", lambda msg: _make_spinner_recorder(spinner_calls)(msg))

    monkeypatch.setattr(httpx, "get", fake_get)

    mod = importlib.import_module("crm_svc.frontend.pages.dashboard")
    importlib.reload(mod)

    sd = date(2023, 1, 1)
    ed = date(2023, 1, 10)

    r1 = mod.fetch_sales_performance_data(sd, ed)
    assert r1["params"]["start_date"] == sd.isoformat()
    assert r1["params"]["end_date"] == ed.isoformat()
    assert any("Loading sales performance" in s for s in spinner_calls)

    r2 = mod.fetch_team_productivity_data(sd, ed)
    assert r2["params"]["start_date"] == sd.isoformat()

    r3 = mod.fetch_customer_interaction_data(sd, ed)
    assert r3["params"]["start_date"] == sd.isoformat()

    r4 = mod.fetch_pipeline_analytics_data(sd, ed)
    assert r4["params"]["start_date"] == sd.isoformat()

    # validate urls used
    expected_urls = {
        f"{mod.BASE_URL}/sales-performance",
        f"{mod.BASE_URL}/team-productivity",
        f"{mod.BASE_URL}/customer-interaction",
        f"{mod.BASE_URL}/pipeline-analytics",
    }
    called_urls = {c[0] for c in calls}
    assert expected_urls == called_urls


def test_fetchers_handle_http_errors(monkeypatch):
    # raise HTTPStatusError from httpx.get
    def raise_http_status(*args, **kwargs):
        raise httpx.HTTPStatusError(message="err", request=None, response=None)

    monkeypatch.setattr(st, "cache_data", lambda fn: fn)
    err_calls = []
    monkeypatch.setattr(st, "error", lambda msg: err_calls.append(msg))

    monkeypatch.setattr(httpx, "get", raise_http_status)

    mod = importlib.import_module("crm_svc.frontend.pages.dashboard")
    importlib.reload(mod)

    sd = date(2023, 1, 1)
    ed = date(2023, 1, 2)

    assert mod.fetch_sales_performance_data(sd, ed) is None
    assert any("server returned an error" in e or "Failed to fetch" in e for e in err_calls)


def test_fetchers_handle_request_errors(monkeypatch):
    def raise_request_error(*args, **kwargs):
        raise httpx.RequestError("network")

    monkeypatch.setattr(st, "cache_data", lambda fn: fn)
    err_calls = []
    monkeypatch.setattr(st, "error", lambda msg: err_calls.append(msg))

    monkeypatch.setattr(httpx, "get", raise_request_error)

    mod = importlib.import_module("crm_svc.frontend.pages.dashboard")
    importlib.reload(mod)

    sd = date(2023, 2, 1)
    ed = date(2023, 2, 2)

    assert mod.fetch_team_productivity_data(sd, ed) is None
    assert any("Network error" in e or "Network error while fetching" in e for e in err_calls)


def test_render_dashboard_displays_raw_json(monkeypatch):
    # prepare stubbed responses
    def fake_get(url, params=None, timeout=None):
        class Resp:
            def raise_for_status(self):
                return None

            def json(self):
                return {"url": url, "params": params}

        return Resp()

    # stub streamlit UI pieces
    monkeypatch.setattr(st, "cache_data", lambda fn: fn)
    displayed = {"json": []}

    monkeypatch.setattr(st, "json", lambda payload: displayed["json"].append(payload))
    monkeypatch.setattr(st, "info", lambda _msg: None)
    monkeypatch.setattr(st, "warning", lambda _msg: None)
    monkeypatch.setattr(st, "set_page_config", lambda **kw: None)

    # stub date inputs and session auth
    monkeypatch.setitem(st.session_state, "authenticated", True)
    monkeypatch.setattr(st, "date_input", lambda *a, **kw: date(2023, 3, 1))

    monkeypatch.setattr(httpx, "get", fake_get)

    mod = importlib.import_module("crm_svc.frontend.pages.dashboard")
    importlib.reload(mod)

    # call render
    mod.render_dashboard()

    # Four sections should have been displayed
    assert len(displayed["json"]) == 4
    for payload in displayed["json"]:
        assert "url" in payload and "params" in payload
