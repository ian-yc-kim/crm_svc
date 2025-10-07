import base64
from datetime import date


def test_sales_performance_ok(client):
    resp = client.get(
        "/api/sales-performance",
        params={"start_date": "2023-01-01", "end_date": "2023-01-05"},
    )
    assert resp.status_code == 200
    j = resp.json()
    assert j["start_date"] == "2023-01-01"
    assert j["end_date"] == "2023-01-05"
    assert "revenue" in j and "conversion_rate" in j and "pipeline_velocity" in j


def test_team_productivity_ok(client):
    resp = client.get(
        "/api/team-productivity",
        params={"start_date": "2023-02-01", "end_date": "2023-02-03"},
    )
    assert resp.status_code == 200
    j = resp.json()
    assert j["start_date"] == "2023-02-01"
    assert j["end_date"] == "2023-02-03"
    assert "tasks_completed" in j and "deals_closed" in j and "activity_level" in j


def test_customer_interaction_ok(client):
    resp = client.get(
        "/api/customer-interaction",
        params={"start_date": "2023-03-01", "end_date": "2023-03-02"},
    )
    assert resp.status_code == 200
    j = resp.json()
    assert j["start_date"] == "2023-03-01"
    assert j["end_date"] == "2023-03-02"
    assert "total_interactions" in j and "avg_engagement_score" in j


def test_pipeline_analytics_ok(client):
    resp = client.get(
        "/api/pipeline-analytics",
        params={"start_date": "2023-04-01", "end_date": "2023-04-05"},
    )
    assert resp.status_code == 200
    j = resp.json()
    assert j["start_date"] == "2023-04-01"
    assert j["end_date"] == "2023-04-05"
    assert "stage_conversion_rates" in j
    assert isinstance(j["stage_conversion_rates"], dict)
    assert "lead" in j["stage_conversion_rates"]


def test_export_sales_csv_ok(client):
    resp = client.get(
        "/api/export",
        params={"start_date": "2023-05-01", "end_date": "2023-05-03", "report_type": "sales"},
    )
    assert resp.status_code == 200
    j = resp.json()
    assert j["filename"] == "report_sales.csv"
    assert j["content_type"] == "text/csv"
    data_b64 = j["data_b64"]
    decoded = base64.b64decode(data_b64).decode("utf-8")
    assert "start_date,end_date,revenue,conversion_rate,pipeline_velocity" in decoded


def test_export_pipeline_csv_ok(client):
    resp = client.get(
        "/api/export",
        params={"start_date": "2023-06-01", "end_date": "2023-06-05", "report_type": "pipeline"},
    )
    assert resp.status_code == 200
    j = resp.json()
    assert j["filename"] == "report_pipeline.csv"
    assert j["content_type"] == "text/csv"
    decoded = base64.b64decode(j["data_b64"]).decode("utf-8")
    assert "stage,rate" in decoded
    assert "lead," in decoded


def test_invalid_date_range_returns_422(client):
    # DateRangeQuery validation occurs at request parsing resulting in 422
    resp = client.get(
        "/api/sales-performance",
        params={"start_date": "2023-07-10", "end_date": "2023-07-01"},
    )
    assert resp.status_code == 422

    resp2 = client.get(
        "/api/export",
        params={"start_date": "2023-07-10", "end_date": "2023-07-01", "report_type": "sales"},
    )
    assert resp2.status_code == 422
