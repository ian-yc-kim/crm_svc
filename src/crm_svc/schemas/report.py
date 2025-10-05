from __future__ import annotations
from datetime import date
from enum import Enum
from typing import Dict

from pydantic import BaseModel, Field, model_validator


class ReportTypeFilter(str, Enum):
    SALES = "sales"
    TEAM = "team"
    PIPELINE = "pipeline"
    CUSTOMER = "customer"


class DateRangeQuery(BaseModel):
    start_date: date = Field(...)
    end_date: date = Field(...)

    @model_validator(mode="after")
    def check_dates(self) -> "DateRangeQuery":
        if self.start_date > self.end_date:
            raise ValueError("start_date must be less than or equal to end_date")
        return self


class SalesPerformanceResponse(BaseModel):
    start_date: date
    end_date: date
    revenue: float
    conversion_rate: float
    pipeline_velocity: float


class TeamProductivityResponse(BaseModel):
    start_date: date
    end_date: date
    tasks_completed: int
    deals_closed: int
    activity_level: float


class CustomerInteractionResponse(BaseModel):
    start_date: date
    end_date: date
    total_interactions: int
    avg_engagement_score: float


class PipelineAnalyticsResponse(BaseModel):
    start_date: date
    end_date: date
    stage_conversion_rates: Dict[str, float]


class ReportExportResponse(BaseModel):
    filename: str
    content_type: str
    data_b64: str
