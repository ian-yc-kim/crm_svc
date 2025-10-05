from datetime import date
import logging

from sqlalchemy import select

from crm_svc.models import (
    SalesPerformanceMetrics,
    TeamProductivityMetrics,
    CustomerInteractionMetrics,
    PipelineAnalyticsMetrics,
)


def test_report_models_crud(db_session):
    try:
        # Create
        sp = SalesPerformanceMetrics(
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 31),
            revenue=10000.0,
            conversion_rate=0.05,
            pipeline_velocity=1.2,
        )

        tp = TeamProductivityMetrics(
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 31),
            tasks_completed=42,
            deals_closed=5,
            activity_level=0.85,
        )

        ci = CustomerInteractionMetrics(
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 31),
            total_interactions=120,
            avg_engagement_score=4.2,
        )

        pa = PipelineAnalyticsMetrics(
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 31),
            stage_conversion_rates={"prospect": 0.1, "qualified": 0.3, "closed": 0.6},
        )

        db_session.add_all([sp, tp, ci, pa])
        db_session.commit()

        # Read
        sp_db = db_session.execute(select(SalesPerformanceMetrics).filter_by(id=sp.id)).scalars().one()
        assert sp_db.revenue == 10000.0

        tp_db = db_session.execute(select(TeamProductivityMetrics).filter_by(id=tp.id)).scalars().one()
        assert tp_db.tasks_completed == 42

        ci_db = db_session.execute(select(CustomerInteractionMetrics).filter_by(id=ci.id)).scalars().one()
        assert ci_db.total_interactions == 120

        pa_db = db_session.execute(select(PipelineAnalyticsMetrics).filter_by(id=pa.id)).scalars().one()
        assert isinstance(pa_db.stage_conversion_rates, dict)
        assert pa_db.stage_conversion_rates.get("qualified") == 0.3

        # Update
        sp_db.revenue = 11000.0
        db_session.commit()
        sp_updated = db_session.execute(select(SalesPerformanceMetrics).filter_by(id=sp.id)).scalars().one()
        assert sp_updated.revenue == 11000.0

        # Delete
        db_session.delete(sp_updated)
        db_session.commit()
        sp_deleted = db_session.execute(select(SalesPerformanceMetrics).filter_by(id=sp.id)).scalars().all()
        assert sp_deleted == []

    except Exception as e:
        logging.error(e, exc_info=True)
        raise
