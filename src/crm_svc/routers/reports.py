from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import base64
import logging
from typing import Any
from datetime import date

from crm_svc.models.base import get_db
from crm_svc.schemas.report import (
    DateRangeQuery,
    ReportTypeFilter,
    SalesPerformanceResponse,
    TeamProductivityResponse,
    CustomerInteractionResponse,
    PipelineAnalyticsResponse,
    ReportExportResponse,
)
from crm_svc.services.report_service import ReportService

logger = logging.getLogger(__name__)

reports_router = APIRouter()


def _parse_date_range(
    start_date: date = Query(...), end_date: date = Query(...)
) -> DateRangeQuery:
    """Dependency helper to build and validate DateRangeQuery explicitly.

    Using an explicit function avoids unhandled pydantic_core ValidationError
    bubbling out of FastAPI's dependency resolver. It converts validation
    failures into HTTP 422 responses.
    """
    try:
        return DateRangeQuery.model_validate({"start_date": start_date, "end_date": end_date})
    except Exception as e:
        logger.error(e, exc_info=True)
        # FastAPI maps HTTPException to an HTTP response; use 422 to indicate validation
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@reports_router.get("/sales-performance", response_model=SalesPerformanceResponse)
def get_sales_performance(
    date_range: DateRangeQuery = Depends(_parse_date_range), db_session: Session = Depends(get_db)
) -> Any:
    service = ReportService()
    try:
        resp = service.get_sales_performance(db_session, date_range.start_date, date_range.end_date)
        return resp
    except ValueError as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@reports_router.get("/team-productivity", response_model=TeamProductivityResponse)
def get_team_productivity(
    date_range: DateRangeQuery = Depends(_parse_date_range), db_session: Session = Depends(get_db)
) -> Any:
    service = ReportService()
    try:
        resp = service.get_team_productivity(db_session, date_range.start_date, date_range.end_date)
        return resp
    except ValueError as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@reports_router.get("/customer-interaction", response_model=CustomerInteractionResponse)
def get_customer_interaction(
    date_range: DateRangeQuery = Depends(_parse_date_range), db_session: Session = Depends(get_db)
) -> Any:
    service = ReportService()
    try:
        resp = service.get_customer_interaction(db_session, date_range.start_date, date_range.end_date)
        return resp
    except ValueError as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@reports_router.get("/pipeline-analytics", response_model=PipelineAnalyticsResponse)
def get_pipeline_analytics(
    date_range: DateRangeQuery = Depends(_parse_date_range), db_session: Session = Depends(get_db)
) -> Any:
    service = ReportService()
    try:
        resp = service.get_pipeline_analytics(db_session, date_range.start_date, date_range.end_date)
        return resp
    except ValueError as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@reports_router.get("/export", response_model=ReportExportResponse)
def export_report(
    report_type: ReportTypeFilter,
    date_range: DateRangeQuery = Depends(_parse_date_range),
    db_session: Session = Depends(get_db),
) -> Any:
    """Export selected report as base64 encoded CSV text."""
    service = ReportService()
    try:
        start = date_range.start_date
        end = date_range.end_date

        if report_type == ReportTypeFilter.SALES:
            data = service.get_sales_performance(db_session, start, end).model_dump()
            header = "start_date,end_date,revenue,conversion_rate,pipeline_velocity"
            row = f"{data['start_date']},{data['end_date']},{data['revenue']},{data['conversion_rate']},{data['pipeline_velocity']}"
            csv_text = header + "\n" + row + "\n"
        elif report_type == ReportTypeFilter.TEAM:
            data = service.get_team_productivity(db_session, start, end).model_dump()
            header = "start_date,end_date,tasks_completed,deals_closed,activity_level"
            row = f"{data['start_date']},{data['end_date']},{data['tasks_completed']},{data['deals_closed']},{data['activity_level']}"
            csv_text = header + "\n" + row + "\n"
        elif report_type == ReportTypeFilter.CUSTOMER:
            data = service.get_customer_interaction(db_session, start, end).model_dump()
            header = "start_date,end_date,total_interactions,avg_engagement_score"
            row = f"{data['start_date']},{data['end_date']},{data['total_interactions']},{data['avg_engagement_score']}"
            csv_text = header + "\n" + row + "\n"
        elif report_type == ReportTypeFilter.PIPELINE:
            data = service.get_pipeline_analytics(db_session, start, end).model_dump()
            # prepend a comment line with dates for traceability
            header = "stage,rate"
            rows = [f"{k},{v}" for k, v in data['stage_conversion_rates'].items()]
            csv_text = f"# start_date={start},end_date={end}\n" + header + "\n" + "\n".join(rows) + "\n"
        else:
            raise ValueError("Unsupported report type")

        b64 = base64.b64encode(csv_text.encode("utf-8")).decode("utf-8")
        filename = f"report_{report_type.value}.csv"
        return ReportExportResponse(filename=filename, content_type="text/csv", data_b64=b64)
    except ValueError as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
