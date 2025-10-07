import logging
from datetime import date
from typing import Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class ReportService:
    """Service to fetch or generate CRM reports without persisting mock data."""

    def _validate_date_range(self, start_date: date, end_date: date) -> None:
        if start_date > end_date:
            raise ValueError("start_date must be less than or equal to end_date")

    def _days_span(self, start_date: date, end_date: date) -> int:
        return (end_date - start_date).days + 1

    def get_sales_performance(self, db_session: Session, start_date: date, end_date: date):
        from crm_svc.models import SalesPerformanceMetrics
        from crm_svc.schemas import SalesPerformanceResponse

        self._validate_date_range(start_date, end_date)
        try:
            stmt = select(SalesPerformanceMetrics).where(
                SalesPerformanceMetrics.start_date == start_date,
                SalesPerformanceMetrics.end_date == end_date,
            )
            existing = db_session.execute(stmt).scalars().one_or_none()
            if existing:
                data = {
                    "start_date": existing.start_date,
                    "end_date": existing.end_date,
                    "revenue": float(existing.revenue),
                    "conversion_rate": float(existing.conversion_rate),
                    "pipeline_velocity": float(existing.pipeline_velocity),
                }
                return SalesPerformanceResponse.model_validate(data)

            # generate deterministic mock data (do NOT persist)
            days = self._days_span(start_date, end_date)
            revenue = float(days * 1000.0)
            conversion_rate = min(0.9, 0.05 + days * 0.03)
            pipeline_velocity = max(0.5, 10.0 / max(days, 1))

            data = {
                "start_date": start_date,
                "end_date": end_date,
                "revenue": revenue,
                "conversion_rate": conversion_rate,
                "pipeline_velocity": pipeline_velocity,
            }
            return SalesPerformanceResponse.model_validate(data)
        except ValueError:
            raise
        except Exception as e:
            logger.error(e, exc_info=True)
            try:
                db_session.rollback()
            except Exception:
                logger.error("Failed to rollback session", exc_info=True)
            raise

    def get_team_productivity(self, db_session: Session, start_date: date, end_date: date):
        from crm_svc.models import TeamProductivityMetrics
        from crm_svc.schemas import TeamProductivityResponse

        self._validate_date_range(start_date, end_date)
        try:
            stmt = select(TeamProductivityMetrics).where(
                TeamProductivityMetrics.start_date == start_date,
                TeamProductivityMetrics.end_date == end_date,
            )
            existing = db_session.execute(stmt).scalars().one_or_none()
            if existing:
                data = {
                    "start_date": existing.start_date,
                    "end_date": existing.end_date,
                    "tasks_completed": int(existing.tasks_completed),
                    "deals_closed": int(existing.deals_closed),
                    "activity_level": float(existing.activity_level),
                }
                return TeamProductivityResponse.model_validate(data)

            days = self._days_span(start_date, end_date)
            tasks_completed = int(days * 5)
            deals_closed = int(min(tasks_completed, max(0, tasks_completed * 0.3)))
            activity_level = min(1.0, 0.5 + days * 0.05)

            data = {
                "start_date": start_date,
                "end_date": end_date,
                "tasks_completed": tasks_completed,
                "deals_closed": deals_closed,
                "activity_level": float(activity_level),
            }
            return TeamProductivityResponse.model_validate(data)
        except ValueError:
            raise
        except Exception as e:
            logger.error(e, exc_info=True)
            try:
                db_session.rollback()
            except Exception:
                logger.error("Failed to rollback session", exc_info=True)
            raise

    def get_customer_interaction(self, db_session: Session, start_date: date, end_date: date):
        from crm_svc.models import CustomerInteractionMetrics
        from crm_svc.schemas import CustomerInteractionResponse

        self._validate_date_range(start_date, end_date)
        try:
            stmt = select(CustomerInteractionMetrics).where(
                CustomerInteractionMetrics.start_date == start_date,
                CustomerInteractionMetrics.end_date == end_date,
            )
            existing = db_session.execute(stmt).scalars().one_or_none()
            if existing:
                data = {
                    "start_date": existing.start_date,
                    "end_date": existing.end_date,
                    "total_interactions": int(existing.total_interactions),
                    "avg_engagement_score": float(existing.avg_engagement_score),
                }
                return CustomerInteractionResponse.model_validate(data)

            days = self._days_span(start_date, end_date)
            total_interactions = int(days * 20)
            avg_engagement_score = min(1.0, 0.3 + days * 0.02)

            data = {
                "start_date": start_date,
                "end_date": end_date,
                "total_interactions": total_interactions,
                "avg_engagement_score": float(avg_engagement_score),
            }
            return CustomerInteractionResponse.model_validate(data)
        except ValueError:
            raise
        except Exception as e:
            logger.error(e, exc_info=True)
            try:
                db_session.rollback()
            except Exception:
                logger.error("Failed to rollback session", exc_info=True)
            raise

    def get_pipeline_analytics(self, db_session: Session, start_date: date, end_date: date):
        from crm_svc.models import PipelineAnalyticsMetrics
        from crm_svc.schemas import PipelineAnalyticsResponse

        self._validate_date_range(start_date, end_date)
        try:
            stmt = select(PipelineAnalyticsMetrics).where(
                PipelineAnalyticsMetrics.start_date == start_date,
                PipelineAnalyticsMetrics.end_date == end_date,
            )
            existing = db_session.execute(stmt).scalars().one_or_none()
            if existing:
                data = {
                    "start_date": existing.start_date,
                    "end_date": existing.end_date,
                    "stage_conversion_rates": dict(existing.stage_conversion_rates or {}),
                }
                return PipelineAnalyticsResponse.model_validate(data)

            days = self._days_span(start_date, end_date)
            base_rates: Dict[str, float] = {
                "lead": 0.6,
                "qualified": 0.5,
                "proposal": 0.3,
                "negotiation": 0.2,
                "closed_won": 0.1,
            }
            stage_conversion_rates: Dict[str, float] = {}
            for k, v in base_rates.items():
                adjusted = v + (days * 0.005)
                adjusted = max(0.01, min(0.95, adjusted))
                stage_conversion_rates[k] = float(round(adjusted, 4))

            data = {
                "start_date": start_date,
                "end_date": end_date,
                "stage_conversion_rates": stage_conversion_rates,
            }
            return PipelineAnalyticsResponse.model_validate(data)
        except ValueError:
            raise
        except Exception as e:
            logger.error(e, exc_info=True)
            try:
                db_session.rollback()
            except Exception:
                logger.error("Failed to rollback session", exc_info=True)
            raise
