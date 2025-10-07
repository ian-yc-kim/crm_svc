from datetime import date

import plotly.graph_objects as go

from crm_svc.schemas.report import (
    SalesPerformanceResponse,
    TeamProductivityResponse,
    CustomerInteractionResponse,
    PipelineAnalyticsResponse,
)
from crm_svc.frontend.components.charts import (
    create_sales_performance_chart,
    create_team_productivity_chart,
    create_customer_interaction_chart,
    create_pipeline_analytics_chart,
)


def test_create_sales_performance_chart_normal():
    data = SalesPerformanceResponse(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 31),
        revenue=12345.67,
        conversion_rate=0.12,
        pipeline_velocity=3.4,
    )
    fig = create_sales_performance_chart(data)
    assert isinstance(fig, go.Figure)
    assert len(fig.data) >= 1
    trace = fig.data[0]
    assert list(trace["x"]) == ["revenue", "conversion_rate", "pipeline_velocity"]
    assert list(trace["y"]) == [12345.67, 0.12, 3.4]


def test_create_sales_performance_chart_zero_values():
    data = SalesPerformanceResponse(
        start_date=date(2025, 2, 1),
        end_date=date(2025, 2, 28),
        revenue=0.0,
        conversion_rate=0.0,
        pipeline_velocity=0.0,
    )
    fig = create_sales_performance_chart(data)
    assert isinstance(fig, go.Figure)
    trace = fig.data[0]
    assert list(trace["y"]) == [0.0, 0.0, 0.0]


def test_create_team_productivity_chart():
    data = TeamProductivityResponse(
        start_date=date(2025, 3, 1),
        end_date=date(2025, 3, 31),
        tasks_completed=50,
        deals_closed=5,
        activity_level=7.5,
    )
    fig = create_team_productivity_chart(data)
    assert isinstance(fig, go.Figure)
    trace = fig.data[0]
    assert list(trace["x"]) == ["tasks_completed", "deals_closed", "activity_level"]
    assert list(trace["y"]) == [50, 5, 7.5]


def test_create_customer_interaction_chart():
    data = CustomerInteractionResponse(
        start_date=date(2025, 4, 1),
        end_date=date(2025, 4, 30),
        total_interactions=200,
        avg_engagement_score=4.2,
    )
    fig = create_customer_interaction_chart(data)
    assert isinstance(fig, go.Figure)
    trace = fig.data[0]
    assert list(trace["x"]) == ["total_interactions", "avg_engagement_score"]
    assert list(trace["y"]) == [200, 4.2]


def test_create_pipeline_analytics_chart_multiple_stages():
    data = PipelineAnalyticsResponse(
        start_date=date(2025, 5, 1),
        end_date=date(2025, 5, 31),
        stage_conversion_rates={"Prospect": 0.2, "Qualified": 0.15, "Proposal": 0.1},
    )
    fig = create_pipeline_analytics_chart(data)
    assert isinstance(fig, go.Figure)
    trace = fig.data[0]
    assert list(trace["x"]) == ["Prospect", "Qualified", "Proposal"]
    assert list(trace["y"]) == [0.2, 0.15, 0.1]


def test_create_pipeline_analytics_chart_empty():
    data = PipelineAnalyticsResponse(
        start_date=date(2025, 6, 1),
        end_date=date(2025, 6, 30),
        stage_conversion_rates={},
    )
    fig = create_pipeline_analytics_chart(data)
    assert isinstance(fig, go.Figure)
    # when empty, functions return a Figure with no data
    assert len(fig.data) == 0
