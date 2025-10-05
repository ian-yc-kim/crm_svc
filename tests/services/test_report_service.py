from datetime import date

from sqlalchemy import select

from crm_svc.services.report_service import ReportService
from crm_svc.models import (
    SalesPerformanceMetrics,
    TeamProductivityMetrics,
    CustomerInteractionMetrics,
    PipelineAnalyticsMetrics,
)


def test_get_sales_performance_caches_result(db_session):
    svc = ReportService()
    start = date(2025, 1, 1)
    end = date(2025, 1, 3)

    res1 = svc.get_sales_performance(db_session, start, end)
    rows = db_session.execute(
        select(SalesPerformanceMetrics).where(
            SalesPerformanceMetrics.start_date == start,
            SalesPerformanceMetrics.end_date == end,
        )
    ).scalars().all()
    assert len(rows) == 1

    res2 = svc.get_sales_performance(db_session, start, end)
    assert res1.revenue == res2.revenue


def test_get_team_productivity_caches_result(db_session):
    svc = ReportService()
    start = date(2025, 2, 1)
    end = date(2025, 2, 7)

    res1 = svc.get_team_productivity(db_session, start, end)
    rows = db_session.execute(
        select(TeamProductivityMetrics).where(
            TeamProductivityMetrics.start_date == start,
            TeamProductivityMetrics.end_date == end,
        )
    ).scalars().all()
    assert len(rows) == 1

    res2 = svc.get_team_productivity(db_session, start, end)
    assert res1.tasks_completed == res2.tasks_completed


def test_get_customer_interaction_caches_result(db_session):
    svc = ReportService()
    start = date(2025, 3, 1)
    end = date(2025, 3, 5)

    res1 = svc.get_customer_interaction(db_session, start, end)
    rows = db_session.execute(
        select(CustomerInteractionMetrics).where(
            CustomerInteractionMetrics.start_date == start,
            CustomerInteractionMetrics.end_date == end,
        )
    ).scalars().all()
    assert len(rows) == 1

    res2 = svc.get_customer_interaction(db_session, start, end)
    assert res1.total_interactions == res2.total_interactions


def test_get_pipeline_analytics_caches_result(db_session):
    svc = ReportService()
    start = date(2025, 4, 1)
    end = date(2025, 4, 10)

    res1 = svc.get_pipeline_analytics(db_session, start, end)
    rows = db_session.execute(
        select(PipelineAnalyticsMetrics).where(
            PipelineAnalyticsMetrics.start_date == start,
            PipelineAnalyticsMetrics.end_date == end,
        )
    ).scalars().all()
    assert len(rows) == 1

    res2 = svc.get_pipeline_analytics(db_session, start, end)
    assert res1.stage_conversion_rates == res2.stage_conversion_rates


def test_invalid_date_range_raises(db_session):
    svc = ReportService()
    start = date(2025, 5, 10)
    end = date(2025, 5, 1)

    try:
        svc.get_sales_performance(db_session, start, end)
        assert False, "Expected ValueError"
    except ValueError:
        pass
